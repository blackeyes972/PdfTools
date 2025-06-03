# output_manager.py
"""
Sistema di gestione output files per applicazioni PDF.
Organizza i file di output in directory strutturate e configurabili.
"""

import os
import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from enum import Enum
from typing import Optional, List, Dict


class OutputType(Enum):
    """Tipi di operazioni di output supportate."""
    COMPRESSED = "compressed"
    MERGED = "merged"
    PROTECTED = "protected"
    UNPROTECTED = "unprotected"
    WATERMARKED = "watermarked"
    CONVERTED = "converted"
    SPLIT = "split"


class OutputManager:
    """
    Gestisce l'organizzazione e la configurazione dei file di output.
    Completamente riutilizzabile per altre applicazioni.
    """
    
    def __init__(self, base_output_dir=None, auto_cleanup_days=30):
        """
        Inizializza l'OutputManager.
        
        Args:
            base_output_dir (str): Directory base per gli output (default: ./output)
            auto_cleanup_days (int): Giorni dopo i quali i file vengono eliminati automaticamente (0 = disabilitato)
        """
        self.base_output_dir = Path(base_output_dir) if base_output_dir else Path.cwd() / "output"
        self.auto_cleanup_days = auto_cleanup_days
        self.config_file = "output_config.json"
        self.settings = self._load_settings()
        
        # Crea la struttura di directory
        self._create_directory_structure()
        
        # Esegui pulizia automatica se abilitata
        if self.auto_cleanup_days > 0:
            self._auto_cleanup()
    
    def _load_settings(self):
        """Carica le impostazioni salvate."""
        default_settings = {
            'base_output_dir': str(self.base_output_dir),
            'auto_cleanup_days': self.auto_cleanup_days,
            'create_subdirectories': True,
            'add_timestamp': True,
            'preserve_original_names': True,
            'max_files_per_directory': 1000
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    # Aggiorna con nuove impostazioni se mancano
                    for key, value in default_settings.items():
                        if key not in settings:
                            settings[key] = value
                    return settings
        except Exception:
            pass
        
        return default_settings
    
    def _save_settings(self):
        """Salva le impostazioni correnti."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception:
            pass  # Ignora errori di salvataggio
    
    def _create_directory_structure(self):
        """Crea la struttura di directory per gli output."""
        self.base_output_dir.mkdir(parents=True, exist_ok=True)
        
        if self.settings.get('create_subdirectories', True):
            # Crea sottodirectory per ogni tipo di operazione
            for output_type in OutputType:
                type_dir = self.base_output_dir / output_type.value
                type_dir.mkdir(exist_ok=True)
                
                # Crea anche directory per data (anno/mese)
                today = datetime.now()
                year_dir = type_dir / str(today.year)
                month_dir = year_dir / f"{today.month:02d}"
                month_dir.mkdir(parents=True, exist_ok=True)
    
    def get_output_path(self, original_filename, output_type: OutputType, 
                       custom_suffix=None, extension=None):
        """
        Genera il percorso completo per un file di output.
        
        Args:
            original_filename (str): Nome del file originale
            output_type (OutputType): Tipo di operazione
            custom_suffix (str): Suffisso personalizzato (opzionale)
            extension (str): Estensione file (default: .pdf)
            
        Returns:
            str: Percorso completo del file di output
        """
        original_path = Path(original_filename)
        base_name = original_path.stem
        file_extension = extension or original_path.suffix or '.pdf'
        
        # Determina la directory di destinazione
        if self.settings.get('create_subdirectories', True):
            today = datetime.now()
            output_dir = (self.base_output_dir / 
                         output_type.value / 
                         str(today.year) / 
                         f"{today.month:02d}")
        else:
            output_dir = self.base_output_dir
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Costruisce il nome del file
        filename_parts = []
        
        if self.settings.get('preserve_original_names', True):
            filename_parts.append(base_name)
        
        # Aggiunge suffisso dell'operazione
        operation_suffixes = {
            OutputType.COMPRESSED: 'compressed',
            OutputType.MERGED: 'merged',
            OutputType.PROTECTED: 'protected',
            OutputType.UNPROTECTED: 'unprotected',
            OutputType.WATERMARKED: 'watermarked',
            OutputType.CONVERTED: 'converted',
            OutputType.SPLIT: 'split'
        }
        
        if custom_suffix:
            filename_parts.append(custom_suffix)
        else:
            filename_parts.append(operation_suffixes.get(output_type, 'processed'))
        
        # Aggiunge timestamp se abilitato
        if self.settings.get('add_timestamp', True):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename_parts.append(timestamp)
        
        # Combina le parti
        filename = '_'.join(filename_parts) + file_extension
        output_path = output_dir / filename
        
        # Verifica che non ci siano conflitti di nomi
        counter = 1
        while output_path.exists():
            filename_with_counter = '_'.join(filename_parts + [f'({counter})']) + file_extension
            output_path = output_dir / filename_with_counter
            counter += 1
            
            # Evita loop infiniti
            if counter > 1000:
                break
        
        return str(output_path)
    
    def get_batch_output_directory(self, output_type: OutputType):
        """
        Ottiene la directory per operazioni batch.
        
        Args:
            output_type (OutputType): Tipo di operazione
            
        Returns:
            str: Percorso della directory per batch
        """
        if self.settings.get('create_subdirectories', True):
            today = datetime.now()
            batch_dir = (self.base_output_dir / 
                        output_type.value / 
                        str(today.year) / 
                        f"{today.month:02d}" / 
                        f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        else:
            batch_dir = self.base_output_dir / f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        batch_dir.mkdir(parents=True, exist_ok=True)
        return str(batch_dir)
    
    def set_base_output_directory(self, new_directory):
        """
        Cambia la directory base per gli output.
        
        Args:
            new_directory (str): Nuova directory base
        """
        self.base_output_dir = Path(new_directory)
        self.settings['base_output_dir'] = str(new_directory)
        self._save_settings()
        self._create_directory_structure()
    
    def get_base_output_directory(self):
        """Restituisce la directory base corrente."""
        return str(self.base_output_dir)
    
    def configure_settings(self, **kwargs):
        """
        Configura le impostazioni dell'OutputManager.
        
        Args:
            **kwargs: Impostazioni da aggiornare
        """
        valid_settings = {
            'auto_cleanup_days', 'create_subdirectories', 
            'add_timestamp', 'preserve_original_names', 
            'max_files_per_directory'
        }
        
        for key, value in kwargs.items():
            if key in valid_settings:
                self.settings[key] = value
        
        self._save_settings()
        
        # Riapplica le impostazioni
        if 'auto_cleanup_days' in kwargs:
            self.auto_cleanup_days = kwargs['auto_cleanup_days']
        
        if 'create_subdirectories' in kwargs:
            self._create_directory_structure()
    
    def get_output_statistics(self):
        """
        Restituisce statistiche sui file di output.
        
        Returns:
            dict: Statistiche organizzate per tipo
        """
        stats = {
            'total_files': 0,
            'total_size_mb': 0,
            'by_type': {},
            'by_date': {}
        }
        
        if not self.base_output_dir.exists():
            return stats
        
        for file_path in self.base_output_dir.rglob('*.pdf'):
            try:
                file_stat = file_path.stat()
                file_size_mb = file_stat.st_size / (1024 * 1024)
                
                stats['total_files'] += 1
                stats['total_size_mb'] += file_size_mb
                
                # Statistiche per tipo (basate sulla directory parent)
                type_name = file_path.parent.name
                if type_name not in stats['by_type']:
                    stats['by_type'][type_name] = {'count': 0, 'size_mb': 0}
                
                stats['by_type'][type_name]['count'] += 1
                stats['by_type'][type_name]['size_mb'] += file_size_mb
                
                # Statistiche per data
                mod_date = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m')
                if mod_date not in stats['by_date']:
                    stats['by_date'][mod_date] = {'count': 0, 'size_mb': 0}
                
                stats['by_date'][mod_date]['count'] += 1
                stats['by_date'][mod_date]['size_mb'] += file_size_mb
                
            except Exception:
                continue
        
        # Arrotonda i valori delle dimensioni
        stats['total_size_mb'] = round(stats['total_size_mb'], 2)
        for type_stats in stats['by_type'].values():
            type_stats['size_mb'] = round(type_stats['size_mb'], 2)
        for date_stats in stats['by_date'].values():
            date_stats['size_mb'] = round(date_stats['size_mb'], 2)
        
        return stats
    
    def _auto_cleanup(self):
        """Esegue la pulizia automatica dei file vecchi."""
        if self.auto_cleanup_days <= 0:
            return
        
        cutoff_date = datetime.now() - timedelta(days=self.auto_cleanup_days)
        deleted_count = 0
        deleted_size = 0
        
        if not self.base_output_dir.exists():
            return
        
        for file_path in self.base_output_dir.rglob('*.pdf'):
            try:
                file_stat = file_path.stat()
                file_date = datetime.fromtimestamp(file_stat.st_mtime)
                
                if file_date < cutoff_date:
                    deleted_size += file_stat.st_size
                    file_path.unlink()
                    deleted_count += 1
                    
            except Exception:
                continue
        
        # Rimuovi directory vuote
        self._remove_empty_directories()
        
        return {
            'deleted_files': deleted_count,
            'deleted_size_mb': round(deleted_size / (1024 * 1024), 2)
        }
    
    def manual_cleanup(self, days_older_than=None, file_types=None):
        """
        Esegue una pulizia manuale personalizzata.
        
        Args:
            days_older_than (int): Elimina file più vecchi di N giorni
            file_types (list): Lista di OutputType da pulire (None = tutti)
            
        Returns:
            dict: Statistiche della pulizia
        """
        if days_older_than is None:
            days_older_than = self.auto_cleanup_days
        
        if days_older_than <= 0:
            return {'deleted_files': 0, 'deleted_size_mb': 0}
        
        cutoff_date = datetime.now() - timedelta(days=days_older_than)
        deleted_count = 0
        deleted_size = 0
        
        if not self.base_output_dir.exists():
            return {'deleted_files': 0, 'deleted_size_mb': 0}
        
        # Determina le directory da pulire
        if file_types:
            target_dirs = [self.base_output_dir / ft.value for ft in file_types]
        else:
            target_dirs = [self.base_output_dir]
        
        for target_dir in target_dirs:
            if not target_dir.exists():
                continue
                
            for file_path in target_dir.rglob('*.pdf'):
                try:
                    file_stat = file_path.stat()
                    file_date = datetime.fromtimestamp(file_stat.st_mtime)
                    
                    if file_date < cutoff_date:
                        deleted_size += file_stat.st_size
                        file_path.unlink()
                        deleted_count += 1
                        
                except Exception:
                    continue
        
        # Rimuovi directory vuote
        self._remove_empty_directories()
        
        return {
            'deleted_files': deleted_count,
            'deleted_size_mb': round(deleted_size / (1024 * 1024), 2)
        }
    
    def _remove_empty_directories(self):
        """Rimuove le directory vuote dalla struttura output."""
        if not self.base_output_dir.exists():
            return
        
        # Rimuovi directory vuote dal basso verso l'alto
        for directory in sorted(self.base_output_dir.rglob('*'), key=lambda p: len(p.parts), reverse=True):
            if directory.is_dir() and not any(directory.iterdir()):
                try:
                    directory.rmdir()
                except Exception:
                    continue
    
    def open_output_directory(self):
        """Apre la directory di output nel file manager del sistema."""
        import subprocess
        import platform
        
        output_dir = str(self.base_output_dir)
        
        try:
            if platform.system() == 'Windows':
                subprocess.run(['explorer', output_dir])
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', output_dir])
            else:  # Linux e altri Unix
                subprocess.run(['xdg-open', output_dir])
        except Exception:
            pass  # Ignora errori di apertura
    
    def export_file_list(self, output_file=None):
        """
        Esporta un elenco di tutti i file di output in formato JSON.
        
        Args:
            output_file (str): Percorso del file di export (default: file_list.json)
            
        Returns:
            str: Percorso del file creato
        """
        if output_file is None:
            output_file = self.base_output_dir / 'file_list.json'
        
        file_list = []
        
        if self.base_output_dir.exists():
            for file_path in self.base_output_dir.rglob('*.pdf'):
                try:
                    file_stat = file_path.stat()
                    relative_path = file_path.relative_to(self.base_output_dir)
                    
                    file_info = {
                        'filename': file_path.name,
                        'relative_path': str(relative_path),
                        'full_path': str(file_path),
                        'size_bytes': file_stat.st_size,
                        'size_mb': round(file_stat.st_size / (1024 * 1024), 2),
                        'created_date': datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                        'modified_date': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                        'operation_type': file_path.parent.name if file_path.parent != self.base_output_dir else 'unknown'
                    }
                    
                    file_list.append(file_info)
                    
                except Exception:
                    continue
        
        # Ordina per data di modifica (più recenti prima)
        file_list.sort(key=lambda x: x['modified_date'], reverse=True)
        
        export_data = {
            'export_date': datetime.now().isoformat(),
            'base_directory': str(self.base_output_dir),
            'total_files': len(file_list),
            'total_size_mb': sum(f['size_mb'] for f in file_list),
            'files': file_list
        }
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Failed to export file list: {str(e)}")
        
        return str(output_file)