# menu_manager.py
"""
Menu Manager riutilizzabile per applicazioni PyQt6.
Questo modulo fornisce una classe generica per la gestione dei menu
che può essere utilizzata in diverse applicazioni.
"""

from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import Qt, pyqtSignal, QObject


class MenuAction:
    """Rappresenta un'azione del menu con tutte le sue proprietà."""
    
    def __init__(self, name, text, callback=None, shortcut=None, 
                 tooltip=None, icon=None, checkable=False, enabled=True):
        """
        Inizializza un'azione del menu.
        
        Args:
            name (str): Nome identificativo dell'azione
            text (str): Testo visualizzato nel menu
            callback (callable): Funzione da chiamare quando l'azione è attivata
            shortcut (str): Scorciatoia da tastiera (es. "Ctrl+S")
            tooltip (str): Tooltip dell'azione
            icon (str): Percorso dell'icona
            checkable (bool): Se l'azione è selezionabile
            enabled (bool): Se l'azione è abilitata
        """
        self.name = name
        self.text = text
        self.callback = callback
        self.shortcut = shortcut
        self.tooltip = tooltip
        self.icon = icon
        self.checkable = checkable
        self.enabled = enabled


class MenuManager(QObject):
    """
    Gestisce la creazione e l'aggiornamento dei menu per applicazioni PyQt6.
    Questa classe è progettata per essere riutilizzabile tra diverse applicazioni.
    """
    
    # Segnali per comunicare con l'applicazione principale
    action_triggered = pyqtSignal(str)  # Emesso quando un'azione è attivata
    language_changed = pyqtSignal(str)  # Emesso quando cambia la lingua
    
    def __init__(self, parent_window, translations=None):
        """
        Inizializza il MenuManager.
        
        Args:
            parent_window: Finestra principale dell'applicazione
            translations: Oggetto traduzioni (opzionale)
        """
        super().__init__()
        self.parent_window = parent_window
        self.translations = translations
        self.menu_bar = None
        self.menus = {}
        self.actions = {}
        self.current_language = 'en'
        
    def create_menu_bar(self):
        """Crea la barra del menu principale."""
        if hasattr(self.parent_window, 'menuBar'):
            self.menu_bar = self.parent_window.menuBar()
        else:
            self.menu_bar = QMenuBar(self.parent_window)
        
        return self.menu_bar
    
    def add_menu(self, menu_name, title):
        """
        Aggiunge un menu alla barra dei menu.
        
        Args:
            menu_name (str): Nome identificativo del menu
            title (str): Titolo visualizzato del menu
            
        Returns:
            QMenu: Il menu creato
        """
        if not self.menu_bar:
            self.create_menu_bar()
        
        menu = self.menu_bar.addMenu(title)
        self.menus[menu_name] = menu
        return menu
    
    def add_action_to_menu(self, menu_name, action):
        """
        Aggiunge un'azione a un menu specifico.
        
        Args:
            menu_name (str): Nome del menu
            action (MenuAction): Azione da aggiungere
        """
        if menu_name not in self.menus:
            raise ValueError(f"Menu '{menu_name}' not found")
        
        menu = self.menus[menu_name]
        q_action = QAction(action.text, self.parent_window)
        
        # Configura l'azione
        if action.shortcut:
            q_action.setShortcut(QKeySequence(action.shortcut))
        
        if action.tooltip:
            q_action.setToolTip(action.tooltip)
            q_action.setStatusTip(action.tooltip)
        
        if action.icon:
            # TODO: Implementare il caricamento delle icone
            pass
        
        q_action.setCheckable(action.checkable)
        q_action.setEnabled(action.enabled)
        
        # Connetti il callback
        if action.callback:
            q_action.triggered.connect(action.callback)
        else:
            # Emetti un segnale generico con il nome dell'azione
            q_action.triggered.connect(lambda: self.action_triggered.emit(action.name))
        
        menu.addAction(q_action)
        self.actions[action.name] = q_action
        
        return q_action
    
    def add_separator_to_menu(self, menu_name):
        """
        Aggiunge un separatore a un menu.
        
        Args:
            menu_name (str): Nome del menu
        """
        if menu_name not in self.menus:
            raise ValueError(f"Menu '{menu_name}' not found")
        
        self.menus[menu_name].addSeparator()
    
    def get_action(self, action_name):
        """
        Ottiene un'azione per nome.
        
        Args:
            action_name (str): Nome dell'azione
            
        Returns:
            QAction: L'azione richiesta o None se non trovata
        """
        return self.actions.get(action_name)
    
    def enable_action(self, action_name, enabled=True):
        """
        Abilita o disabilita un'azione.
        
        Args:
            action_name (str): Nome dell'azione
            enabled (bool): True per abilitare, False per disabilitare
        """
        action = self.get_action(action_name)
        if action:
            action.setEnabled(enabled)
    
    def set_action_text(self, action_name, text):
        """
        Imposta il testo di un'azione.
        
        Args:
            action_name (str): Nome dell'azione
            text (str): Nuovo testo
        """
        action = self.get_action(action_name)
        if action:
            action.setText(text)
    
    def update_translations(self, new_language=None):
        """
        Aggiorna tutte le traduzioni dei menu.
        
        Args:
            new_language (str): Nuova lingua (opzionale)
        """
        if new_language and self.translations:
            self.translations.set_language(new_language)
            self.current_language = new_language
            self.language_changed.emit(new_language)
        
        # Ricostruisce i menu con le nuove traduzioni
        self._rebuild_menus()
    
    def _rebuild_menus(self):
        """Ricostruisce i menu con le traduzioni aggiornate."""
        # Questa funzione dovrebbe essere implementata dalle classi derivate
        # o dalle applicazioni che utilizzano questo manager
        pass
    
    def clear_all_menus(self):
        """Rimuove tutti i menu e le azioni."""
        if self.menu_bar:
            self.menu_bar.clear()
        self.menus.clear()
        self.actions.clear()


