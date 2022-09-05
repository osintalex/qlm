# Contributing

Contributions are very welcome!

:smile:

## How to get started

First, please consider starring the repo if you're enjoying using **qlm**.

Then please create an issue to discuss the bug/feature/whatever before making a pull request.

## Local Development

**qlm** uses [poetry](https://python-poetry.org/). There are quite a few ways to set up a
poetry project, but I've found this approach the most reliable for me.

1. Use [pyenv](https://github.com/pyenv/pyenv) to configure the local python version with
`pyenv local <virtualenv name>`.
2. Install poetry with `pip install poetry`.
3. Then to set up your poetry virtuale environment, run `poetry env use $(pyenv which python)`.
4. Now to set up the project, run `poetry install`.

Hopefully that all goes smoothly - if it doesn't, please submit an issue on Github.

Now, here are some commands you will need for local development:

* `poetry run qlm` to run the application locally
* `poetry build` to build the Python package and then, in a new folder/virtualenv, run
`pip install <path to wheel you just built>`
* To run test: `poetry run pytest --cov=qlm --cov-report=html tests/`
* To set up the pre-commit hooks, `poetry run pre-commit install`

I'm not aiming at 100% test coverage in this project since I don't think there's much point
testing the Github API integrations or Python builtins that interact with files. However,
anything that tests the application's commands should include tests.
