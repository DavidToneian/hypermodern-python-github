# Python project template based on Hypermodern Python

This is a template that can be used when starting a new Python project based on the structure and tooling presented in the Hypermodern Python articles and repositories. See `hypermodern-python-link.txt` for references, and `links.txt` for further resources.

## Installation

First, clone the repository, and then run

```
poetry install
poetry run pip install nox nox-poetry
```

From then on, everytime you use a new shell to work with the project, run
`poetry shell`
in order to have the right python environment enabled.

If you want to install git pre-commit hooks to locally run `black` and `flake8`
prior to committing, execute the following once:

```
poetry install
poetry run pip install nox nox-poetry
```
