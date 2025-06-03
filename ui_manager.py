# ui_manager.py (AGGIORNATO)
"""
UI Manager aggiornato con supporto temi e toolbar professionale.
Interfaccia moderna, responsiva e completamente tematizzabile.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QStatusBar, QFrame,
    QGroupBox, QSizePolicy, QSpacerItem, QDialog, QTextEdit,
    QToolBar, QToolButton
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QPalette, QColor, QAction, QIcon
from theme_manager import ThemeManager, ThemeVariant


class ModernToolButton(QToolButton):
    """Bottone toolbar con stile moderno e personalizzabile."""
    
    def __init__(self, text, primary=False, parent=None):
        super().__init__(parent)
        self.primary = primary
        self.setText(text)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        self.setAutoRaise(True)
        self.setMinimumSize(QSize(100, 40))
        
        if primary:
            self.setProperty("primary", "true")


class AboutDialog(QDialog):
    """Dialog moderno per le informazioni sull'applicazione con supporto temi."""
    
    def __init__(self, translations=None, theme_manager=None, parent=None):
        super().__init__(parent)
        self.translations = translations
        self.theme_manager = theme_manager
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Configura l'interfaccia del dialog."""
        self.setWindowTitle(self._get_text('about_title'))
        self.setFixedSize(550, 450)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Titolo principale
        title_label = QLabel("PDF Tools")
        title_label.setProperty("header", "true")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Area di testo per le informazioni
        text_area = QTextEdit(self)
        text_area.setHtml(self._get_text('about_text'))
        text_area.setReadOnly(True)
        text_area.setMaximumHeight(280)
        
        # Bottone chiudi
        close_button = QPushButton(self._get_text('close') if self.translations else 'Close')
        close_button.clicked.connect(self.accept)
        close_button.setMinimumWidth(120)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        
        layout.addWidget(title_label)
        layout.addWidget(text_area)
        layout.addLayout(button_layout)
    
    def apply_theme(self):
        """Applica il tema corrente al dialog."""
        if self.theme_manager:
            self.setStyleSheet(
                self.theme_manager.get_dialog_style() +
                self.theme_manager.get_button_style(primary=True) +
                self.theme_manager.get_label_style()
            )
    
    def _get_text(self, key):
        """Helper per ottenere testo tradotto."""
        if self.translations:
            return self.translations.get(key)
        return key


