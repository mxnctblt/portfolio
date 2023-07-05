## This folder contains all the files of a Django app.

| File          | Usage         |
| ------------- |:-------------:|
| `migrations/`     | This directory contains database migration files. Migrations are used to manage database schema changes over time. Each migration file represents a set of changes and allows for seamless database schema updates. |
| `__init__.py` | This file is a Python package file. Its presence in a directory indicates that the directory is a Python package. In the context of a Django project, `__init__.py` files are typically empty or may contain some initialization code. They allow the directory to be recognized as a package, enabling you to import modules and files from that directory. |
| `admin.py`     | This file is used to configure the Django admin interface. It allows you to define the administration options for your models, specify custom admin views, and customize the appearance of the admin site.  |
| `apps.py` | This file is present in each Django application within a project. It is responsible for application-specific configuration. It contains the configuration class for the application, which inherits from django.apps.AppConfig. This class allows us to customize various aspects of the application, such as its name. |
| `functions.py`     | This file contains the functions for link conversions & getting a hashtag used in our views |
| `models.py`     | This file defines the database models for our application. Models are Python classes that represent database tables and encapsulate the data access and manipulation logic. They define the fields, relationships, and methods associated with the data. |
| `tests.py`     | This file is used for writing tests for your Django application. Django provides a testing framework that allows us to create and run tests to ensure the correctness of our application's functionality. |
| `urls.py`     | This file defines the URL patterns for our project. It maps URLs to views or other URL patterns using regular expressions or path converters. It acts as a routing configuration for our web application. |
| `views.py`     | This file contains the views or functions that handle HTTP requests and return HTTP responses. Views define the logic for rendering templates, processing form data, interacting with models, and more. |