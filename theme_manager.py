# theme_manager.py
"""
Sistema di gestione temi riutilizzabile per applicazioni PyQt6.
Supporta tre varianti di colore professionali e può essere utilizzato
in qualsiasi applicazione PyQt6.
"""

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from enum import Enum
import json
import os


class ThemeVariant(Enum):
    """Enumerazione delle varianti di tema disponibili."""
    LIGHT = "light"
    DARK = "dark"
    BLUE = "blue"


class ColorScheme:
    """Definisce uno schema di colori per un tema."""
    
    def __init__(self, name, colors):
        self.name = name
        self.primary = colors.get('primary', '#0078d4')
        self.primary_hover = colors.get('primary_hover', '#106ebe')
        self.primary_pressed = colors.get('primary_pressed', '#005a9e')
        self.secondary = colors.get('secondary', '#f3f2f1')
        self.secondary_hover = colors.get('secondary_hover', '#edebe9')
        self.secondary_pressed = colors.get('secondary_pressed', '#e1dfdd')
        self.background = colors.get('background', '#ffffff')
        self.surface = colors.get('surface', '#fafafa')
        self.surface_alt = colors.get('surface_alt', '#f5f5f5')
        self.border = colors.get('border', '#e1dfdd')
        self.border_hover = colors.get('border_hover', '#323130')
        self.text_primary = colors.get('text_primary', '#323130')
        self.text_secondary = colors.get('text_secondary', '#605e5c')
        self.text_disabled = colors.get('text_disabled', '#a19f9d')
        self.accent = colors.get('accent', '#107c10')
        self.warning = colors.get('warning', '#ff8c00')
        self.error = colors.get('error', '#d13438')
        self.success = colors.get('success', '#107c10')


