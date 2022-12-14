"""A 'Theme Changer' plugin for novelyst.

Version @release

Adds a 'Theme Changer' entry to the 'Tools' menu to open a window
with a combobox that lists all available themes. 
The selected theme will be persistently applied.  

To have a wider choice, you may want to install the ttkthemes package:

pip install ttkthemes

Requires Python 3.6+
Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_themes
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
APPLICATION = 'Theme Changer'
PLUGIN = f'{APPLICATION} plugin @release'

import tkinter as tk
from tkinter import ttk
try:
    from ttkthemes import ThemedStyle
    extraThemes = True
except ModuleNotFoundError:
    extraThemes = False


class Plugin():
    """A 'Theme Changer' plugin class.
    
    Public methods:
        disable_menu() -- disable menu entries when no project is open.
        enable_menu() -- enable menu entries when a project is open.    
    """
    VERSION = '@release'
    NOVELYST_API = '4.0'
    DESCRIPTION = 'Allows changing between available themes'
    URL = 'https://peter88213.github.io/novelyst_themes'

    def install(self, ui):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            ui -- reference to the NovelystTk instance of the application.
        """
        self._ui = ui
        __, x, y = self._ui.root.geometry().split('+')
        offset = 300
        windowGeometry = f'+{int(x)+offset}+{int(y)+offset}'
        if extraThemes:
            self._ui.guiStyle = ThemedStyle(self._ui.root)
        if not self._ui.kwargs.get('gui_theme', ''):
            self._ui.kwargs['gui_theme'] = self._ui.guiStyle.theme_use()

        if not self._ui.kwargs['gui_theme'] in self._ui.guiStyle.theme_names():
            self._ui.kwargs['gui_theme'] = self._ui.guiStyle.theme_use()
        if extraThemes:
            self._ui.guiStyle.set_theme(self._ui.kwargs['gui_theme'])
        else:
            self._ui.guiStyle.theme_use(self._ui.kwargs['gui_theme'])

        # Create a submenu
        self._ui.toolsMenu.add_command(label=APPLICATION, command=lambda: SettingsWindow(self._ui, windowGeometry))
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self._ui.toolsMenu.entryconfig(APPLICATION, state='normal')


class LabelCombo(ttk.Frame):
    """Combobox with a label.
    
    Credit goes to user stovfl on stackoverflow
    https://stackoverflow.com/questions/54584673/how-to-keep-tkinter-button-on-same-row-as-label-and-entry-box
    """

    def __init__(self, parent, text, textvariable, values, lblWidth=10):
        super().__init__(parent)
        self.pack(fill=tk.X)
        self._label = ttk.Label(self, text=text, anchor=tk.W, width=lblWidth)
        self._label.pack(side=tk.LEFT)
        self._combo = ttk.Combobox(self, textvariable=textvariable, values=values)
        self._combo.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def current(self):
        """Return the combobox selection."""
        return self._combo.current()

    def configure(self, text=None, values=None):
        """Configure internal widgets."""
        if text is not None:
            self._label['text'] = text
        if values is not None:
            self._combo['values'] = values


class SettingsWindow(tk.Toplevel):

    def __init__(self, ui, size, **kw):
        self._ui = ui
        super().__init__(**kw)
        self.title(APPLICATION)
        self.geometry(size)
        self.grab_set()
        self.focus()
        window = ttk.Frame(self)
        window.pack(fill=tk.BOTH)

        # Combobox for theme setting.
        theme = self._ui.guiStyle.theme_use()
        themeList = list(self._ui.guiStyle.theme_names())
        themeList.sort()
        self._theme = tk.StringVar(value=theme)
        self._theme.trace('w', self._change_theme)
        themeCombobox = LabelCombo(window,
                              text='GUI Theme',
                              textvariable=self._theme,
                              values=themeList,
                              lblWidth=20)
        themeCombobox.pack(padx=5, pady=5)

        # "Exit" button.
        ttk.Button(window, text='Exit', command=self.destroy).pack(padx=5, pady=5)

    def _change_theme(self, *args, **kwargs):
        theme = self._theme.get()
        self._ui.kwargs['gui_theme'] = theme
        if extraThemes:
            self._ui.guiStyle.set_theme(self._ui.kwargs['gui_theme'])
        else:
            self._ui.guiStyle.theme_use(self._ui.kwargs['gui_theme'])

