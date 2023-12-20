"""A 'Theme Changer' plugin for noveltree.

Version @release

Adds a 'Theme Changer' entry to the 'Tools' menu to open a window
with a combobox that lists all available themes. 
The selected theme will be persistently applied.  

To have a wider choice, you may want to install the ttkthemes package:

pip install ttkthemes

Requires Python 3.6+
Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_themes
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
import sys
import os
import tkinter as tk
from tkinter import ttk
import gettext
import locale
try:
    from ttkthemes import ThemedStyle
    extraThemes = True
except ModuleNotFoundError:
    extraThemes = False

# Initialize localization.
LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
try:
    CURRENT_LANGUAGE = locale.getlocale()[0][:2]
except:
    # Fallback for old Windows versions.
    CURRENT_LANGUAGE = locale.getdefaultlocale()[0][:2]
try:
    t = gettext.translation('nv_themes', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
    _ = t.gettext
except:

    def _(message):
        return message


class Plugin():
    """A 'Theme Changer' plugin class."""
    VERSION = '@release'
    NOVELYST_API = '0.6'
    DESCRIPTION = 'Allows changing between available themes'
    URL = 'https://peter88213.github.io/nv_themes'

    def install(self, model, ui, controller, prefs):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            controller -- reference to the main controller instance of the application.
            ui -- reference to the main view instance of the application.
        """
        self._ui = ui
        self._prefs = prefs
        __, x, y = self._ui.root.geometry().split('+')
        offset = 300
        windowGeometry = f'+{int(x)+offset}+{int(y)+offset}'
        if extraThemes:
            self._ui.guiStyle = ThemedStyle(self._ui.root)
        if not self._prefs.get('gui_theme', ''):
            self._prefs['gui_theme'] = self._ui.guiStyle.theme_use()

        if not self._prefs['gui_theme'] in self._ui.guiStyle.theme_names():
            self._prefs['gui_theme'] = self._ui.guiStyle.theme_use()
        if extraThemes:
            self._ui.guiStyle.set_theme(self._prefs['gui_theme'])
        else:
            self._ui.guiStyle.theme_use(self._prefs['gui_theme'])

        # Create a submenu
        self._ui.viewMenu.add_command(
            label=_('Change theme'),
            command=lambda: SettingsWindow(self._ui, self._prefs, windowGeometry)
            )


class LabelCombo(ttk.Frame):
    """Combobox with a label.
    
    Credit goes to user stovfl on stackoverflow
    https://stackoverflow.com/questions/54584673/how-to-keep-tkinter-button-on-same-row-as-label-and-entry-box
    """

    def __init__(self, parent, text, textvariable, values, lblWidth=10):
        super().__init__(parent)
        self.pack(fill='x')
        self._label = ttk.Label(self, text=text, anchor='w', width=lblWidth)
        self._label.pack(side='left')
        self._combo = ttk.Combobox(self, textvariable=textvariable, values=values)
        self._combo.pack(side='left', fill='x', expand=True)

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

    def __init__(self, ui, prefs, size, **kw):
        self._ui = ui
        self._prefs = prefs
        super().__init__(**kw)
        self.title(_('Theme Changer'))
        self.geometry(size)
        self.grab_set()
        self.focus()
        window = ttk.Frame(self)
        window.pack(fill='both')

        # Combobox for theme setting.
        theme = self._ui.guiStyle.theme_use()
        themeList = list(self._ui.guiStyle.theme_names())
        themeList.sort()
        self._theme = tk.StringVar(value=theme)
        self._theme.trace('w', self._change_theme)
        themeCombobox = LabelCombo(
            window,
            text=_('GUI Theme'),
            textvariable=self._theme,
            values=themeList,
            lblWidth=20
            )
        themeCombobox.pack(padx=5, pady=5)

        # "Exit" button.
        ttk.Button(window, text=_('Exit'), command=self.destroy).pack(padx=5, pady=5)

    def _change_theme(self, *args, **kwargs):
        theme = self._theme.get()
        self._prefs['gui_theme'] = theme
        if extraThemes:
            self._ui.guiStyle.set_theme(self._prefs['gui_theme'])
        else:
            self._ui.guiStyle.theme_use(self._prefs['gui_theme'])

