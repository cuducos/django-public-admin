Example
=======

There is an example app in `Django Public Admin repository <https://github.com/cuducos/django-public-admin/>`_, inside the ``example/`` directory. This example is meant to be a straightforward use case, having *Django's native admin* running in parallel with *Django Public Admin*.

Requirements
------------

* Git
* Python 3.6 or newer with `Poetry <https://python-poetry.org>`_ (or other `PEP 517 <https://www.python.org/dev/peps/pep-0517/>`_ `pyproject.toml` compatible tool)

Running the example
-------------------

First, clone the repository and install the dependencies:

::

    git clone https://github.com/cuducos/django-public-admin.git
    poetry install

Then start the application:

::

    poetry run python example/manage.py runexample

The ``runexample`` command is a wrapper around Django's native ``runserver``. It creates a temporary SQLite database, run migrations, creates a superuser, and collects static files *automagically* before spinning up the development server. If you are having trouble with this command, you can try to delete all these temporary files with ``poetry run python manage.py cleanexample``.

Once the application is up and running, you can:

* Access the *Django's native admin*, **password protected** (username is ``admin`` and password is also ``admin``) at `localhost:8000/admin <http://localhost:8000/admin/>`_
* Access the *Django Public Admin*, with **no login needed** at `localhost:8000/dashboard <http://localhost:8000/dashboard/>`_

You can add and edit data at ``admin/``, while non-logged-in users can browse data at ``dashboard/`` with all the filters and perks of a Django Admin instance!
