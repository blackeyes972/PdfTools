# main.py
"""
Applicazione principale PDF Tools - Versione Modulare
Questo file orchestra tutti i componenti dell'applicazione.
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal, QObject
from PyQt6.QtGui import QIcon

# Import dei moduli personalizzati
from translations import Translations
from pdf_functions import PDFProcessor, PDFValidator
from output_manager import OutputManager, OutputType
from menu_manager import ApplicationMenuManager, MenuAction
from ui_manager import UIManager


class PDFWorker(QObject):
    """
    Worker thread per eseguire operazioni PDF in background
    senza bloccare l'interfaccia utente.
    """
    
    # Segnali per comunicare con il thread principale
    operation_completed = pyqtSignal(str, bool, str)  # operazione, successo, messaggio
    progress_updated = pyqtSignal(int)  # progresso (0-100)
    
    def __init__(self, pdf_processor=None):
        super().__init__()
        self.processor = pdf_processor or PDFProcessor()
    
    def compress_pdf(self, input_file, output_file=None):
        """Esegue la compressione PDF in background."""
        try:
            self.progress_updated.emit(25)
            result_path = self.processor.compress_pdf(input_file, output_file)
            self.progress_updated.emit(100)
            self.operation_completed.emit('compress', True, f'PDF compressed successfully: {result_path}')
        except Exception as e:
            self.operation_completed.emit('compress', False, str(e))
    
    def merge_pdfs(self, input_files, output_file=None):
        """Esegue l'unione PDF in background."""
        try:
            self.progress_updated.emit(20)
            result_path = self.processor.merge_pdfs(input_files, output_file)
            self.progress_updated.emit(100)
            self.operation_completed.emit('merge', True, f'PDFs merged successfully: {result_path}')
        except Exception as e:
            self.operation_completed.emit('merge', False, str(e))
    
    def protect_pdf(self, input_file, password, output_file=None):
        """Esegue la protezione PDF in background."""
        try:
            self.progress_updated.emit(30)
            result_path = self.processor.protect_pdf(input_file, password, output_file)
            self.progress_updated.emit(100)
            self.operation_completed.emit('protect', True, f'PDF protected successfully: {result_path}')
        except Exception as e:
            self.operation_completed.emit('protect', False, str(e))
    
    def remove_protection(self, input_file, password, output_file=None):
        """Rimuove la protezione PDF in background."""
        try:
            self.progress_updated.emit(30)
            result_path = self.processor.remove_protection(input_file, password, output_file)
            self.progress_updated.emit(100)
            self.operation_completed.emit('remove_protection', True, f'Protection removed successfully: {result_path}')
        except Exception as e:
            self.operation_completed.emit('remove_protection', False, str(e))
    
    def add_watermark(self, input_file, watermark_text, output_file=None):
        """Aggiunge filigrana in background."""
        try:
            self.progress_updated.emit(40)
            result_path = self.processor.add_watermark(input_file, watermark_text, output_file)
            self.progress_updated.emit(100)
            self.operation_completed.emit('watermark', True, f'Watermark added successfully: {result_path}')
        except Exception as e:
            self.operation_completed.emit('watermark', False, str(e))


