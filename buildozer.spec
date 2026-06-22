[app]

# App title shown on home screen
title = Hedge Calculator

# Package name (must be lowercase, no spaces)
package.name = hedgecalculator

# Package domain (reverse domain style, make it anything)
package.domain = org.hedgeapp

# Source directory (. means same folder as this spec file)
source.dir = .

# Main script
source.include_exts = py,png,jpg,kv,atlas

# App version
version = 1.0

# Requirements - kivy and python
requirements = python3,kivy==2.3.0

# Orientation
orientation = portrait

# Android permissions (none needed for this app)
# android.permissions = INTERNET

# Minimum Android API level
android.minapi = 21

# Target Android API level
android.api = 33

# NDK version
android.ndk = 25b

# Icon - comment this out if you don't have a custom icon file
# icon.filename = %(source.dir)s/icon.png

# Presplash (loading screen) - comment out if no image
# presplash.filename = %(source.dir)s/presplash.png

# Presplash background color (shown while app loads)
android.presplash_color = #1A1A26

# App fullscreen (0 = show status bar, 1 = hide it)
fullscreen = 0

[buildozer]

# Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# Warn before building on a non-Linux platform
warn_on_root = 1
