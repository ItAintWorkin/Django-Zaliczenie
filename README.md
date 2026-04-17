# QR code generator
A website to easily generate and save/download QR codes.

![The picture depicts a webpage to generate QR codes. On the left half is a text box labeled "Wpisz tekst" filled with the test "lorem ipsum". On the right side is the QR code corresponding to that input. Below the code is a clickable label "Download your QR". On the top of the webpage is the navigation bar with centered buttons: "Home", "QR Generator", "Your QRs", "Analyze (alpha)". On the far right of the nav bar are buttons: "Login" and "Sign Up". On the left side of the nav bar is a logo depicting dummy QR code behind portable electric generator. On the right of the logo is acronym "QRCG".](qr_generator.png "Preview of the generator webpage")

## Features:
- generating QR codes from text and links for up to 41 characters with up to 15% of damage recovery capacity! 
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


### Hot to set up a virtual environment and install dependencies (Linux):
Run `setup_project.sh`

## How to switch to a virtual environment in a terminal:

Run `.venv\Scripts\activate`. Then you will see (.venv) on the left from a CLI prompt

## How to install all dependencies in an env:

`python3 -m pip install -r requirements.txt`

For some Python versions installation might fail with ModuleNotFoundError: no module named 'distutils'. In that case necessary module can be obtained via command: `pip3 install setuptools`

## How to run local server:

Next get to the `webapp` directory: `cd webapp` and run `python3 manage.py startup` for migrations and admin account creaction (only during the first launch) from webapp folder and after that run `python3 manage.py runserver` in the same folder

*In some enviroments it could be not `python3` but `python`* 

## How to Quit the server:

Quit the server with CTRL-C in command line

## Admin account information:

- Login: admin1
- Password: admin1
- Other accounts can be created via the register page.


## Description of project’s structure:
The project was built using the Django framework and is divided into the following components:                 
### main
Main system app, responsible for:
- view handling (views)
- models logic (models)
- routing URL (urls)
- users system (login, register)
- rendering HTML templates

Additionally contains:
- custom Django command (startup.py), which can automatically run operations when the project is started
- static files (CSS, images)
- HTML templates
### qrgenerator:
Module responsible for creating QR codes:
- qrcode.py – main logic of generator and serialization
- export.py  –  export / saving generated QR codes
- bitarray.py - class for manipulating individual bits in bytearray
- tables_and_enums.py - constants from the specification extracted for clarity of code
