# QR code generator
The website to easily generate QR codes.
## Features:
 - ~~generating QR codes from text~~ [ TODO ]
 - ~~generation history (after log in)~~ [ TODO ]
 - ~~ability to choose any of the 8 masks depending on application conditions~~ [ TODO ]
 - ~~image embedding in code~~ [ TODO ]
 - ~~REST API for fetching the codes from terminal or other programs~~ [ to be suggested 😭]

## Build instructions: 

PyCharm will prepare the virtual environment for project automatically. For non-PyCharm users (for example VSCode) look an instructions below how to do this manually

## How to run local server
Get to the `webapp` directory: `cd webapp` and run `python3 manage.py runserver` from webapp folder

*In some enviroments it could be not `python3` but `python`* 


### How to set up a virtual environment:

`python3 -m venv .venv` and then select new environment in a VSCode (bottom-right corner)

### How to switch to a virtual environment in a terminal

Run `.venv\Scripts\Activate`. Then you will see (.venv) on the left from a CLI prompt

### How to install all dependencies in an env

`pip3 install -r requirements.txt`

For some Python versions installation might fail with `ModuleNotFoundError: no module named 'distutils'`.
In that case necessary module can be obtained via command:

`pip3 install setuptools`

### How Quit the server :
Quit the server with CTRL-C in command line

## Happy coding!
