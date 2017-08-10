#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import chdir
from os.path import abspath, dirname, join
from datetime import datetime
now = datetime.now()

# make sure that we're in the source directory
# so that it's consistent between read the docs and local
cur_dir = abspath(dirname(__file__))

import phypno

# -- General configuration ------------------------------------------------
extensions = [
    'sphinx.ext.autosummary',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.mathjax',
]

# autodoc options
autosummary_generate = True
autodoc_default_flags = ['inherited-members']

# Napoleon settings
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True

# mathjax settings
mathjax_path = '//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML'

# todo settings
todo_include_todos = True
todo_link_only = True

# source suffix
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'phypno'
copyright = '2013-{}, Gio Piantoni'.format(now.year)
author = 'Gio Piantoni'

# The short X.Y version.
version = phypno.__version__
# The full version, including alpha/beta/rc tags.
release = version

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_show_sphinx = False

html_extra_path = [
        '.nojekyll',
        ]

# Output file base name for HTML help builder.
htmlhelp_basename = 'phypnodoc'


def run_apidoc(_):
    chdir(cur_dir)  # use same dir as readthedocs, which is docs/source
    from sphinx.apidoc import main
    output_path = join(cur_dir, 'api')
    # here use paths relative to docs/source
    main(['-f', '-e', '-o', output_path, '../../phypno',
          '../../phypno/viz', '../../phypno/widgets',
          '../../phypno/scroll_data.py'])

def setup(app):
    app.connect('builder-inited', run_apidoc)
