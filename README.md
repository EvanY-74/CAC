
# HOW TO START CODING
1. Clone GitHub repository (if you haven't done so already)
    - Press the **Code** button then copy the _URL_
2. Create a virtual environment with: `python -m venv venv`
    - Press _Ctrl + \`_ (the tilde is above the tab key) to open the **terminal**
    - This will create your very own _venv_ folder where stuff like libraries and Scripts will go
3. Activate it: `venv\Scripts\activate`
    - You should see **(venv)** before the working directory showing that your virtual environment is activated
4. Install all the dependencies: `pip install .`
    - This installs all the dependencies in _pyproject.toml_ to your local files. They are stored in `venv\Lib\site-packages`.
5. Run the file: `python main.py`