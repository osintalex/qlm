# Overview

A command line tool to take notes. Still _very much_ a work in progress! Uses github as a backend.

# How To

Use pyenv to set version locally with `pyenv local <virtualenv>`. Then do `poetry env use $(pyenv which python)`.
Then `pip install poetry` and `poetry install`.

1. `poetry run qlm` for dev
2. `poetry build` to build the package
3. Then in a new virtual env:
   `pip uninstall qlm`
   `pip install <path to new build>`
4. Then you can run `qlm` in that directory.
5. Run `poetry run pytest -vv`.

