# Info about the project:

This is the project for the startup portal.

To clone this repository keep the following things in mind :

1. Pull command will create a folder in the directory you run it in and initialise the repository inside that folder. So the directory will look like 'startupportal>repository pulled files>subdirectories..'
 
2. Once you pull the repository , navigate inside the initial folder that was created and create your virtual environment,by following the following steps.

Initial Setup Guidelines post cloning repository:

1.Create Virtual environment:
         virtualenv -p /usr/bin/python3 DESTINATION_FOLDER_NAME (if not created creates automatically.)
         Initiate environment by "source venv/bin/activate"

2.Install all required packages with 'pip install -r Requirements.txt'. You have to be in the directory where this file has been provided.

3.After installation, add the app names: 'material.admin' in the first line under INSTALLED_APPS in settings.py and then add 'material'.

4.Runserver and check if your admin site is functioning properly or not.

- If any package is being installed by you which will be needed by other contributors,please run the command 'pip freeze > Requirements.txt' and then push the changes--

- Note: Please make sure your have the gitignore files in your git home. Dont upload your settings.py file and other such system specific files. This will pollute the repository and create unwanted effects on every contributors machine.--  

Present contributing members:

## Administrators:

- Grappus team

- Site : www.grappus.com

## Development team:


- Debojit Kaushik - (email : kaushik.debojit@gmail.com)

- Saksham B.M Verenkar - (email : verenkar.saksham@gmail.com)
