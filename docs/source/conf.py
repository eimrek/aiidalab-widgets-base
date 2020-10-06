# pylint: disable=invalid-name

# -*- coding: utf-8 -*-
"""Sphinx configuration for aiidalab-widgets-base."""
import os
import subprocess
import sys
import time

# Load the dummy profile to make sure the docs build suucceed even if the current
# default profile of the AiiDA installation is not configured.
from aiida.manage.configuration import load_documentation_profile
load_documentation_profile()

# Let's make sure the entry points are up to date
try:
    from aiida.plugins.entry_point import ENTRYPOINT_MANAGER as mgr
    mgr.scan()
except AttributeError:
    # .scan may be no longer availabe if we switch away from reentry
    pass

import aiidalab_widgets_base  # pylint: disable=wrong-import-position

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinxcontrib.contentui',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3.7', None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
#~ master_doc = 'index'
master_doc = 'index'

# General information about the project.
project = u'aiidalab-widgets-base'
copyright_first_year = "2020"
copyright_owners = "The AiiDAlab Team"

current_year = str(time.localtime().tm_year)
copyright_year_string = current_year if current_year == copyright_first_year else "{}-{}".format(
    copyright_first_year, current_year)
copyright = u'{}, {}. All rights reserved'.format(copyright_year_string, copyright_owners)  # pylint: disable=redefined-builtin

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The full version, including alpha/beta/rc tags.
# The short X.Y version.
version = '.'.join(aiidalab_widgets_base.__version__.split('.')[:2])

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# Output file base name for HTML help builder.
htmlhelp_basename = 'aiidalab-widgets-base-doc'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


def run_apidoc(_):
    """Runs sphinx-apidoc when building the documentation.
    Needs to be done in conf.py in order to include the APIdoc in the
    build on readthedocs.
    See also https://github.com/rtfd/readthedocs.org/issues/1139
    """
    source_dir = os.path.abspath(os.path.dirname(__file__))
    apidoc_dir = os.path.join(source_dir, 'apidoc')
    package_dir = os.path.join(source_dir, os.pardir, os.pardir, 'aiidalab_widgets_base')

    # In #1139, they suggest the route below, but this ended up
    # calling sphinx-build, not sphinx-apidoc
    #from sphinx.apidoc import main
    #main([None, '-e', '-o', apidoc_dir, package_dir, '--force'])

    cmd_path = 'sphinx-apidoc'
    if hasattr(sys, 'real_prefix'):  # Check to see if we are in a virtualenv
        # If we are, assemble the path manually
        cmd_path = os.path.abspath(os.path.join(sys.prefix, 'bin', 'sphinx-apidoc'))

    options = [
        '-o',
        apidoc_dir,
        package_dir,
        '--private',
        '--force',
        '--no-toc',
    ]

    # See https://stackoverflow.com/a/30144019
    env = os.environ.copy()
    env["SPHINX_APIDOC_OPTIONS"] = 'members,special-members,private-members,undoc-members,show-inheritance'
    subprocess.check_call([cmd_path] + options, env=env)


def setup(app):
    app.connect('builder-inited', run_apidoc)


# Warnings to ignore when using the -n (nitpicky) option
# We should ignore any python built-in exception, for instance
nitpick_ignore = [
    ('py:class', 'ipywidgets.widgets.widget_box.VBox'),
    ('py:class', 'ipywidgets.widgets.widget_button.Button'),
    ('py:class', 'ipywidgets.widgets.widget_selection.Dropdown'),
    ('py:class', 'ipywidgets.widgets.widget_string.HTML'),
    ('py:class', 'ipywidgets.widgets.widget_string.Textarea'),
    ('py:class', 'BandsData'),
    ('py:class', 'Dict'),
    ('py:class', 'FolderData'),
]
