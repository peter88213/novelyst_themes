[Project home page](index) > Changelog

------------------------------------------------------------------------

## Changelog

### v4.0.2

Fix a bug where the available themes are not displayed, if ttkthemes.ThemedStyle is not installed.
This is, because ttkthemes.ThemedStyle.theme_names() returns a list, whereas ttk.Style.theme_names() returns a tuple, which has no sort() method.

Compatibility: novelyst v4.0 API

### v4.0.1

- Make the setup script run with Python 3.11 under Windows.

Compatibility: novelyst v4.0 API

### v4.0.0

- API update. 

Compatibility: novelyst v4.0 API

### v3.0.0

- Code optimization and library update. 

Compatibility: novelyst v3.0 API

### v2.0.1

- API upgrade.

Compatibility: novelyst v2.0 API

### v0.2.1

- Release under the GPLv3 license.

Compatibility: novelyst v1.0 API
