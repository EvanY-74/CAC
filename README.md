# HOW TO SET UP YOUR ENVIRONMENT

1. Clone GitHub repository (if you haven't done so already)
    - Press the **Code** button then copy the _URL_

2. Install [poetry](https://python-poetry.org/docs/)
    - Poetry is a package manager for python that keeps track of the needed packages and dependencies for those packages so you can install them easily.
    - Install in vscode terminal (open using _Ctrl + \`_) by running: `(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -`
    - Then add this to your *Path environment variable* so you can use poetry: `%USERPROFILE%\AppData\Roaming\Python\Scripts`
    - Check installation and correct environment variable configuration using `poetry --version`
    
3. Create a virtual environment with: `python -m venv venv`
    - This will create your very own _venv_ folder where stuff like libraries and scripts will go

4. Activate it: `venv\Scripts\activate`
    - You might need to run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force` if running scripts is disabled
    - You should see **`(venv)`** before the working directory showing that your virtual environment is activated

5. Install all the dependencies (one time thing): `poetry install`
    - This installs all the packages and dependencies in _pyproject.toml_ and _poetry.lock_ to your virtual environment. They are stored in `venv\Lib\site-packages`.

6. Run the app: `python main.py`
    - When you make changes, the server will automatically restart with the new changes.

# DEVELOPMENT

- If you want to add a new package, use `poetry add [package name]`
- Other users will need to re-run `poetry install` in order to locally install the package on their computer
