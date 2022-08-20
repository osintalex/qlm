# Overview

A command line tool to take notes. Still _very much_ a work in progress! Uses github as a backend.

# How To

1. `poetry run qlm` for dev
2. `poetry build` to build the package
3. Then in `qlm-builds` virtual env:
   `pip uninstall qlm`
   `pip install <path to new build>`
4. Then you can run `qlm` in that directory.