class StandardMenuBuilder:
    """
    Builder per creare menu standard comuni a molte applicazioni.
    """
    
    @staticmethod
    def create_file_menu_actions(translations=None):
        """
        Crea le azioni standard per un menu File.
        
        Args:
            translations: Oggetto traduzioni
            
        Returns:
            list: Lista di MenuAction per il menu File
        """
        t = translations if translations else lambda x: x
        
        return [
            MenuAction('new', t.get('new') if hasattr(t, 'get') else 'New', 
                      shortcut='Ctrl+N'),
            MenuAction('open', t.get('open') if hasattr(t, 'get') else 'Open', 
                      shortcut='Ctrl+O'),
            MenuAction('save', t.get('save') if hasattr(t, 'get') else 'Save', 
                      shortcut='Ctrl+S'),
            MenuAction('save_as', t.get('save_as') if hasattr(t, 'get') else 'Save As...', 
                      shortcut='Ctrl+Shift+S'),
            MenuAction('separator', ''),  # Separatore
            MenuAction('exit', t.get('exit') if hasattr(t, 'get') else 'Exit', 
                      shortcut='Ctrl+Q')
        ]
    
    @staticmethod
    def create_help_menu_actions(translations=None):
        """
        Crea le azioni standard per un menu Help.
        
        Args:
            translations: Oggetto traduzioni
            
        Returns:
            list: Lista di MenuAction per il menu Help
        """
        t = translations if translations else lambda x: x
        
        return [
            MenuAction('help', t.get('help') if hasattr(t, 'get') else 'Help', 
                      shortcut='F1'),
            MenuAction('about', t.get('about') if hasattr(t, 'get') else 'About')
        ]
    
    @staticmethod
    def create_language_menu_actions(available_languages, translations=None):
        """
        Crea le azioni per un menu di selezione lingua.
        
        Args:
            available_languages (list): Lista delle lingue disponibili
            translations: Oggetto traduzioni
            
        Returns:
            list: Lista di MenuAction per la selezione lingua
        """
        actions = []
        for lang in available_languages:
            # Mappa i codici lingua ai nomi
            lang_names = {
                'it': 'Italiano',
                'en': 'English',
                'es': 'Español',
                'fr': 'Français',
                'de': 'Deutsch'
            }
            
            display_name = lang_names.get(lang, lang.upper())
            actions.append(
                MenuAction(f'lang_{lang}', display_name, checkable=True)
            )
        
        return actions


