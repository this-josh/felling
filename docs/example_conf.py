
import os
import sys
import felling

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("cd ../.."))


project = "felling"
copyright = "2021, this-josh"
author = "this-josh"


release = str(felling.__version__)


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
    "sphinxarg.ext",
]

html_theme = "sphinx_rtd_theme"


htmlhelp_basename = "felling"
