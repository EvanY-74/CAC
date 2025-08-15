# HOW TO SET UP YOUR ENVIRONMENT

1. Clone GitHub repository (if you haven't done so already)
    - Press the **Code** button then copy the _URL_

2. Install [poetry](https://python-poetry.org/docs/)
    - Install in powershell using: `(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -`
    - Then add this to your *Path environment variable* so you can use poetry: `%USERPROFILE%\AppData\Roaming\Python\Scripts`
    
3. Create a virtual environment with: `python -m venv venv`
    - Press _Ctrl + \`_ to open the **terminal**
    - This will create your very own _venv_ folder where stuff like libraries and Scripts will go

4. Activate it: `venv\Scripts\activate`
    - You should see **(venv)** before the working directory showing that your virtual environment is activated
    - You might need to run `Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process` if running scripts is disabled

5. Install all the dependencies: `pip install .`
    - This installs all the dependencies in _poetry install_ to your local files. They are stored in `venv\Lib\site-packages`.

6. Run the app: `python main.py`