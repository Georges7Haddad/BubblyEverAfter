# Bubbly Ever After
## Getting Started
To start working on the code, you'll need to clone the repo in your local directory.
1. Create a Python virtual environment for your Django project. This virtual environment allows you to isolate this project and install any packages you need without affecting the system Python installation. At the terminal, type the following command:

        $ virtualenv .venv

2. Activate the virtual environment:

        $ activate ./venv/bin/activate

3. Install Python dependencies for this project:

        $ pip install -r requirements.txt

4. Start the Django development server:

        $ python manage.py runserver

5. Open http://127.0.0.1:8000/ in a web browser to view your application.
## Pre-hook and Black
Now, we're gonna set up the project with pre-hook and black. This way, before each commit black will check your code.
[Black](https://github.com/python/black) is a highly opinionated code formatter. Black focuses on reformatting your code files in place for you. When you're comfortable with black taking over the minutiae of hand formatting you will see that you can focus more on the content of your code than formatting it properly.

1. **Install pre-commit**

		 `pip install pre-commit`

2. **Configure Black**
Create a `pyproject.toml` file in the root of the project directory, if it doesn't exist, and copy the following into the file:
```[tool.black]
line-length = 120
target-version = ['py37']
include = '\.pyi?$'
exclude = '''
/(
    \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | \.env
  | env
  | venv
  | \.venv3
  | venv3
  | _build
  | buck-out
  | build
  | dist
)/
'''
```
3. **Configure pre-commit**
Create a `.pre-commit-config.yaml` file in the root of the project directory, if it doesn't exist, and add the following to the file:
```
# See https://pre-commit.com for more information
    # See https://pre-commit.com/hooks.html for more hooks
    repos:
      - repo: https://github.com/ambv/black
        rev: stable
        hooks:
          - id: black
            language_version: python3.7
```
4. **Install the hooks**
Install the git hooks defined in the pre-commit file by running the following in the terminal:
    `pre-commit install`
5. **Run the hooks**
If this is an already existing project you may want to go ahead and format all the files. You can do this by running the following in the terminal:
`pre-commit run --all-files`
