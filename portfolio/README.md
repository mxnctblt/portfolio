## This folder contains all the files of a Django project.

| File          | Usage         |
| ------------- |:-------------:|
| `__init__.py` | This file is a Python package file. Its presence in a directory indicates that the directory is a Python package. In the context of a Django project, `__init__.py` files are typically empty or may contain some initialization code. They allow the directory to be recognized as a package, enabling you to import modules and files from that directory. |
| `asgi.py`     | This file is used in Django projects that utilize the ASGI (Asynchronous Server Gateway Interface) protocol. ASGI is a standard interface for Python web applications to communicate with web servers or other ASGI-compatible applications. In the `asgi.py` file, we configure the ASGI application for our Django project, specifying the application instance to be used by the ASGI server. |
| `settings.py` | This file contains the configuration settings for your Django project. It includes settings related to the database, static files, middleware, installed applications, and more. |
| `urls.py`     | This file defines the URL patterns for our project. It maps URLs to views or other URL patterns using regular expressions or path converters. It acts as a routing configuration for our web application. |
| `wsgi.py`     | This file is used in Django projects that utilize the WSGI (Web Server Gateway Interface) protocol. WSGI is a standard interface that allows web servers to communicate with web applications written in Python. In the `wsgi.py` file, we configure the WSGI application for our Django project, specifying the application instance to be used by the WSGI server. |

Both `asgi.py` and `wsgi.py` files serve as entry points for the respective server protocols (ASGI and WSGI). They create the application object and handle the server's communication with the Django project.

These files are automatically generated by the startproject management command when you create a new Django project.

Since we did not use ASGI and WSGI, both files are empty.