class UIManager:
    """
    Gestisce la creazione e l'aggiornamento dell'interfaccia utente principale
    con supporto temi e toolbar professionale.
    """
    
    def __init__(self, main_window, translations=None, theme_manager=None):
        """
        Inizializza l'UI Manager.
        
        Args:
            main_window: Finestra principale dell'applicazione
            translations: Oggetto traduzioni
            theme_manager: Gestore temi
        """
        self.main_window = main_window
        self.translations = translations
        self.theme_manager = theme_manager or ThemeManager()
        
        # Riferimenti ai widgets
        self.widgets = {}
        self.layouts = {}
        
        # Toolbar e status bar
        self.toolbar = None
        self.status_bar = None
        
        # Connetti il cambio tema
        self.theme_manager.theme_changed.connect(self.apply_current_theme)
        
    def setup_main_window(self):
        """Configura la finestra principale con il nuovo design."""
        self.main_window.setWindowTitle(self._get_text('app_title'))
        self.main_window.setMinimumSize(1000, 700)
        self.main_window.resize(1200, 800)
        
        # Crea la toolbar
        self._create_toolbar()
        
        # Crea il widget centrale
        central_widget = QWidget()
        self.main_window.setCentralWidget(central_widget)
        
        # Layout principale
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Crea le sezioni dell'interfaccia
        self._create_file_section(main_layout)
        self._create_options_section(main_layout)
        
        # Aggiungi spazio flessibile
        main_layout.addStretch()
        
        # Status bar
        self._create_status_bar()
        
        # Applica il tema iniziale
        self.apply_current_theme()
        
    def _create_toolbar(self):
        """Crea la toolbar professionale."""
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        
        # Bottone sfoglia
        self.widgets['browse_btn'] = ModernToolButton(self._get_text('browse_btn'))
        self.toolbar.addWidget(self.widgets['browse_btn'])
        
        self.toolbar.addSeparator()
        
        # Bottone comprimi (primario)
        self.widgets['compress_btn'] = ModernToolButton(self._get_text('compress_btn'), primary=True)
        self.toolbar.addWidget(self.widgets['compress_btn'])
        
        # Altri bottoni
        self.widgets['merge_btn'] = ModernToolButton(self._get_text('merge_btn'))
        self.toolbar.addWidget(self.widgets['merge_btn'])
        
        self.widgets['protect_btn'] = ModernToolButton(self._get_text('protect_btn'))
        self.toolbar.addWidget(self.widgets['protect_btn'])
        
        self.toolbar.addSeparator()
        
        self.widgets['remove_protection_btn'] = ModernToolButton(self._get_text('remove_protection_btn'))
        self.toolbar.addWidget(self.widgets['remove_protection_btn'])
        
        self.widgets['watermark_btn'] = ModernToolButton(self._get_text('watermark_btn'))
        self.toolbar.addWidget(self.widgets['watermark_btn'])
        
        self.toolbar.addSeparator()
        
        # Bottone cancella campi
        self.widgets['clear_btn'] = ModernToolButton(self._get_text('clear_btn'))
        self.toolbar.addWidget(self.widgets['clear_btn'])
        
        # Aggiungi la toolbar alla finestra
        self.main_window.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)
        
    def _create_file_section(self, parent_layout):
        """Crea la sezione per la selezione dei file con design migliorato."""
        file_group = QGroupBox(self._get_text('file_selection'))
        
        file_layout = QGridLayout(file_group)
        file_layout.setSpacing(20)
        file_layout.setContentsMargins(30, 35, 30, 30)
        
        # Input file con icona
        input_label = QLabel(self._get_text('input_file'))
        self.widgets['input_file'] = QLineEdit()
        self.widgets['input_file'].setPlaceholderText(self._get_text('input_file_placeholder'))
        
        file_layout.addWidget(input_label, 0, 0)
        file_layout.addWidget(self.widgets['input_file'], 0, 1)
        
        # Output directory info (non più editabile)
        output_label = QLabel(self._get_text('output_directory'))
        self.widgets['output_file'] = QLineEdit()
        self.widgets['output_file'].setPlaceholderText(self._get_text('output_directory_placeholder'))
        self.widgets['output_file'].setReadOnly(True)
        # Rimuoviamo lo stile inline, sarà gestito dal theme manager
        
        file_layout.addWidget(output_label, 1, 0)
        file_layout.addWidget(self.widgets['output_file'], 1, 1)
        
        # Configura il layout delle colonne
        file_layout.setColumnStretch(1, 1)
        file_layout.setColumnMinimumWidth(0, 150)
        
        parent_layout.addWidget(file_group)
    
    def _create_options_section(self, parent_layout):
        """Crea la sezione per le opzioni con design migliorato."""
        options_group = QGroupBox(self._get_text('options'))
        
        options_layout = QGridLayout(options_group)
        options_layout.setSpacing(20)
        options_layout.setContentsMargins(30, 35, 30, 30)
        
        # Password
        password_label = QLabel(self._get_text('password'))
        self.widgets['password'] = QLineEdit()
        self.widgets['password'].setPlaceholderText(self._get_text('password_placeholder'))
        self.widgets['password'].setEchoMode(QLineEdit.EchoMode.Password)
        
        options_layout.addWidget(password_label, 0, 0)
        options_layout.addWidget(self.widgets['password'], 0, 1)
        
        # Watermark
        watermark_label = QLabel(self._get_text('watermark'))
        self.widgets['watermark'] = QLineEdit()
        self.widgets['watermark'].setPlaceholderText(self._get_text('watermark_placeholder'))
        
        options_layout.addWidget(watermark_label, 1, 0)
        options_layout.addWidget(self.widgets['watermark'], 1, 1)
        
        # Configura il layout delle colonne
        options_layout.setColumnStretch(1, 1)
        options_layout.setColumnMinimumWidth(0, 150)
        
        parent_layout.addWidget(options_group)
        
    def _create_status_bar(self):
        """Crea la status bar con design moderno."""
        self.status_bar = QStatusBar()
        self.main_window.setStatusBar(self.status_bar)
        self.show_status_message(self._get_text('ready'))
    
    def apply_current_theme(self):
        """Applica il tema corrente a tutti i componenti."""
        if not self.theme_manager:
            return
            
        # Applica stili ai componenti
        style_sheet = (
            self.theme_manager.get_main_window_style() +
            self.theme_manager.get_toolbar_style() +
            self.theme_manager.get_groupbox_style() +
            self.theme_manager.get_lineedit_style() +
            self.theme_manager.get_label_style() +
            self.theme_manager.get_statusbar_style() +
            self.theme_manager.get_menu_style()
        )
        
        self.main_window.setStyleSheet(style_sheet)
        
        # Applica il tema all'applicazione
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            self.theme_manager.apply_theme_to_application(app)
    
    def get_widget(self, name):
        """
        Ottiene un widget per nome.
        
        Args:
            name (str): Nome del widget
            
        Returns:
            QWidget: Il widget richiesto o None
        """
        return self.widgets.get(name)
    
    def get_input_file_path(self):
        """Ottiene il percorso del file di input."""
        return self.widgets['input_file'].text().strip()
    
    def set_input_file_path(self, path):
        """Imposta il percorso del file di input."""
        self.widgets['input_file'].setText(path)
    
    def get_output_file_path(self):
        """Ottiene il percorso del file di output."""
        return self.widgets['output_file'].text().strip()
    
    def set_output_file_path(self, path):
        """Imposta il percorso del file di output."""
        self.widgets['output_file'].setText(path)
    
    def get_password(self):
        """Ottiene la password."""
        return self.widgets['password'].text()
    
    def clear_password(self):
        """Pulisce il campo password."""
        self.widgets['password'].clear()
    
    def get_watermark_text(self):
        """Ottiene il testo della filigrana."""
        return self.widgets['watermark'].text().strip()
    
    def clear_watermark(self):
        """Pulisce il campo filigrana."""
        self.widgets['watermark'].clear()
    
    def clear_all_fields(self):
        """Pulisce tutti i campi del form."""
        self.widgets['input_file'].clear()
        self.widgets['output_file'].clear()
        self.widgets['password'].clear()
        self.widgets['watermark'].clear()
    
    def show_status_message(self, message, timeout=0):
        """
        Mostra un messaggio nella status bar.
        
        Args:
            message (str): Messaggio da mostrare
            timeout (int): Timeout in millisecondi (0 = permanente)
        """
        if self.status_bar:
            self.status_bar.showMessage(message, timeout)
    
    def enable_toolbar_buttons(self, enabled=True):
        """
        Abilita o disabilita tutti i bottoni della toolbar.
        
        Args:
            enabled (bool): True per abilitare, False per disabilitare
        """
        button_names = [
            'compress_btn', 'merge_btn', 'protect_btn',
            'remove_protection_btn', 'watermark_btn', 'clear_btn'
        ]
        
        for btn_name in button_names:
            if btn_name in self.widgets:
                self.widgets[btn_name].setEnabled(enabled)
    
    def update_translations(self):
        """Aggiorna tutti i testi dell'interfaccia con le nuove traduzioni."""
        # Aggiorna il titolo della finestra
        self.main_window.setWindowTitle(self._get_text('app_title'))
        
        # Aggiorna placeholder text
        if 'input_file' in self.widgets:
            self.widgets['input_file'].setPlaceholderText(self._get_text('input_file_placeholder'))
        if 'output_file' in self.widgets:
            self.widgets['output_file'].setPlaceholderText(self._get_text('output_directory_placeholder'))
        if 'password' in self.widgets:
            self.widgets['password'].setPlaceholderText(self._get_text('password_placeholder'))
        if 'watermark' in self.widgets:
            self.widgets['watermark'].setPlaceholderText(self._get_text('watermark_placeholder'))
        
        # Aggiorna testi dei bottoni della toolbar
        button_text_map = {
            'browse_btn': 'browse_btn',
            'compress_btn': 'compress_btn',
            'merge_btn': 'merge_btn',
            'protect_btn': 'protect_btn',
            'remove_protection_btn': 'remove_protection_btn',
            'watermark_btn': 'watermark_btn',
            'clear_btn': 'clear_btn'
        }
        
        for widget_name, text_key in button_text_map.items():
            if widget_name in self.widgets:
                self.widgets[widget_name].setText(self._get_text(text_key))
        
        # Aggiorna status bar
        self.show_status_message(self._get_text('ready'))
    
    def show_about_dialog(self):
        """Mostra il dialog delle informazioni con tema applicato."""
        dialog = AboutDialog(self.translations, self.theme_manager, self.main_window)
        dialog.exec()
    
    def set_theme(self, theme_variant):
        """
        Cambia il tema dell'interfaccia.
        
        Args:
            theme_variant (ThemeVariant): Nuova variante del tema
        """
        if self.theme_manager:
            self.theme_manager.set_theme(theme_variant)
    
    def get_current_theme(self):
        """Restituisce la variante del tema corrente."""
        if self.theme_manager:
            return self.theme_manager.current_theme
        return ThemeVariant.LIGHT
    
    def _get_text(self, key):
        """Helper per ottenere testo tradotto."""
        if self.translations:
            return self.translations.get(key)
        
        # Testi di fallback in inglese
        fallback_texts = {
            'app_title': 'PDF Tools',
            'file_selection': 'File Selection',
            'options': 'Options',
            'input_file': 'Input File:',
            'output_file': 'Output File:',
            'output_directory': 'Output Directory:',
            'password': 'Password:',
            'watermark': 'Watermark:',
            'input_file_placeholder': 'Select a PDF file...',
            'output_file_placeholder': 'Output filename...',
            'output_directory_placeholder': 'Files will be automatically saved in output directory...',
            'password_placeholder': 'Enter password...',
            'watermark_placeholder': 'Enter watermark text...',
            'browse_btn': 'Browse',
            'compress_btn': 'Compress',
            'merge_btn': 'Merge',
            'protect_btn': 'Protect',
            'remove_protection_btn': 'Remove Password',
            'watermark_btn': 'Add Watermark',
            'clear_btn': 'Clear Fields',
            'ready': 'Ready...',
            'about_title': 'About',
            'close': 'Close'
        }
        
        return fallback_texts.get(key, key)