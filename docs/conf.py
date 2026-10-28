# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as package_version

project = "ATG"
copyright = "2026, Allan Cao"
author = "Allan Cao"
try:
    version = release = package_version("ATG-lib")
except PackageNotFoundError:
    version = release = ""

# -- General configuration ------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
]
extensions = ['sphinx.ext.autodoc', 'sphinx_copybutton', 'sphinx_rtd_theme']
language = "en"
master_doc = "index"
pygments_style = "sphinx"
source_suffix = ".rst"
templates_path = ["_templates"]

# -- Options for HTML output ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
