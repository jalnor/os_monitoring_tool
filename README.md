

# OS Monitoring Tool ![python-powered-w-70x28](https://user-images.githubusercontent.com/31383711/190922610-d309b96e-318e-4e82-9b04-8eb2ab52938d.png)
---

A Python tool that monitors processes as they start and stop. It utilizes a separate subprocess to capture the current running processes, compares those to the database and adds the process or updates its status. It features graphs created with matplotlib and calls to an API for information about the process. OS Monitor Tool uses Tkinter for the GUI!

## System Requirements
---
* Python 3.10, see [PYTHONINSTALL.md](PYTHONINSTALL.md) for detailed instructions.
* Poetry 1.1.15 or
* Pip (Which comes with Python)
* Database (Sqlite is the default but if you want to use another DBMS you can find instructions in the [.env-template](https://github.com/jalnor/os_monitoring_tool/blob/main/.env-template) file)


### Poetry Installation
Per the [documentation](https://python-poetry.org/docs/), Poetry is a dependency management and packaging tool.

##### Note: You can follow the instructions on their [website](https://python-poetry.org/docs/) to install poetry.
##### Note: Make sure to follow the instructions for activating the virtual environment in the PYTHONINSTALL.md file before continuing.
To install the requirements for the app type:

``` poetry install ```

and poetry will install all the dependencies listed in the project.lock file.

If you are planning on developing this app further, it is easy to add new dependencies, build, and package your application. A simple example of adding a dependency is:

``` poetry add requests ```

This will pull in all the dependencies required for the requests package and add them to the poetry.lock and .toml files.

Now you are ready to setup your .env file. You need to create this file in the root directory of the project. There is a template provided that shows what needs to be added to the .env file.
This includes the url for which database you are using. Also, be sure to copy over the subprocess and web_lookup just as they appear as those are needed for the app to run properly.


Once the dependencies are installed and the .env file are in place, you can run the app.

``` poetry run python main.py```

That is it, the app should be up and running at this point, capturing, and saving the processes running on your computer.

https://user-images.githubusercontent.com/31383711/199861204-d952435a-8b1f-4d94-84d1-3ee60422d523.mp4


