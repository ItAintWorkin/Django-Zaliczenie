# QR code generator
The website to easily generate and save/download QR codes.

## Features:
- generating QR codes from text and links for up to 41 characters
- library of saved QR codes (for logged in only)
- option to download generated or saved QR code

## Technologies used:

- Python 3
- Django
- HTML / CSS
- SQLite

## Build instructions: 

PyCharm will prepare the virtual environment for project automatically. For non-PyCharm users (for example VSCode) look an instructions below how to do this manually

## How to set up a virtual environment:


`python3 -m venv .venv` and then select new environment in a VSCode (bottom-right corner)

## How to switch to a virtual environment in a terminal:

Run `.venv\Scripts\Activate`. Then you will see (.venv) on the left from a CLI prompt

## How to install all dependencies in an env:

`pip3 install -r requirements.txt`

For some Python versions installation might fail with ModuleNotFoundError: no module named 'distutils'. In that case necessary module can be obtained via command: `pip3 install setuptools`

## How to run local server:

Next get to the `webapp` directory: `cd webapp` and run `python3 manage.py startup` for migrations and admin account creaction (only during the first launch) from webapp folder and after that run `python3 manage.py runserver` in the same folder

*In some enviroments it could be not `python3` but `python`* 

## How Quit the server :

Quit the server with CTRL-C in command line

## Admin account information:

Login: admin1
Password: admin1
Other accounts can be created via the register page.


## Description of project’s structure
The project was built using the Django framework and is divided into the following components:                 
# main
Main system app, responsible for:
-view handling (views)
-models logic (models)
-routing URL (urls)
-users system (login, register)
-rendering HTML templates

Additionally contains:
-custom Django command (startup.py), which can automatically run operations when the project is started
-static files (CSS, grafiki)
-HTML templates
# qrgenerator
Module responsible for creating QR codes:
-qrcode.py – QR code generator
-export.py  –  export / saving generated QR codes
