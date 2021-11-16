# Keep It Tidy

Web app that lets you create customized collections of various items.
Each collection can be set up multiple fields of different types deppending on the the items you intend to keep track of.

## Getting Started

This webapp is built with the Django framework so it requires Python to be installed in your computer.

### Prerequisites

- Python 3
- Django
- Pillow (used by Django for processing image files)
- SQLite3
- XLRD (used to read user uploaded XLS files in order to import data from them)

### Installing

Install Python

    https://www.python.org/downloads/

Set up a virtual enviroment

    python3 -m venv /path/to/new/virtual/environment

Virtual Enviroment needs to be activated before each use

    Windows -> virtualEnviromentFolder\Scripts\ -> activate
    Linux -> virtualEnviromentFolder/bin/ -> source activate
    
Install dependencies from requirements.txt - Go inside the directory containing requirements.txt and run the following command

    pip install -r requirements.txt

Start Server - Go inside the directory containing manage.py and run the following command

    python manage.py runserver
    
Use the link in the terminal to access the site


## Acknowledgments

  - CS50’s Web Programming with Python and JavaScript course - https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript
  - Helpful strangers on stackoverflow.com
  - Hat tip to anyone whose code is used
