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

Before first launch you need to follow steps below.

### Automatic project setup (Linux):

Run the `setup_project.sh` script before first launch.

### Manual setup:

Open terminal/command prompt in the project's root directory and run these commands: 
```
python3 -m venv .venv
.venv\Scripts\activate
python3 -m pip install -r requirements.txt
cd webapp
python3 manage.py startup
```

## How to run local server:

### VS Code:
Click F5 and run the `runserver` launch configuration.

### PyCharm
Run the `runserver` run configuration.

### other/terminal
On Linux - launch the `runserver.sh` script.

On Windows - open project's root directory and run these commands:
```
.venv\Scripts\activate
python3 webapp\manage.py runserver
```

*In some enviroments it could be not `python3` but `python`* 

## How to Quit the server:

Quit the server with CTRL-C in command line.
If the server was started using launch configuration for PyCharm or VSCode you can close the server by clicking the red square symbol.  

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
