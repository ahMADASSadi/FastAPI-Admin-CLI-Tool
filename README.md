# FastAPI-Admin

Inspired by **Django** cli tool, **FastAPI-Admin** provides a well-structured, ready-to-use, and customizable interpreter tool that can make creating and maintaining FastAPI projects like a piece of Cake 🍰.

Note: The project has not yet been deployed on the PyPI for online installation, so you'll need to clone it and then install it using `pip install —e .` or any other method you choose.

After installation, you are all set to use it:

## Usage

At the moment, only two main below commands are implemented:

### 1. Creating a new project

To create a new project you only need simply to call:

```bash
fastapi-admin startproject [project_name] [project_directory]
```

- project_name:
    It's the name of your desired project and will create two sub-directories containing the main structure and necessary files.

- project_directory:
    Just the directory you want to start your project in!

Below is an example you might find usefull:

```bash
fastapi-admin startproject lets_rock .
```

The command above will start and create a project named "lets_rock" in the directory of "." which is the current working directory.
note that the "." is not necessary and its the **default** directory value.

### 2. Creating a new app

To create a new app you only need simply to call:

```bash
fastapi-admin startapp [app_name] [app_directory]
```

- app_name:
    It's the name of your desired project and will create two sub-directories containing the main structure and necessary files.

- app_directory:
    Just the directory you want to start your project in!

Below is an example you might find usefull:

```bash
fastapi-admin startapp queen 
```

The command above will create an app named "queen" in the current working directory.
Note that for this command to work, you must already created a project and run it in the same directory as the manage.py file is.


