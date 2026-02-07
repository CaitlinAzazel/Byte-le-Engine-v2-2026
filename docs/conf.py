# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = '2026 QBB Security Manual'
copyright = '1974-2026, NDSU ACM'
author = 'NDSU ACM Byte-le 2026 Dev Team'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_copybutton',
    'sphinx_tabs.tabs',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = [
    '_static'
]
html_css_files = [
    'styles/custom.css'
]

html_title = '2026 QBB Security Manual'
html_theme = 'shibuya'
html_theme_options = {
    'sidebar_hide_name': True, # furo
    'accent_color': 'indigo', # shibuya
    'github_url': 'https://github.com/acm-ndsu/Byte-le-2026-Client-Package', # shibuya
    'discord_url': 'https://discord.gg/zJ9xU7gZ8q', # shibuya
}
html_logo = '_static/images/bytele-logo.png'
