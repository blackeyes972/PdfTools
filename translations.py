# translations.py
"""
Modulo per la gestione delle traduzioni multilingua dell'applicazione PDF Tools.
Supporta italiano e inglese con possibilità di aggiungere altre lingue.
"""

class Translations:
    """Gestisce le traduzioni per l'applicazione."""
    
    def __init__(self, language='it'):
        self.language = language
        self.translations = {
            'it': {
                # Titoli finestre
                'app_title': 'PDF Tools',
                'about_title': 'Informazioni',
                
                # Menu
                'file_menu': 'File',
                'help_menu': '?',
                'language_menu': 'Lingua',
                'tools_menu': 'Strumenti',
                
                # Azioni menu strumenti
                'open_output_folder': 'Apri Cartella Output',
                'output_statistics': 'Statistiche Output',
                'cleanup_old_files': 'Pulisci File Vecchi',
                'configure_output': 'Configura Directory Output',
                
                # Directory output
                'output_directory': 'Directory Output',
                'select_output_directory': 'Seleziona Directory Output',
                'output_directory_changed': 'Directory output cambiata: {}',
                'creating_output_structure': 'Creazione struttura directory...',
                'output_structure_created': 'Struttura directory creata.',
                
                # Statistiche
                'statistics_title': 'Statistiche File Output',
                'total_files': 'File totali: {}',
                'total_size': 'Dimensione totale: {} MB',
                'files_by_type': 'File per tipo',
                'cleanup_completed': 'Pulizia completata: {} file eliminati ({} MB liberati)',
                'tools_menu': 'Strumenti',
                
                # Azioni menu
                'browse': 'Sfoglia',
                'compress': 'Comprimi',
                'merge': 'Unisci',
                'protect': 'Proteggi',
                'remove_protection': 'Rimuovi Password',
                'add_watermark': 'Aggiungi Filigrana',
                'clear_fields': 'Cancella Campi',
                'exit': 'Esci',
                'about': 'Informazioni',
                'italian': 'Italiano',
                'english': 'English',
                
                # Labels
                'input_file': 'File di input',
                'output_file': 'Nome file output',
                'output_directory': 'Directory di Output',
                'password': 'Password',
                'watermark': 'Filigrana',
                
                # Bottoni
                'browse_btn': 'Sfoglia',
                'compress_btn': 'Comprimi',
                'merge_btn': 'Unisci',
                'protect_btn': 'Proteggi',
                'remove_protection_btn': 'Rimuovi Password',
                'watermark_btn': 'Filigrana',
                'clear_btn': 'Cancella Campi',
                
                # Messaggi
                'ready': 'Pronto...',
                'file_selected': 'File selezionato: {}',
                'success': 'Successo',
                'error': 'Errore',
                'warning': 'Attenzione',
                
                # Errori e avvisi
                'no_file_selected': 'Seleziona un file PDF.',
                'no_files_selected': 'Seleziona almeno un file PDF da unire.',
                'no_output_name': 'Specifica un nome per il file di output.',
                'no_password': 'Specifica una password.',
                'no_watermark_text': 'Specifica un testo per la filigrana.',
                
                # Successi
                'compressed_success': 'PDF compresso e salvato in "{}".',
                'merged_success': 'PDF unito e salvato in "{}".',
                'protected_success': 'PDF protetto e salvato in "{}".',
                'unprotected_success': 'Protezione rimossa e salvato in "{}".',
                'watermark_success': 'Filigrana aggiunta e salvato in "{}".',
                
                # Errori operazioni
                'compression_error': 'Errore durante la compressione: {}',
                'merge_error': 'Errore durante l\'unione: {}',
                'protection_error': 'Errore durante la protezione: {}',
                'unprotection_error': 'Errore durante la rimozione protezione: {}',
                'watermark_error': 'Errore durante l\'aggiunta filigrana: {}',
                
                # Temi
                'theme_menu': 'Tema',
                'light_theme': 'Chiaro Professionale',
                'dark_theme': 'Scuro Professionale', 
                'blue_theme': 'Blu Aziendale',
                
                # Messaggi operazioni
                'compressing': 'Compressione in corso...',
                'merging': 'Unione in corso...',
                'protecting': 'Protezione in corso...',
                'removing_protection': 'Rimozione protezione...',
                'adding_watermark': 'Aggiunta filigrana...',
                'operation_completed': 'Operazione completata.',
                'operation_failed': 'Operazione fallita',
                'fields_cleared': 'Campi cancellati.',
                
                # Dialog file
                'select_pdf': 'Seleziona file PDF',
                'select_pdfs_to_merge': 'Seleziona PDF da unire',
                'save_merged_pdf': 'Salva PDF unito',
                'file_not_found': 'File non trovato.',
                'invalid_pdf': 'File PDF non valido.',
                'input_file_placeholder': 'Seleziona un file PDF...',
                'output_file_placeholder': 'Nome file output...',
                'output_directory_placeholder': 'I file verranno salvati automaticamente nella directory output...',
                'password_placeholder': 'Inserisci password...',
                'watermark_placeholder': 'Inserisci testo filigrana...',
                'opening_output_folder': 'Apertura cartella output...',
                
                # About dialog
                'about_text': '''
                <h2 style="color: #0078d4; text-align: center;">PDF Tools</h2>
                <p><b>Versione:</b> 2.0.0 Professional</p>
                <p><b>Descrizione:</b> Applicazione professionale per la gestione dei file PDF con interfaccia moderna e temi personalizzabili.</p>
                
                <h3 style="color: #0078d4;">Funzionalità:</h3>
                <ul>
                <li>🗜️ Compressione PDF avanzata per ridurre le dimensioni</li>
                <li>🔗 Unione di più file PDF</li>
                <li>🔒 Protezione con password sicura</li>
                <li>🔓 Rimozione protezione</li>
                <li>🖋️ Aggiunta filigrane personalizzate</li>
                <li>🎨 Tre temi professionali (Chiaro, Scuro, Blu)</li>
                <li>🌐 Interfaccia multilingua (IT/EN)</li>
                </ul>
                
                <p><b>Sviluppato da:</b> Alessandro Castaldi</p>
                <p><b>Email:</b> notifiche72@gmail.com</p>
                <p><b>Sito web:</b> https://unpoditutto.info/</p>
                
                <p style="text-align: center;"><i>Copyright © 2025 Alessandro Castaldi. Tutti i diritti riservati.</i></p>
                '''
            },
            'en': {
                # Window titles
                'app_title': 'PDF Tools',
                'about_title': 'About',
                
                # Menu
                'file_menu': 'File',
                'help_menu': 'Help',
                'language_menu': 'Language',
                'tools_menu': 'Tools',
                
                # Tools menu actions
                'open_output_folder': 'Open Output Folder',
                'output_statistics': 'Output Statistics',
                'cleanup_old_files': 'Cleanup Old Files',
                'configure_output': 'Configure Output Directory',
                
                # Output directory
                'output_directory': 'Output Directory',
                'select_output_directory': 'Select Output Directory',
                'output_directory_changed': 'Output directory changed: {}',
                'creating_output_structure': 'Creating directory structure...',
                'output_structure_created': 'Directory structure created.',
                
                # Statistics
                'statistics_title': 'Output Files Statistics',
                'total_files': 'Total files: {}',
                'total_size': 'Total size: {} MB',
                'files_by_type': 'Files by type',
                'cleanup_completed': 'Cleanup completed: {} files deleted ({} MB freed)',
                
                # Menu actions
                'browse': 'Browse',
                'compress': 'Compress',
                'merge': 'Merge',
                'protect': 'Protect',
                'remove_protection': 'Remove Password',
                'add_watermark': 'Add Watermark',
                'clear_fields': 'Clear Fields',
                'exit': 'Exit',
                'about': 'About',
                'italian': 'Italiano',
                'english': 'English',
                
                # Labels
                'input_file': 'Input File',
                'output_file': 'Output filename',
                'output_directory': 'Output Directory',
                'password': 'Password',
                'watermark': 'Watermark',
                
                # Buttons
                'browse_btn': 'Browse',
                'compress_btn': 'Compress',
                'merge_btn': 'Merge',
                'protect_btn': 'Protect',
                'remove_protection_btn': 'Remove Password',
                'watermark_btn': 'Watermark',
                'clear_btn': 'Clear Fields',
                
                # Messages
                'ready': 'Ready...',
                'file_selected': 'File selected: {}',
                'success': 'Success',
                'error': 'Error',
                'warning': 'Warning',
                
                # Errors and warnings
                'no_file_selected': 'Select a PDF file.',
                'no_files_selected': 'Select at least one PDF file to merge.',
                'no_output_name': 'Specify a name for the output file.',
                'no_password': 'Specify a password.',
                'no_watermark_text': 'Specify watermark text.',
                
                # Success messages
                'compressed_success': 'PDF compressed and saved as "{}".',
                'merged_success': 'PDF merged and saved as "{}".',
                'protected_success': 'PDF protected and saved as "{}".',
                'unprotected_success': 'Protection removed and saved as "{}".',
                'watermark_success': 'Watermark added and saved as "{}".',
                
                # Operation errors
                'compression_error': 'Error during compression: {}',
                'merge_error': 'Error during merge: {}',
                'protection_error': 'Error during protection: {}',
                'unprotection_error': 'Error during protection removal: {}',
                'watermark_error': 'Error during watermark addition: {}',
                
                # Themes
                'theme_menu': 'Theme',
                'light_theme': 'Light Professional',
                'dark_theme': 'Dark Professional',
                'blue_theme': 'Corporate Blue',
                
                # Operation messages
                'compressing': 'Compressing...',
                'merging': 'Merging...',
                'protecting': 'Protecting...',
                'removing_protection': 'Removing protection...',
                'adding_watermark': 'Adding watermark...',
                'operation_completed': 'Operation completed.',
                'operation_failed': 'Operation failed',
                'fields_cleared': 'Fields cleared.',
                
                # File dialogs
                'select_pdf': 'Select PDF file',
                'select_pdfs_to_merge': 'Select PDFs to merge',
                'save_merged_pdf': 'Save merged PDF',
                'file_not_found': 'File not found.',
                'invalid_pdf': 'Invalid PDF file.',
                'input_file_placeholder': 'Select a PDF file...',
                'output_file_placeholder': 'Output filename...',
                'output_directory_placeholder': 'Files will be automatically saved in output directory...',
                'password_placeholder': 'Enter password...',
                'watermark_placeholder': 'Enter watermark text...',
                'opening_output_folder': 'Opening output folder...',
                
                # About dialog
                'about_text': '''
                <h2 style="color: #0078d4; text-align: center;">PDF Tools</h2>
                <p><b>Version:</b> 2.0.0 Professional</p>
                <p><b>Description:</b> Professional application for PDF file management with modern interface and customizable themes.</p>
                
                <h3 style="color: #0078d4;">Features:</h3>
                <ul>
                <li>🗜️ Advanced PDF compression to reduce file size</li>
                <li>🔗 Merge multiple PDF files</li>
                <li>🔒 Secure password protection</li>
                <li>🔓 Remove protection</li>
                <li>🖋️ Add custom watermarks</li>
                <li>🎨 Three professional themes (Light, Dark, Blue)</li>
                <li>🌐 Multilingual interface (IT/EN)</li>
                </ul>
                
                <p><b>Developed by:</b> Alessandro Castaldi</p>
                <p><b>Email:</b> notifiche72@gmail.com</p>
                <p><b>Website:</b> https://unpoditutto.info/</p>
                
                <p style="text-align: center;"><i>Copyright © 2025 Alessandro Castaldi. All rights reserved.</i></p>
                '''
            }
        }
    
    def get(self, key, *args):
        """
        Ottiene una traduzione per la chiave specificata.
        
        Args:
            key (str): Chiave della traduzione
            *args: Argomenti per la formattazione della stringa
            
        Returns:
            str: Testo tradotto
        """
        text = self.translations.get(self.language, {}).get(key, key)
        if args:
            return text.format(*args)
        return text
    
    def set_language(self, language):
        """
        Imposta la lingua dell'applicazione.
        
        Args:
            language (str): Codice lingua ('it' o 'en')
        """
        if language in self.translations:
            self.language = language
    
    def get_available_languages(self):
        """
        Restituisce le lingue disponibili.
        
        Returns:
            list: Lista delle lingue disponibili
        """
        return list(self.translations.keys())