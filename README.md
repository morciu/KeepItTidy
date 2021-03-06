# Keep It Tidy

Web app that serves the purpose of a customizable online inventory.

Users can create collections and assign custom fields to them with various data types, later they can add items to those collections and fill in the information according to the fields they created.

## Screenshots

### Main page after logging in with all the collections created by the user
![VirtualBox_Xubuntu_18_03_2022_08_51_33](https://user-images.githubusercontent.com/67121125/158951627-4f2d19ef-416c-4fc7-b46a-9be82ad15caa.png)

### Viewing a created collection (dropdown filter options are dynamically created for each collection)
![VirtualBox_Xubuntu_18_03_2022_08_53_48](https://user-images.githubusercontent.com/67121125/158951859-95912f6f-2e6a-4496-819c-9b5fb5a3f31d.png)
![VirtualBox_Xubuntu_18_03_2022_08_53_26](https://user-images.githubusercontent.com/67121125/158951864-536d7e3f-1742-43d8-8f27-8bc0f8d5b8c7.png)

### Viewing an item
![VirtualBox_Xubuntu_18_03_2022_08_56_08](https://user-images.githubusercontent.com/67121125/158952148-693030c1-8df2-4e86-8a42-27dbb72cb9d8.png)

### Creating a new collection page
![VirtualBox_Xubuntu_18_03_2022_08_56_47](https://user-images.githubusercontent.com/67121125/158952280-13a82889-a570-4ba6-bc03-dc1822d71e8d.png)

### Adding a new item (number and types of form fields deppend on how the collection is set up)
![VirtualBox_Xubuntu_18_03_2022_09_02_00](https://user-images.githubusercontent.com/67121125/158952747-510be783-d1ab-4886-9679-7ba8f1c0cd23.png)

### Importing a collection from an existing xlsx spreadsheet file (must manually input which headers the app should look up and import under "additional fields")
![VirtualBox_Xubuntu_18_03_2022_09_08_13](https://user-images.githubusercontent.com/67121125/158953748-85ddbae6-9c9c-4e9c-a4b5-5a7514e9c3c3.png)

### Uploading multiple image files and automatically linking them up with the correct item (user must choose which of the item's fields the images will refference and their file names must the same the contents of that respective field)
![VirtualBox_Xubuntu_18_03_2022_09_11_34](https://user-images.githubusercontent.com/67121125/158954262-85b7f194-629a-4e70-becb-ebcf62480863.png)



## Distinctiveness and Complexity

The main goal of for this web application was to create an inventory that is unrestrictive to the user and to what the user wants to store in it.
When a collection is being created the user can see it has 3 main fields added to it: Name, Description, Image. The user can add additional fields acording to the collection's needs, the number of fields and types of fields are up to the user. Later when an item is being registered to that collections, the forms that need to be filled in for that item represent the fields the user chose when creating that collection. This way each collection is able to store different kinds of items.

Considering the features detailed below, this project is sufficiently distinct from an e-commerce site or a social media site. It is also sufficiently complex because its database is being adapted to the user and not the other way around, it also provides options to automatically create large collections from existing xls files and options to export collections to xls files.

### Backend
Because I wanted these collections to be customizable, each additional field besides Name, Description will have it's own class inside models.py.
Image fields also have their own model class in order to allow an item to have multiple images.
For the purpose of sending a dictionary to the front end that communicates each "Field Name: Field Type" associated with a certain collection I've created a model class that acts as a dictionary called "FieldDict" and a model class for the name-type pair of a certain field called "FieldNameTypePair"; these are created along with the collection and will be used to communcate each collection's fields and their respective types to the front end in order to create forms.

When all these models come together they allow items to be highly customizable so that it is possible for 2 items from 2 different collections to have completely different attributes.

### Frontend
For the frontend I used Bootstrap 4, some google fonts and created my own javascript file to make the site dynamic.

The JavaScript file ended up being a lot larger than I planned with a lot of separate functions that all come together to help display everything.

There is a "Browse" button in the top navigation bar that sends a call to the backend and returns a dropdown list for all the collections created by the user.
There is a buttonless "Search" bar that sends a call to the backend and returns a list of all the items (from all the user's collections) whose names contain the characters entered in the searchbar.

Collection pages are created dynamically by the JavaScript file. When a collection is clicked the js functions work together to create a main area for the title which houses buttons and the filter area.

The filter area creates a dropdown menu for each field associated to the collection, and in each dropdown menu the options are a list of non repeating entries for that field taken from the database. When multiple filters are sellected from different fields, the other drop down menus will only show valid options taken from the already filtered items.
This way the user can filter the list of items using a combination of multiple filters and will never have a filter show an option that is not compatible to the other options.

Delete buttons trigger a separate confirmation button.

Items are displayed making use of Bootstrap's grid system and I've implemented an "infinite scroll" that only displays 20 items at a time and loads the rest after reaching the bottom of the page.

Each item is a link in the form of a bootstrap card and displays the item name and description (if there is one) along with either an image or an icon representing the lack of an image. Clicking an item card will trigger a modal (also using bootsrap) and will pop-up a new section where the user can see all the information related to that item along with an image carousel that can display all the images related to that item (if there are more than one). This modal pop-up also houses an edit button which will take the user to a different page where the item can be edited, and a delete button which removes the item, deletes all the model classes associated to it and removes the image files from the system.

### Extra Features

#### Import

The import button in the nav bar allows the user to import an XLS file and create a collection automatically from it. The user must make sure the fields entered in the import page will match the ones in the XLS table, and must make sure that the information type selected for those fields are relevant to the what the entries in the table are.

#### Upload multiple files to the collection

A way to automatically distribute multiple images amog multiple items inside a collection.
In the "Title" area of each collection there is a button called "Upload images". Here the user can upload multiple images at once and select which field should be used to distribute them. Using that field, all items whose field entries matches or partially maches the name of an image file will have that image attached to them.

#### Export to XLS

By clicking "Export to Excel" the backend will create an xls table of the current collection and the browser will download an XLS file on the user's computer.

## Created files

#### Static folder
keepItTidy.js - A javascript file containing various functions for DOM manipulation. This allows the application to be more dynamic and to build distinct froms and menus deppending on user created collections

styles.css - Various CSS settings to customize some prebuilt Bootstrap stylings

#### Templates folder
Several html files: a layout file from witch the others will inherit the overall layout of the site, some static html files that use Django templates, a mostly empty html file called view_collection.html that will act as a canvas for the javascript functions to work on.

#### Media follder
This folder contains a folder called "images" where the web application will store image files uploaded by the user and one icon PNG file for items that do not have images.
In models.py Django's delete method has been modified to not just delete the the objects in the data base but also to remove the image files associated to the item being deleted. Uploading multiple files at once also makes sure that image files will not be duplicated.


## How to run

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


## Prerequisites

- Python 3
- Django
- Pillow (used by Django for processing image files)
- SQLite3
- XLRD (used to read user uploaded XLS files in order to import data from them)
- XLWT (used to write xls files and allow the user to download an excel report in the browser for a specific collection)


## Acknowledgments

  - CS50???s Web Programming with Python and JavaScript course - https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript.
  - Strangers on stackoverflow.com that asked the right questions and those other ones that gave helpful answers.
  - Thank you anyone whose code is used by importing packages.