class ThemeManager(QObject):
    """
    Gestisce i temi dell'applicazione e fornisce stili CSS.
    Completamente riutilizzabile in altre applicazioni PyQt6.
    """
    
    # Segnale emesso quando il tema cambia
    theme_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.current_theme = ThemeVariant.LIGHT
        self.themes = self._create_default_themes()
        self.settings_file = "theme_settings.json"
        self._load_saved_theme()
    
    def _create_default_themes(self):
        """Crea i temi di default professionali."""
        return {
            ThemeVariant.LIGHT: ColorScheme("Light Professional", {
                'primary': '#0078d4',
                'primary_hover': '#106ebe',
                'primary_pressed': '#005a9e',
                'secondary': '#f8f9fa',
                'secondary_hover': '#e9ecef',
                'secondary_pressed': '#dee2e6',
                'background': '#ffffff',
                'surface': '#f8f9fa',
                'surface_alt': '#e9ecef',
                'border': '#dee2e6',
                'border_hover': '#6c757d',
                'text_primary': '#212529',
                'text_secondary': '#6c757d',
                'text_disabled': '#adb5bd',
                'accent': '#20c997',
                'warning': '#ffc107',
                'error': '#dc3545',
                'success': '#28a745'
            }),
            
            ThemeVariant.DARK: ColorScheme("Dark Professional", {
                'primary': '#0d7377',
                'primary_hover': '#14a085',
                'primary_pressed': '#0a5d61',
                'secondary': '#2d3748',
                'secondary_hover': '#4a5568',
                'secondary_pressed': '#1a202c',
                'background': '#1a1a1a',
                'surface': '#2d3748',
                'surface_alt': '#4a5568',
                'border': '#4a5568',
                'border_hover': '#718096',
                'text_primary': '#f7fafc',
                'text_secondary': '#e2e8f0',
                'text_disabled': '#718096',
                'accent': '#38b2ac',
                'warning': '#ed8936',
                'error': '#f56565',
                'success': '#48bb78'
            }),
            
            ThemeVariant.BLUE: ColorScheme("Corporate Blue", {
                'primary': '#1e3a8a',
                'primary_hover': '#1e40af',
                'primary_pressed': '#1e3a8a',
                'secondary': '#eff6ff',
                'secondary_hover': '#dbeafe',
                'secondary_pressed': '#bfdbfe',
                'background': '#f8fafc',
                'surface': '#ffffff',
                'surface_alt': '#f1f5f9',
                'border': '#cbd5e1',
                'border_hover': '#475569',
                'text_primary': '#0f172a',
                'text_secondary': '#475569',
                'text_disabled': '#94a3b8',
                'accent': '#0ea5e9',
                'warning': '#f59e0b',
                'error': '#ef4444',
                'success': '#10b981'
            })
        }
    
    def get_current_theme(self):
        """Restituisce il tema corrente."""
        return self.themes[self.current_theme]
    
    def set_theme(self, theme_variant):
        """
        Imposta il tema corrente.
        
        Args:
            theme_variant (ThemeVariant): Variante del tema da applicare
        """
        if theme_variant in self.themes:
            self.current_theme = theme_variant
            self._save_theme()
            self.theme_changed.emit(theme_variant.value)
    
    def get_available_themes(self):
        """Restituisce lista delle varianti di tema disponibili."""
        return list(self.themes.keys())
    
    def get_theme_name(self, theme_variant):
        """Restituisce il nome di un tema."""
        return self.themes[theme_variant].name if theme_variant in self.themes else ""
    
    def _save_theme(self):
        """Salva il tema corrente nel file di configurazione."""
        try:
            settings = {'current_theme': self.current_theme.value}
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
        except Exception:
            pass  # Ignora errori di salvataggio
    
    def _load_saved_theme(self):
        """Carica il tema salvato dal file di configurazione."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    theme_value = settings.get('current_theme', 'light')
                    for variant in ThemeVariant:
                        if variant.value == theme_value:
                            self.current_theme = variant
                            break
        except Exception:
            pass  # Usa tema di default in caso di errore
    
    def get_main_window_style(self):
        """Restituisce lo stile CSS per la finestra principale."""
        theme = self.get_current_theme()
        return f"""
            QMainWindow {{
                background-color: {theme.background};
                color: {theme.text_primary};
            }}
            
            QMainWindow::separator {{
                background-color: {theme.border};
                width: 1px;
                height: 1px;
            }}
        """
    
    def get_toolbar_style(self):
        """Restituisce lo stile CSS per la toolbar."""
        theme = self.get_current_theme()
        return f"""
            QToolBar {{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 {theme.surface}, stop: 1 {theme.surface_alt});
                border: none;
                border-bottom: 2px solid {theme.border};
                spacing: 8px;
                padding: 8px 12px;
                font-weight: 500;
            }}
            
            QToolBar::separator {{
                background-color: {theme.border};
                width: 1px;
                margin: 4px 8px;
            }}
            
            QToolBar QToolButton {{
                background-color: transparent;
                border: 2px solid transparent;
                border-radius: 8px;
                padding: 8px 16px;
                margin: 2px;
                font-size: 11pt;
                font-weight: 500;
                color: {theme.text_primary};
                min-width: 80px;
                min-height: 32px;
            }}
            
            QToolBar QToolButton:hover {{
                background-color: {theme.secondary_hover};
                border-color: {theme.border_hover};
            }}
            
            QToolBar QToolButton:pressed {{
                background-color: {theme.secondary_pressed};
                border-color: {theme.primary};
            }}
            
            QToolBar QToolButton:disabled {{
                color: {theme.text_disabled};
                background-color: transparent;
                border-color: transparent;
            }}
            
            QToolBar QToolButton[primary="true"] {{
                background-color: {theme.primary};
                color: white;
                border-color: {theme.primary};
                font-weight: bold;
            }}
            
            QToolBar QToolButton[primary="true"]:hover {{
                background-color: {theme.primary_hover};
            }}
            
            QToolBar QToolButton[primary="true"]:pressed {{
                background-color: {theme.primary_pressed};
            }}
            
            QToolBar QToolButton[primary="true"]:disabled {{
                background-color: {theme.text_disabled};
                border-color: {theme.text_disabled};
            }}
        """
    
    def get_groupbox_style(self):
        """Restituisce lo stile CSS per i QGroupBox."""
        theme = self.get_current_theme()
        return f"""
            QGroupBox {{
                font-weight: 600;
                font-size: 12pt;
                border: 2px solid {theme.border};
                border-radius: 12px;
                margin: 15px 0px;
                padding-top: 20px;
                background-color: {theme.surface};
                color: {theme.text_primary};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 15px 0 15px;
                background-color: {theme.surface};
                color: {theme.primary};
                font-weight: bold;
            }}
        """
    
    def get_lineedit_style(self):
        """Restituisce lo stile CSS per i QLineEdit."""
        theme = self.get_current_theme()
        return f"""
            QLineEdit {{
                border: 2px solid {theme.border};
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 11pt;
                background-color: {theme.background};
                color: {theme.text_primary};
                selection-background-color: {theme.primary};
                selection-color: white;
            }}
            
            QLineEdit:focus {{
                border-color: {theme.primary};
                background-color: {theme.background};
            }}
            
            QLineEdit:disabled {{
                background-color: {theme.surface_alt};
                color: {theme.text_disabled};
                border-color: {theme.border};
            }}
            
            QLineEdit[readOnly="true"] {{
                background-color: {theme.surface_alt};
                color: {theme.text_secondary};
                border: 2px solid {theme.border};
                font-style: italic;
                border-radius: 8px;
                padding: 12px 16px;
            }}
            
            QLineEdit::placeholder {{
                color: {theme.text_secondary};
                font-style: italic;
            }}
        """
    
    def get_label_style(self):
        """Restituisce lo stile CSS per i QLabel."""
        theme = self.get_current_theme()
        return f"""
            QLabel {{
                color: {theme.text_primary};
                font-size: 11pt;
                font-weight: 500;
            }}
            
            QLabel[header="true"] {{
                font-size: 14pt;
                font-weight: bold;
                color: {theme.primary};
            }}
            
            QLabel:disabled {{
                color: {theme.text_disabled};
            }}
        """
    
    def get_statusbar_style(self):
        """Restituisce lo stile CSS per la status bar."""
        theme = self.get_current_theme()
        return f"""
            QStatusBar {{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 {theme.surface_alt}, stop: 1 {theme.surface});
                border-top: 1px solid {theme.border};
                padding: 8px 16px;
                font-size: 10pt;
                color: {theme.text_secondary};
            }}
            
            QStatusBar::item {{
                border: none;
            }}
        """
    
    def get_dialog_style(self):
        """Restituisce lo stile CSS per i dialog."""
        theme = self.get_current_theme()
        return f"""
            QDialog {{
                background-color: {theme.background};
                color: {theme.text_primary};
            }}
            
            QTextEdit {{
                border: 2px solid {theme.border};
                border-radius: 8px;
                background-color: {theme.surface};
                padding: 16px;
                font-size: 10pt;
                color: {theme.text_primary};
            }}
            
            QTextEdit:focus {{
                border-color: {theme.primary};
            }}
        """
    
    def get_button_style(self, primary=False):
        """
        Restituisce lo stile CSS per i bottoni.
        
        Args:
            primary (bool): Se True, restituisce lo stile per bottone primario
        """
        theme = self.get_current_theme()
        
        if primary:
            return f"""
                QPushButton {{
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 {theme.primary}, stop: 1 {theme.primary_pressed});
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 11pt;
                    padding: 12px 20px;
                    min-width: 100px;
                    min-height: 40px;
                }}
                
                QPushButton:hover {{
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 {theme.primary_hover}, stop: 1 {theme.primary});
                }}
                
                QPushButton:pressed {{
                    background-color: {theme.primary_pressed};
                }}
                
                QPushButton:disabled {{
                    background-color: {theme.text_disabled};
                    color: {theme.surface};
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 {theme.secondary}, stop: 1 {theme.secondary_hover});
                    color: {theme.text_primary};
                    border: 2px solid {theme.border};
                    border-radius: 8px;
                    font-size: 11pt;
                    font-weight: 500;
                    padding: 12px 20px;
                    min-width: 100px;
                    min-height: 40px;
                }}
                
                QPushButton:hover {{
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 {theme.secondary_hover}, stop: 1 {theme.secondary_pressed});
                    border-color: {theme.border_hover};
                }}
                
                QPushButton:pressed {{
                    background-color: {theme.secondary_pressed};
                    border-color: {theme.primary};
                }}
                
                QPushButton:disabled {{
                    background-color: {theme.surface_alt};
                    color: {theme.text_disabled};
                    border-color: {theme.border};
                }}
            """
    
    def get_menu_style(self):
        """Restituisce lo stile CSS per i menu."""
        theme = self.get_current_theme()
        return f"""
            QMenuBar {{
                background-color: {theme.surface};
                color: {theme.text_primary};
                border-bottom: 1px solid {theme.border};
                padding: 4px 8px;
                font-size: 11pt;
            }}
            
            QMenuBar::item {{
                background-color: transparent;
                padding: 8px 12px;
                border-radius: 4px;
            }}
            
            QMenuBar::item:selected {{
                background-color: {theme.secondary_hover};
                color: {theme.text_primary};
            }}
            
            QMenuBar::item:pressed {{
                background-color: {theme.secondary_pressed};
            }}
            
            QMenu {{
                background-color: {theme.background};
                border: 2px solid {theme.border};
                border-radius: 8px;
                padding: 8px 0px;
                color: {theme.text_primary};
            }}
            
            QMenu::item {{
                padding: 8px 20px;
                background-color: transparent;
            }}
            
            QMenu::item:selected {{
                background-color: {theme.secondary_hover};
                color: {theme.text_primary};
            }}
            
            QMenu::separator {{
                height: 1px;
                background-color: {theme.border};
                margin: 4px 12px;
            }}
        """
    
    def apply_theme_to_application(self, app):
        """
        Applica il tema all'intera applicazione.
        
        Args:
            app (QApplication): Istanza dell'applicazione
        """
        theme = self.get_current_theme()
        
        # Imposta palette dell'applicazione
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(theme.background))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(theme.text_primary))
        palette.setColor(QPalette.ColorRole.Base, QColor(theme.surface))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(theme.surface_alt))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(theme.surface))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(theme.text_primary))
        palette.setColor(QPalette.ColorRole.Text, QColor(theme.text_primary))
        palette.setColor(QPalette.ColorRole.Button, QColor(theme.secondary))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(theme.text_primary))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(theme.error))
        palette.setColor(QPalette.ColorRole.Link, QColor(theme.primary))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(theme.primary))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor('#ffffff'))
        
        app.setPalette(palette)