class ApplicationMenuManager(MenuManager):
    """
    Estensione specializzata di MenuManager per applicazioni specifiche.
    Questa classe può essere ulteriormente personalizzata per ogni applicazione.
    """
    
    def __init__(self, parent_window, translations=None, theme_manager=None):
        super().__init__(parent_window, translations)
        self.theme_manager = theme_manager
        self.language_actions = {}
        self.theme_actions = {}
    
    def setup_standard_menus(self):
        """Configura i menu standard dell'applicazione con ordine logico."""
        self.create_menu_bar()
        
        # Menu File
        file_menu = self.add_menu('file', self._get_text('file_menu'))
        
        # Menu Strumenti (secondo per importanza)
        tools_menu = self.add_menu('tools', self._get_text('tools_menu'))
        
        # Menu Tema (personalizzazione)
        theme_menu = self.add_menu('theme', self._get_text('theme_menu'))
        
        # Menu Lingua (personalizzazione)
        lang_menu = self.add_menu('language', self._get_text('language_menu'))
        
        # Menu Help (ultimo)
        help_menu = self.add_menu('help', self._get_text('help_menu'))
        
        return file_menu, tools_menu, theme_menu, lang_menu, help_menu
    
    def setup_language_menu(self):
        """Configura il menu per la selezione della lingua."""
        if 'language' not in self.menus:
            return
        
        if self.translations:
            available_languages = self.translations.get_available_languages()
            lang_actions = StandardMenuBuilder.create_language_menu_actions(
                available_languages, self.translations
            )
            
            for action in lang_actions:
                q_action = self.add_action_to_menu('language', action)
                self.language_actions[action.name] = q_action
                
                # Connetti il cambio lingua
                lang_code = action.name.replace('lang_', '')
                q_action.triggered.connect(lambda checked, lang=lang_code: self._change_language(lang))
    
    def setup_theme_menu(self):
        """Configura il menu per la selezione del tema."""
        if 'theme' not in self.menus or not self.theme_manager:
            return
        
        from theme_manager import ThemeVariant
        
        # Crea le azioni per ogni tema
        theme_actions = [
            MenuAction('theme_light', self._get_text('light_theme'), checkable=True),
            MenuAction('theme_dark', self._get_text('dark_theme'), checkable=True),
            MenuAction('theme_blue', self._get_text('blue_theme'), checkable=True)
        ]
        
        for action in theme_actions:
            q_action = self.add_action_to_menu('theme', action)
            self.theme_actions[action.name] = q_action
            
            # Connetti il cambio tema
            if action.name == 'theme_light':
                theme_variant = ThemeVariant.LIGHT
            elif action.name == 'theme_dark':
                theme_variant = ThemeVariant.DARK
            elif action.name == 'theme_blue':
                theme_variant = ThemeVariant.BLUE
            
            q_action.triggered.connect(lambda checked, theme=theme_variant: self._change_theme(theme))
        
        # Imposta il tema corrente come selezionato
        self._update_theme_selection()
    
    def _change_language(self, language):
        """Cambia la lingua dell'applicazione."""
        # Deseleziona tutte le azioni lingua
        for action in self.language_actions.values():
            action.setChecked(False)
        
        # Seleziona la nuova lingua
        if f'lang_{language}' in self.language_actions:
            self.language_actions[f'lang_{language}'].setChecked(True)
        
        # Aggiorna le traduzioni
        self.update_translations(language)
    
    def _change_theme(self, theme_variant):
        """Cambia il tema dell'applicazione."""
        if self.theme_manager:
            self.theme_manager.set_theme(theme_variant)
            self._update_theme_selection()
    
    def _update_theme_selection(self):
        """Aggiorna la selezione del tema nel menu."""
        if not self.theme_manager:
            return
        
        # Deseleziona tutti i temi
        for action in self.theme_actions.values():
            action.setChecked(False)
        
        # Seleziona il tema corrente
        current_theme = self.theme_manager.current_theme
        theme_action_map = {
            'LIGHT': 'theme_light',
            'DARK': 'theme_dark', 
            'BLUE': 'theme_blue'
        }
        
        action_name = theme_action_map.get(current_theme.name)
        if action_name and action_name in self.theme_actions:
            self.theme_actions[action_name].setChecked(True)
    
    def _get_text(self, key):
        """Helper per ottenere testo tradotto."""
        if self.translations:
            return self.translations.get(key)
        return key
    
    def _rebuild_menus(self):
        """Ricostruisce i menu con le nuove traduzioni."""
        # Aggiorna i titoli dei menu con il nuovo ordine
        if 'file' in self.menus:
            self.menus['file'].setTitle(self._get_text('file_menu'))
        if 'tools' in self.menus:
            self.menus['tools'].setTitle(self._get_text('tools_menu'))
        if 'theme' in self.menus:
            self.menus['theme'].setTitle(self._get_text('theme_menu'))
        if 'language' in self.menus:
            self.menus['language'].setTitle(self._get_text('language_menu'))
        if 'help' in self.menus:
            self.menus['help'].setTitle(self._get_text('help_menu'))
        
        # Aggiorna i testi delle azioni dei temi
        theme_text_map = {
            'theme_light': 'light_theme',
            'theme_dark': 'dark_theme',
            'theme_blue': 'blue_theme'
        }
        
        for action_name, text_key in theme_text_map.items():
            if action_name in self.theme_actions:
                self.theme_actions[action_name].setText(self._get_text(text_key))
        
        # Aggiorna i testi delle azioni delle lingue
        lang_text_map = {
            'lang_it': 'italian',
            'lang_en': 'english'
        }
        
        for action_name, text_key in lang_text_map.items():
            if action_name in self.language_actions:
                self.language_actions[action_name].setText(self._get_text(text_key))