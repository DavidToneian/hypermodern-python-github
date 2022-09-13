import sphinx_rtd_theme


project = "template-project"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx_autodoc_typehints",
    "sphinx_rtd_theme",
]

# Autosummary use inspired by: https://stackoverflow.com/a/62613202
autosummary_generate = True

html_theme = "sphinx_rtd_theme"

templates_path = ["_templates"]
