# Overview

A command line tool to take notes. Still _very much_ a work in progress! Uses github as a backend.

# Installation

Currently only from test pypi:
```commandline
pip install -i https://test.pypi.org/pypi/ --extra-index-url https://pypi.org/simple qlm
```

# Local Development

Use pyenv to set version locally with `pyenv local <virtualenv>`. Then do `poetry env use $(pyenv which python)`.
Then `pip install poetry` and `poetry install`.

1. `poetry run qlm` for dev
2. `poetry build` to build the package
3. Then in a new virtual env:
   `pip uninstall qlm`
   `pip install <path to new build>`
4. Then you can run `qlm` in that directory.
5. Run `poetry run pytest -vv`.
6. For precommit set up, `poetry run pre-commit install`.
