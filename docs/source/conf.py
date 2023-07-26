# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# https://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'usher_wiki'
copyright = '2021, Bryan Thornlow'
author = 'Bryan Thornlow'


# The full version, including alpha/beta/rc tags
release = '0.0.2'


# -- General configuration ---------------------------------------------------

# https://github.com/sphinx-doc/sphinx/issues/7369
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'


# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [ ]

pygments_style = 'sphinx'

linkcheck_anchors = False

# Put in URLs you want to ignore for linkcheck below. Common problematic URLs include:
# * doi.org (but only sometimes?)
# * any docs website that uses ZenDesk
# * websites with weird or expired certs (ex: mlab.wustl.edu)
# * internal links which are not resolved before compile time (ex: a clickable image with an internal link)
linkcheck_ignore = [ "https://mblab.wustl.edu/GTF22.html" ] 

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
#
# Note that if you have the myst_parser extension, .md files we will
# be rendered too, even though they are not listed below!
source_suffix = '.rst'

# Add any paths that contain templates here, relative to this directory.
# This allows us to have RST documents that don't normally appear in the TOC!
templates_path = ['_templates', 'presentations']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#html_theme = 'default'
html_theme = 'sphinx_rtd_theme'

# Note that writing options under "html_theme_options" isn't supported if html_theme is default,
# so we do it like this instead
style_nav_header_background = 'white'
logo_only = True
display_version = False
include_hidden = True

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_logo = '_static/usher_logo.png'