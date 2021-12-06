# Keep It Tidy

Web app that serves the purpose of a customizable online inventory.

Users can create collections and assign custom fields to them with various data types, later they can add items to those collections and fill in the information according to the fields they created.

## Distinctiveness and Complexity

The main goal of for this web application was to create an inventory that is unrestrictive to the user and to what the user wants to store iin it.
When a collection is being created the user can see it has 3 main fields added to it: Name, Description, Image. Below the user can add additional fields acording to the collection's needs, the number of fields and types of fields are up to the user. Later when an item is being registered to that collections, the forms that need to be filled in for that item represent the fields the user chose when creating that collection. This way each collection is able to store different kinds of items.

# Backend
Because I wanted these collections to be customizable, each additional field besides Name, Description will have it's own class inside models.py.
Image fields also have their own model class in order to allow an item to have multiple images.
Also, for the purpose of sending a dictionary to the front end that communicates each "Field Name: Field Type" associated with a certain collection, I've created a model class that acts asa dictionary called "FieldDict" and a model class for the name-type pair of a certain field called "FieldNameTypePair"; these are created along with the collection and will be used to communcate each collection's fields and their respective types to the front end in order to create forms.

When all these models come together they allow items to be highly customizable so that it is possible for 2 items from 2 different collections to have completely different attributes.



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