class PDFToolsApplication(QMainWindow):
    """
    Classe principale dell'applicazione PDF Tools.
    Orchestra tutti i componenti e gestisce la logica dell'applicazione.
    """
    
    def __init__(self):
        super().__init__()
        
        # Inizializza i componenti
        self.translations = Translations('it')  # Lingua di default italiana
        
        # Inizializza il theme manager
        from theme_manager import ThemeManager
        self.theme_manager = ThemeManager()
        
        # Inizializza l'output manager
        self.output_manager = OutputManager(auto_cleanup_days=30)
        
        # Inizializza il PDF processor con output manager
        self.pdf_processor = PDFProcessor(self.output_manager)
        
        self.ui_manager = None
        self.menu_manager = None
        
        # Worker thread per operazioni PDF
        self.pdf_worker = None
        self.worker_thread = None
        
        # Impostazioni applicazione
        self.current_language = 'it'
        self.last_directory = str(Path.home())
        
        # Inizializza l'applicazione
        self.init_application()
    
    def init_application(self):
        """Inizializza tutti i componenti dell'applicazione."""
        # Configura la finestra principale
        self.setWindowTitle(self.translations.get('app_title'))
        self.setMinimumSize(1000, 700)
        
        # Inizializza l'UI Manager con theme manager
        self.ui_manager = UIManager(self, self.translations, self.theme_manager)
        self.ui_manager.setup_main_window()
        
        # Inizializza il Menu Manager con theme manager
        self.menu_manager = ApplicationMenuManager(self, self.translations, self.theme_manager)
        self.setup_menus()
        
        # Connetti i segnali
        self.connect_signals()
        
        # Configura il worker thread
        self.setup_worker_thread()
        
        # Applica le traduzioni iniziali
        self.update_interface_language()
    
    def setup_menus(self):
        """Configura tutti i menu dell'applicazione."""
        # Crea i menu base con ordine aggiornato: File, Strumenti, Tema, Lingua, Help
        file_menu, tools_menu, theme_menu, lang_menu, help_menu = self.menu_manager.setup_standard_menus()
        
        # Menu File
        file_actions = [
            MenuAction('browse', self.translations.get('browse'), 
                      callback=self.browse_file, shortcut='Ctrl+O'),
            MenuAction('separator', ''),
            MenuAction('compress', self.translations.get('compress'), 
                      callback=self.compress_pdf, shortcut='Ctrl+C'),
            MenuAction('merge', self.translations.get('merge'), 
                      callback=self.merge_pdfs, shortcut='Ctrl+M'),
            MenuAction('protect', self.translations.get('protect'), 
                      callback=self.protect_pdf, shortcut='Ctrl+P'),
            MenuAction('remove_protection', self.translations.get('remove_protection'), 
                      callback=self.remove_protection),
            MenuAction('add_watermark', self.translations.get('add_watermark'), 
                      callback=self.add_watermark, shortcut='Ctrl+W'),
            MenuAction('separator', ''),
            MenuAction('clear_fields', self.translations.get('clear_fields'), 
                      callback=self.clear_fields, shortcut='Ctrl+R'),
            MenuAction('separator', ''),
            MenuAction('exit', self.translations.get('exit'), 
                      callback=self.close, shortcut='Ctrl+Q')
        ]
        
        for action in file_actions:
            if action.name == 'separator':
                self.menu_manager.add_separator_to_menu('file')
            else:
                self.menu_manager.add_action_to_menu('file', action)
        
        # Menu Tools (ora già creato da setup_standard_menus)
        tools_actions = [
            MenuAction('configure_output', self.translations.get('configure_output'),
                      callback=self.configure_output_directory),
            MenuAction('open_output_folder', self.translations.get('open_output_folder'),
                      callback=self.open_output_folder),
            MenuAction('separator', ''),
            MenuAction('output_statistics', self.translations.get('output_statistics'),
                      callback=self.show_output_statistics),
            MenuAction('cleanup_old_files', self.translations.get('cleanup_old_files'),
                      callback=self.cleanup_old_files)
        ]
        
        for action in tools_actions:
            if action.name == 'separator':
                self.menu_manager.add_separator_to_menu('tools')
            else:
                self.menu_manager.add_action_to_menu('tools', action)
        
        # Menu Tema
        self.menu_manager.setup_theme_menu()
        
        # Menu Lingua
        self.menu_manager.setup_language_menu()
        
        # Menu Help
        help_actions = [
            MenuAction('about', self.translations.get('about'), 
                      callback=self.show_about, shortcut='F1')
        ]
        
        for action in help_actions:
            self.menu_manager.add_action_to_menu('help', action)
        
        # Connetti il cambio lingua
        self.menu_manager.language_changed.connect(self.change_language)
    
    def connect_signals(self):
        """Connette tutti i segnali dell'interfaccia."""
        # Connetti i bottoni dell'UI
        browse_btn = self.ui_manager.get_widget('browse_btn')
        if browse_btn:
            browse_btn.clicked.connect(self.browse_file)
        
        compress_btn = self.ui_manager.get_widget('compress_btn')
        if compress_btn:
            compress_btn.clicked.connect(self.compress_pdf)
        
        merge_btn = self.ui_manager.get_widget('merge_btn')
        if merge_btn:
            merge_btn.clicked.connect(self.merge_pdfs)
        
        protect_btn = self.ui_manager.get_widget('protect_btn')
        if protect_btn:
            protect_btn.clicked.connect(self.protect_pdf)
        
        remove_protection_btn = self.ui_manager.get_widget('remove_protection_btn')
        if remove_protection_btn:
            remove_protection_btn.clicked.connect(self.remove_protection)
        
        watermark_btn = self.ui_manager.get_widget('watermark_btn')
        if watermark_btn:
            watermark_btn.clicked.connect(self.add_watermark)
        
        clear_btn = self.ui_manager.get_widget('clear_btn')
        if clear_btn:
            clear_btn.clicked.connect(self.clear_fields)
    
    def setup_worker_thread(self):
        """Configura il worker thread per operazioni PDF."""
        self.worker_thread = QThread()
        self.pdf_worker = PDFWorker(self.pdf_processor)
        self.pdf_worker.moveToThread(self.worker_thread)
        
        # Connetti i segnali del worker
        self.pdf_worker.operation_completed.connect(self.on_operation_completed)
        self.pdf_worker.progress_updated.connect(self.on_progress_updated)
        
        self.worker_thread.start()
    
    def browse_file(self):
        """Apre la finestra di selezione file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.translations.get('select_pdf'),
            self.last_directory,
            "PDF Files (*.pdf);;All Files (*)"
        )
        
        if file_path:
            self.last_directory = os.path.dirname(file_path)
            self.ui_manager.set_input_file_path(file_path)
            
            # Mostra informazioni sulla directory di output corrente
            output_dir = self.output_manager.get_base_output_directory()
            self.ui_manager.set_output_file_path(f"Auto-generated in: {output_dir}")
            
            self.ui_manager.show_status_message(
                self.translations.get('file_selected', file_path), 5000
            )
    
    def compress_pdf(self):
        """Avvia la compressione PDF."""
        input_file = self.ui_manager.get_input_file_path()
        output_file = self.ui_manager.get_output_file_path()
        
        if not self.validate_basic_inputs(input_file, output_file):
            return
        
        self.ui_manager.enable_toolbar_buttons(False)
        self.ui_manager.show_status_message(self.translations.get('compressing'))
        
        # Esegui l'operazione nel worker thread
        self.pdf_worker.compress_pdf(input_file, output_file)
    
    def merge_pdfs(self):
        """Avvia l'unione di PDF."""
        input_files, _ = QFileDialog.getOpenFileNames(
            self,
            self.translations.get('select_pdfs_to_merge'),
            self.last_directory,
            "PDF Files (*.pdf)"
        )
        
        if not input_files:
            QMessageBox.warning(
                self, 
                self.translations.get('warning'),
                self.translations.get('no_files_selected')
            )
            return
        
        output_file, _ = QFileDialog.getSaveFileName(
            self,
            self.translations.get('save_merged_pdf'),
            self.last_directory,
            "PDF Files (*.pdf)"
        )
        
        if not output_file:
            return
        
        self.ui_manager.enable_toolbar_buttons(False)
        self.ui_manager.show_status_message(self.translations.get('merging'))
        
        # Esegui l'operazione nel worker thread
        self.pdf_worker.merge_pdfs(input_files, output_file)
    
    def protect_pdf(self):
        """Avvia la protezione PDF."""
        input_file = self.ui_manager.get_input_file_path()
        output_file = self.ui_manager.get_output_file_path()
        password = self.ui_manager.get_password()
        
        if not self.validate_basic_inputs(input_file, output_file):
            return
        
        if not password:
            QMessageBox.warning(
                self,
                self.translations.get('warning'),
                self.translations.get('no_password')
            )
            return
        
        # Valida la password
        is_valid, message = PDFValidator.validate_password_strength(password)
        if not is_valid:
            QMessageBox.warning(self, self.translations.get('warning'), message)
            return
        
        self.ui_manager.enable_toolbar_buttons(False)
        self.ui_manager.show_status_message(self.translations.get('protecting'))
        
        # Esegui l'operazione nel worker thread
        self.pdf_worker.protect_pdf(input_file, output_file, password)
    
    def remove_protection(self):
        """Rimuove la protezione PDF."""
        input_file = self.ui_manager.get_input_file_path()
        output_file = self.ui_manager.get_output_file_path()
        password = self.ui_manager.get_password()
        
        if not self.validate_basic_inputs(input_file, output_file):
            return
        
        if not password:
            QMessageBox.warning(
                self,
                self.translations.get('warning'),
                self.translations.get('no_password')
            )
            return
        
        self.ui_manager.enable_toolbar_buttons(False)
        self.ui_manager.show_status_message(self.translations.get('removing_protection'))
        
        # Esegui l'operazione nel worker thread
        self.pdf_worker.remove_protection(input_file, output_file, password)
    
    def add_watermark(self):
        """Aggiunge filigrana al PDF."""
        input_file = self.ui_manager.get_input_file_path()
        output_file = self.ui_manager.get_output_file_path()
        watermark_text = self.ui_manager.get_watermark_text()
        
        if not self.validate_basic_inputs(input_file, output_file):
            return
        
        if not watermark_text:
            QMessageBox.warning(
                self,
                self.translations.get('warning'),
                self.translations.get('no_watermark_text')
            )
            return
        
        self.ui_manager.enable_toolbar_buttons(False)
        self.ui_manager.show_status_message(self.translations.get('adding_watermark'))
        
        # Esegui l'operazione nel worker thread
        self.pdf_worker.add_watermark(input_file, output_file, watermark_text)
    
    def clear_fields(self):
        """Pulisce tutti i campi."""
        self.ui_manager.clear_all_fields()
        self.ui_manager.show_status_message(self.translations.get('fields_cleared'), 3000)
    
    def validate_basic_inputs(self, input_file):
        """
        Valida gli input di base (solo file di input ora che output è auto-generato).
        
        Args:
            input_file (str): Percorso file di input
            
        Returns:
            bool: True se validi, False altrimenti
        """
        if not input_file:
            QMessageBox.warning(
                self,
                self.translations.get('warning'),
                self.translations.get('no_file_selected')
            )
            return False
        
        if not os.path.exists(input_file):
            QMessageBox.warning(
                self,
                self.translations.get('error'),
                self.translations.get('file_not_found')
            )
            return False
        
        if not PDFValidator.is_valid_pdf(input_file):
            QMessageBox.warning(
                self,
                self.translations.get('error'),
                self.translations.get('invalid_pdf')
            )
            return False
        
        return True
    
    def configure_output_directory(self):
        """Apre la finestra per configurare la directory di output."""
        current_dir = self.output_manager.get_base_output_directory()
        
        new_dir = QFileDialog.getExistingDirectory(
            self,
            self.translations.get('select_output_directory'),
            current_dir
        )
        
        if new_dir and new_dir != current_dir:
            self.output_manager.set_base_output_directory(new_dir)
            self.ui_manager.show_status_message(
                self.translations.get('output_directory_changed', new_dir), 5000
            )
            QMessageBox.information(
                self,
                self.translations.get('success'),
                self.translations.get('output_directory_changed', new_dir)
            )
    
    def open_output_folder(self):
        """Apre la cartella di output nel file manager."""
        try:
            self.output_manager.open_output_directory()
            self.ui_manager.show_status_message(
                self.translations.get('opening_output_folder'), 3000
            )
        except Exception as e:
            QMessageBox.warning(
                self,
                self.translations.get('error'),
                f"Could not open output folder: {str(e)}"
            )
    
    def show_output_statistics(self):
        """Mostra le statistiche dei file di output."""
        try:
            stats = self.output_manager.get_output_statistics()
            
            # Costruisce il messaggio delle statistiche
            stats_message = f"""
            <h3>{self.translations.get('statistics_title')}</h3>
            <p><b>{self.translations.get('total_files', stats['total_files'])}</b></p>
            <p><b>{self.translations.get('total_size', stats['total_size_mb'])}</b></p>
            
            <h4>{self.translations.get('files_by_type')}</h4>
            <ul>
            """
            
            for type_name, type_stats in stats['by_type'].items():
                stats_message += f"<li>{type_name}: {type_stats['count']} files ({type_stats['size_mb']} MB)</li>"
            
            stats_message += "</ul>"
            
            QMessageBox.information(
                self,
                self.translations.get('statistics_title'),
                stats_message
            )
            
        except Exception as e:
            QMessageBox.warning(
                self,
                self.translations.get('error'),
                f"Could not retrieve statistics: {str(e)}"
            )
    
    def cleanup_old_files(self):
        """Esegue la pulizia dei file vecchi."""
        # Chiedi conferma all'utente
        reply = QMessageBox.question(
            self,
            self.translations.get('cleanup_old_files'),
            "Are you sure you want to delete files older than 30 days?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                result = self.output_manager.manual_cleanup(days_older_than=30)
                
                message = self.translations.get(
                    'cleanup_completed',
                    result['deleted_files'],
                    result['deleted_size_mb']
                )
                
                QMessageBox.information(
                    self,
                    self.translations.get('success'),
                    message
                )
                
                self.ui_manager.show_status_message(message, 5000)
                
            except Exception as e:
                QMessageBox.warning(
                    self,
                    self.translations.get('error'),
                    f"Cleanup failed: {str(e)}"
                )
    
    def on_operation_completed(self, operation, success, message):
        """
        Gestisce il completamento di un'operazione PDF.
        
        Args:
            operation (str): Tipo di operazione
            success (bool): Se l'operazione è riuscita
            message (str): Messaggio di risultato
        """
        self.ui_manager.enable_toolbar_buttons(True)
        
        if success:
            QMessageBox.information(
                self,
                self.translations.get('success'),
                message
            )
            self.ui_manager.show_status_message(self.translations.get('operation_completed'), 5000)
            
            # Pulisce alcuni campi dopo il successo
            if operation in ['protect', 'remove_protection']:
                self.ui_manager.clear_password()
            elif operation == 'watermark':
                self.ui_manager.clear_watermark()
        else:
            QMessageBox.critical(
                self,
                self.translations.get('error'),
                f"{self.translations.get('operation_failed')}: {message}"
            )
            self.ui_manager.show_status_message(self.translations.get('operation_failed'), 5000)
    
    def on_progress_updated(self, progress):
        """
        Aggiorna il progresso dell'operazione.
        
        Args:
            progress (int): Progresso da 0 a 100
        """
        # TODO: Implementare una progress bar nella UI
        pass
    
    def change_language(self, language):
        """
        Cambia la lingua dell'applicazione.
        
        Args:
            language (str): Codice della nuova lingua
        """
        self.current_language = language
        self.translations.set_language(language)
        self.update_interface_language()
    
    def update_interface_language(self):
        """Aggiorna tutti i testi dell'interfaccia con la lingua corrente."""
        # Aggiorna UI Manager
        self.ui_manager.update_translations()
        
        # Aggiorna Menu Manager
        self.menu_manager.update_translations()
        
        # Aggiorna status bar
        self.ui_manager.show_status_message(self.translations.get('ready'))
    
    def show_about(self):
        """Mostra il dialog delle informazioni."""
        self.ui_manager.show_about_dialog()
    
    def closeEvent(self, event):
        """Gestisce la chiusura dell'applicazione."""
        # Ferma il worker thread
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.quit()
            self.worker_thread.wait()
        
        event.accept()


def main():
    """Funzione principale dell'applicazione."""
    # Crea l'applicazione Qt
    app = QApplication(sys.argv)
    
    # Imposta informazioni applicazione
    app.setApplicationName("PDF Tools")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("Alessandro Castaldi")
    app.setOrganizationDomain("unpoditutto.info")
    
    # Imposta l'icona dell'applicazione (se disponibile)
    # app.setWindowIcon(QIcon("icons/app_icon.ico"))
    
    # Crea e mostra la finestra principale
    window = PDFToolsApplication()
    window.show()
    
    # Avvia l'event loop
    sys.exit(app.exec())


if __name__ == '__main__':
    main()