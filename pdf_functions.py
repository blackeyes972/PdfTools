# pdf_functions.py
"""
Modulo contenente tutte le funzioni per la manipolazione dei file PDF.
Questo modulo è completamente indipendente dall'interfaccia utente.
Integrato con OutputManager per gestione professionale dei file di output.
"""

import os
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
import pikepdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from output_manager import OutputManager, OutputType


class PDFProcessor:
    """Classe che gestisce tutte le operazioni sui file PDF con gestione output professionale."""
    
    def __init__(self, output_manager=None):
        """
        Inizializza il PDFProcessor.
        
        Args:
            output_manager (OutputManager): Gestore output personalizzato (opzionale)
        """
        self.output_manager = output_manager or OutputManager()
    
    @staticmethod
    def validate_file_exists(file_path):
        """
        Verifica che il file esista.
        
        Args:
            file_path (str): Percorso del file
            
        Returns:
            bool: True se il file esiste, False altrimenti
        """
        return os.path.exists(file_path) and os.path.isfile(file_path)
    
    @staticmethod
    def ensure_pdf_extension(filename):
        """
        Assicura che il filename abbia l'estensione .pdf
        
        Args:
            filename (str): Nome del file
            
        Returns:
            str: Nome del file con estensione .pdf
        """
        if not filename.lower().endswith('.pdf'):
            return filename + '.pdf'
        return filename
    
    def compress_pdf(self, input_file, output_file=None):
        """
        Comprime un PDF utilizzando pikepdf per una compressione reale.
        
        Args:
            input_file (str): Percorso del file PDF di input
            output_file (str): Nome del file di output (opzionale, auto-generato se None)
            
        Returns:
            str: Percorso del file compresso creato
            
        Raises:
            FileNotFoundError: Se il file di input non esiste
            Exception: Per altri errori durante la compressione
        """
        if not self.validate_file_exists(input_file):
            raise FileNotFoundError(f"File not found: {input_file}")
        
        # Genera automaticamente il percorso di output se non fornito
        if output_file is None:
            output_file = self.output_manager.get_output_path(
                input_file, 
                OutputType.COMPRESSED
            )
        else:
            # Se fornito un nome personalizzato, usalo con la directory appropriata
            output_file = self.output_manager.get_output_path(
                input_file,
                OutputType.COMPRESSED,
                custom_suffix=os.path.splitext(os.path.basename(output_file))[0]
            )
        
        try:
            with pikepdf.open(input_file) as pdf:
                pdf.save(output_file, compress_streams=True)
            
            return output_file
            
        except Exception as e:
            raise Exception(f"Compression failed: {str(e)}")
    
    def merge_pdfs(self, input_files, output_file=None):
        """
        Unisce più file PDF in un singolo file.
        
        Args:
            input_files (list): Lista dei percorsi dei file PDF da unire
            output_file (str): Nome del file di output (opzionale, auto-generato se None)
            
        Returns:
            str: Percorso del file unito creato
            
        Raises:
            ValueError: Se la lista dei file è vuota
            FileNotFoundError: Se uno dei file di input non esiste
            Exception: Per altri errori durante l'unione
        """
        if not input_files:
            raise ValueError("No input files provided")
        
        # Verifica che tutti i file esistano
        for file_path in input_files:
            if not self.validate_file_exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
        
        # Genera automaticamente il percorso di output se non fornito
        if output_file is None:
            # Usa il primo file come base per il nome
            base_filename = input_files[0]
            suffix = f"merged_{len(input_files)}_files"
            output_file = self.output_manager.get_output_path(
                base_filename,
                OutputType.MERGED,
                custom_suffix=suffix
            )
        else:
            # Se fornito un nome personalizzato, usalo con la directory appropriata
            output_file = self.output_manager.get_output_path(
                input_files[0],
                OutputType.MERGED,
                custom_suffix=os.path.splitext(os.path.basename(output_file))[0]
            )
        
        try:
            writer = PdfWriter()
            
            for file_path in input_files:
                reader = PdfReader(file_path)
                for page in reader.pages:
                    writer.add_page(page)
            
            with open(output_file, 'wb') as out_file:
                writer.write(out_file)
            
            return output_file
                
        except Exception as e:
            raise Exception(f"Merge failed: {str(e)}")
    
    def protect_pdf(self, input_file, password, output_file=None):
        """
        Protegge un PDF con una password.
        
        Args:
            input_file (str): Percorso del file PDF di input
            password (str): Password per proteggere il PDF
            output_file (str): Nome del file di output (opzionale, auto-generato se None)
            
        Returns:
            str: Percorso del file protetto creato
            
        Raises:
            FileNotFoundError: Se il file di input non esiste
            ValueError: Se la password è vuota
            Exception: Per altri errori durante la protezione
        """
        if not self.validate_file_exists(input_file):
            raise FileNotFoundError(f"File not found: {input_file}")
        
        if not password or not password.strip():
            raise ValueError("Password cannot be empty")
        
        # Genera automaticamente il percorso di output se non fornito
        if output_file is None:
            output_file = self.output_manager.get_output_path(
                input_file,
                OutputType.PROTECTED
            )
        else:
            # Se fornito un nome personalizzato, usalo con la directory appropriata
            output_file = self.output_manager.get_output_path(
                input_file,
                OutputType.PROTECTED,
                custom_suffix=os.path.splitext(os.path.basename(output_file))[0]
            )
        
        try:
            with pikepdf.open(input_file) as pdf:
                pdf.save(
                    output_file, 
                    encryption=pikepdf.Encryption(
                        owner=password, 
                        user=password, 
                        R=4
                    )
                )
            
            return output_file
            
        except Exception as e:
            raise Exception(f"Protection failed: {str(e)}")
    
    def remove_protection(self, input_file, password, output_file=None):
        """
        Rimuove la protezione da un PDF.
        
        Args:
            input_file (str): Percorso del file PDF protetto
            password (str): Password per rimuovere la protezione
            output_file (str): Nome del file di output (opzionale, auto-generato se None)
            
        Returns:
            str: Percorso del file sprotetto creato
            
        Raises:
            FileNotFoundError: Se il file di input non esiste
            ValueError: Se la password è vuota
            Exception: Per altri errori durante la rimozione protezione
        """
        if not self.validate_file_exists(input_file):
            raise FileNotFoundError(f"File not found: {input_file}")
        
        if not password or not password.strip():
            raise ValueError("Password cannot be empty")
        
        # Genera automaticamente il percorso di output se non fornito
        if output_file is None:
            output_file = self.output_manager.get_output_path(
                input_file,
                OutputType.UNPROTECTED
            )
        else:
            # Se fornito un nome personalizzato, usalo con la directory appropriata
            output_file = self.output_manager.get_output_path(
                input_file,
                OutputType.UNPROTECTED,
                custom_suffix=os.path.splitext(os.path.basename(output_file))[0]
            )
        
        try:
            with pikepdf.open(input_file, password=password) as pdf:
                pdf.save(output_file)
            
            return output_file
            
        except Exception as e:
            raise Exception(f"Protection removal failed: {str(e)}")
    
    def add_watermark(self, input_file, watermark_text, output_file=None,
                     font_size=40, opacity=0.3, rotation=45):
        """
        Aggiunge una filigrana a tutte le pagine di un PDF.
        
        Args:
            input_file (str): Percorso del file PDF di input
            watermark_text (str): Testo della filigrana
            output_file (str): Nome del file di output (opzionale, auto-generato se None)
            font_size (int): Dimensione del font (default: 40)
            opacity (float): Opacità della filigrana (0.0-1.0, default: 0.3)
            rotation (int): Rotazione in gradi (default: 45)
            
        Returns:
            str: Percorso del file con filigrana creato
            
        Raises:
            FileNotFoundError: Se il file di input non esiste
            ValueError: Se il testo della filigrana è vuoto
            Exception: Per altri errori durante l'aggiunta della filigrana
        """
        if not self.validate_file_exists(input_file):
            raise FileNotFoundError(f"File not found: {input_file}")
        
        if not watermark_text or not watermark_text.strip():
            raise ValueError("Watermark text cannot be empty")
        
        # Genera automaticamente il percorso di output se non fornito
        if output_file is None:
            # Usa una parte del testo della filigrana come suffisso (primi 10 caratteri)
            watermark_suffix = "".join(c for c in watermark_text[:10] if c.isalnum()).lower()
            output_file = self.output_manager.get_output_path(
                input_file,
                OutputType.WATERMARKED,
                custom_suffix=f"wm_{watermark_suffix}" if watermark_suffix else None
            )
        else:
            # Se fornito un nome personalizzato, usalo con la directory appropriata
            output_file = self.output_manager.get_output_path(
                input_file,
                OutputType.WATERMARKED,
                custom_suffix=os.path.splitext(os.path.basename(output_file))[0]
            )
        
        try:
            reader = PdfReader(input_file)
            writer = PdfWriter()
            
            # Crea la filigrana come PDF
            watermark_pdf = self._create_watermark_pdf(
                watermark_text, font_size, opacity, rotation
            )
            watermark_page = watermark_pdf.pages[0]
            
            # Applica la filigrana a tutte le pagine
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                page.merge_page(watermark_page)
                writer.add_page(page)
            
            with open(output_file, 'wb') as out_file:
                writer.write(out_file)
            
            return output_file
                
        except Exception as e:
            raise Exception(f"Watermark addition failed: {str(e)}")
    
    @staticmethod
    def _create_watermark_pdf(text, font_size, opacity, rotation):
        """
        Crea un PDF contenente solo la filigrana.
        
        Args:
            text (str): Testo della filigrana
            font_size (int): Dimensione del font
            opacity (float): Opacità
            rotation (int): Rotazione in gradi
            
        Returns:
            PdfReader: Reader del PDF contenente la filigrana
        """
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        
        # Configura il font e il colore
        can.setFont("Helvetica", font_size)
        can.setFillColorRGB(0.6, 0.6, 0.6, alpha=opacity)
        
        # Applica la trasformazione (posizione e rotazione)
        can.saveState()
        can.translate(300, 500)  # Centro della pagina approssimativo
        can.rotate(rotation)
        can.drawCentredString(0, 0, text)
        can.restoreState()
        can.save()
        
        packet.seek(0)
        return PdfReader(packet)
    
    def batch_process_directory(self, input_directory, operation, **kwargs):
        """
        Elabora tutti i PDF in una directory con l'operazione specificata.
        
        Args:
            input_directory (str): Directory contenente i PDF da elaborare
            operation (str): Tipo di operazione ('compress', 'watermark', 'protect')
            **kwargs: Parametri specifici per l'operazione
            
        Returns:
            dict: Risultati dell'elaborazione batch
        """
        if not os.path.exists(input_directory):
            raise FileNotFoundError(f"Directory not found: {input_directory}")
        
        # Trova tutti i file PDF nella directory
        pdf_files = []
        for filename in os.listdir(input_directory):
            if filename.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(input_directory, filename))
        
        if not pdf_files:
            raise ValueError("No PDF files found in directory")
        
        # Crea directory di output per il batch
        output_type_map = {
            'compress': OutputType.COMPRESSED,
            'watermark': OutputType.WATERMARKED,
            'protect': OutputType.PROTECTED,
            'remove_protection': OutputType.UNPROTECTED
        }
        
        output_type = output_type_map.get(operation, OutputType.COMPRESSED)
        batch_dir = self.output_manager.get_batch_output_directory(output_type)
        
        results = {
            'total_files': len(pdf_files),
            'processed_files': 0,
            'failed_files': 0,
            'output_directory': batch_dir,
            'processed_list': [],
            'failed_list': []
        }
        
        for input_file in pdf_files:
            try:
                filename = os.path.basename(input_file)
                output_file = os.path.join(batch_dir, filename)
                
                if operation == 'compress':
                    processed_file = self.compress_pdf(input_file, output_file)
                elif operation == 'watermark':
                    watermark_text = kwargs.get('watermark_text', 'PROCESSED')
                    processed_file = self.add_watermark(input_file, watermark_text, output_file)
                elif operation == 'protect':
                    password = kwargs.get('password')
                    if not password:
                        raise ValueError("Password required for protection")
                    processed_file = self.protect_pdf(input_file, password, output_file)
                elif operation == 'remove_protection':
                    password = kwargs.get('password')
                    if not password:
                        raise ValueError("Password required for removing protection")
                    processed_file = self.remove_protection(input_file, password, output_file)
                else:
                    raise ValueError(f"Unknown operation: {operation}")
                
                results['processed_files'] += 1
                results['processed_list'].append({
                    'input_file': input_file,
                    'output_file': processed_file,
                    'status': 'success'
                })
                
            except Exception as e:
                results['failed_files'] += 1
                results['failed_list'].append({
                    'input_file': input_file,
                    'error': str(e),
                    'status': 'failed'
                })
        
        return results
    
    def get_output_manager(self):
        """Restituisce l'OutputManager corrente."""
        return self.output_manager
    
    def set_output_directory(self, directory):
        """
        Imposta una nuova directory di output.
        
        Args:
            directory (str): Nuova directory di output
        """
        self.output_manager.set_base_output_directory(directory)
    
    def get_output_statistics(self):
        """Restituisce statistiche sui file di output."""
        return self.output_manager.get_output_statistics()
    
    @staticmethod
    def get_pdf_info(file_path):
        """
        Ottiene informazioni di base su un file PDF.
        
        Args:
            file_path (str): Percorso del file PDF
            
        Returns:
            dict: Informazioni sul PDF (numero pagine, dimensione file, etc.)
            
        Raises:
            FileNotFoundError: Se il file non esiste
            Exception: Per errori durante la lettura
        """
        if not PDFProcessor.validate_file_exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                
                info = {
                    'num_pages': len(reader.pages),
                    'file_size': os.path.getsize(file_path),
                    'file_size_mb': round(os.path.getsize(file_path) / (1024 * 1024), 2),
                    'encrypted': reader.is_encrypted,
                    'title': reader.metadata.get('/Title', 'N/A') if reader.metadata else 'N/A',
                    'author': reader.metadata.get('/Author', 'N/A') if reader.metadata else 'N/A',
                    'subject': reader.metadata.get('/Subject', 'N/A') if reader.metadata else 'N/A',
                    'creator': reader.metadata.get('/Creator', 'N/A') if reader.metadata else 'N/A'
                }
                
                return info
                
        except Exception as e:
            raise Exception(f"Failed to read PDF info: {str(e)}")


class PDFValidator:
    """Classe per la validazione di file PDF e parametri."""
    
    @staticmethod
    def is_valid_pdf(file_path):
        """
        Verifica se un file è un PDF valido.
        
        Args:
            file_path (str): Percorso del file
            
        Returns:
            bool: True se è un PDF valido, False altrimenti
        """
        try:
            if not PDFProcessor.validate_file_exists(file_path):
                return False
            
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                # Prova a leggere la prima pagina
                if len(reader.pages) > 0:
                    return True
                return False
                
        except Exception:
            return False
    
    @staticmethod
    def validate_password_strength(password, min_length=4):
        """
        Valida la forza di una password.
        
        Args:
            password (str): Password da validare
            min_length (int): Lunghezza minima richiesta
            
        Returns:
            tuple: (is_valid, message)
        """
        if not password or len(password) < min_length:
            return False, f"Password must be at least {min_length} characters long"
        
        return True, "Password is valid"