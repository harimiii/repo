# -- Path setup --------------------------------------------------------------
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

# -- Project information -----------------------------------------------------
project = 'راهنمای آزمایشگاه‌ها'
author = 'داکرمید'
release = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'myst_parser',
    'sphinx_rtd_theme'
]

templates_path = ['_templates']
exclude_patterns = []

language = 'fa'

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_css_files = [
    'rtl.css',
    'sidebar-rtl.css',
    'hide-footer.css',
    'custom-rtl.css',
    'custom.css',  
]
