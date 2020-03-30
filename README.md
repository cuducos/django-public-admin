# _Draft_ for Django Public Admin

A public and read-only version of the [Django Admin](https://docs.djangoproject.com/en/3.0/ref/contrib/admin/). A drop-in replacement for Django's native `AdminSite` and `ModelAdmin` for publicly acessible data.

## Instructions — _they do not work, but are helpful in the API-driven design mindset_

### Install

> As this package is not finished nor published, this command does not work just yet. However, [Poetry](https://python-poetry.org/) should install it in the local _virtualenv_ one can access with `poetry shell`.

```console
$ pip install django-public-admin
```

### Create your _Django Public Admin_ instance

Just like one would create a regular `admin.py`, you can create a module using _Django Public Admin_'s `PublicAdminSite` and `PublicModelAdmin`:

```python
from public_admin.sites import PublicAdminSite, PublicModelAdmin

from my_website.my_open_house.models import Beverage, Snack


class BeverageModelAdmin(PublicModelAdmin):
    pass


class SnackModelAdmin(PublicModelAdmin):
    pass


public_admin = PublicAdminSite(
    "dashboard",  # you name it as you wish
    public_apps=("my_open_house",),  # all your apps that can be public accessible
    public_models=("beverage", "snack")  # all your models from those apps that can be public accessible
)
public_admin.register(Beverage, BeverageModelAdmin)
public_admin.register(Sanck, SanckModelAdmin)
```

### Add your _Django Public Admin_ URLs

In your `urls.py`, import the `public_html` (or whatever you've named it earlier) in your URLs file and create the endpoints:

```python
from django.urls import path

from my_website.my_open_house.admin import public_admin


url = [
    # …
    path("dashboard/", public_admin.urls)
]
```
