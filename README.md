# Django Public Admin

A public and read-only version of the [Django Admin](https://docs.djangoproject.com/en/3.0/ref/contrib/admin/). A drop-in replacement for Django's native `AdminSite` and `ModelAdmin` for publicly accessible data.

## How does it work

1. `PublicAdminSite` works as a clone of Django's native `AdminSite`, but it looks at the HTTP request and the URL to decide whether they should exist in a public and read-only dashboard.
1. `PublicModelAdmin` work as a clone of Django's native `ModelAdmin`, but what it does is to stop actions that would create, edit or delete objects.
1. `DummyUser` is just a an implementation detail, since Django requires an user to process the requests.

## Install

> As this package is not finished nor published, this command does not work just yet. However, [Poetry](https://python-poetry.org/) should install it in the local _virtualenv_ one can access with `poetry shell`.

```console
$ pip install django-public-admin
```

## Usage

### 1. Create your _Django Public Admin_ instance

Just like one would create a regular `admin.py`, you can create a module using _Django Public Admin_'s `PublicAdminSite` and `PublicModelAdmin`:

```python
from public_admin.admin import PublicModelAdmin
from public_admin.sites import PublicAdminSite, PublicApp

from my_website.my_open_house.models import Beverage, Snack


class BeverageModelAdmin(PublicModelAdmin):
    pass


class SnackModelAdmin(PublicModelAdmin):
    pass


public_app = PublicApp("my_open_house", models=("beverage", "snack"))
public_admin = PublicAdminSite(
    "dashboard",  # you name it as you wish
    public_app,  # this can be a single public app or a sequence of public apps
)
public_admin.register(Beverage, BeverageModelAdmin)
public_admin.register(Sanck, SanckModelAdmin)
```

### 2. Add your _Django Public Admin_ URLs

In your `urls.py`, import the `public_html` (or whatever you've named it earlier) in your URLs file and create the endpoints:

```python
from django.urls import path

from my_website.my_open_house.admin import public_admin


url = [
    # …
    path("dashboard/", public_admin.urls)
]
```

### 3. Templates

_Django Public Admin_ comes with a template that hides from the UI elements related to user, login and logout. To use it, add `public_admin` to your `INSTALLED_APPS` **before** `django.contrib.admin`:

```python
INSTALLED_APPS = [
    "public_admin",
    "django.contrib.admin",
    # ...
]
```

If you decide not to use it, you have to create your own `templates/base.html` to avoid errors when rendering the template. Django will fail, for example, in rendering URLs that do not exist, which would be the case for login and logout.

## Contributing

We use `tox` to Run tests with Python 3.6, 3.7 and 3.8, and with Django 2 and 3. Also we use Black and `flake8`:

```console
$ poetry install
$ poetry run tox
```

## License & Credits

This package is licensed under [MIT license](/LICENSE) and acknowledge [Serenata de Amor](https://github.com/okfn-brasil/serenata-de-amor) (© [Open Knowledge Brasil](https://br.okfn.org) and, previously, © [Data Science Brigade](https://github.com/datasciencebr)).
