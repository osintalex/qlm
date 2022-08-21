# Overview

A command line tool to take notes. Still _very much_ a work in progress! Uses github as a backend.

# How To

Use pyenv to set version locally with `pyenv local <virtualenv>`. Then do `poetry env use $(pyenv which python)`.
Then `poetry install`.

1. `poetry run qlm` for dev
2. `poetry build` to build the package
3. Then in `qlm-builds` virtual env:
   `pip uninstall qlm`
   `pip install <path to new build>`
4. Then you can run `qlm` in that directory.
5. For tests set `PYTHONPATH` to `qlm` source code directory then run `poetry run pytest -vv`.

