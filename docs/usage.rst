Usage
=====

Declare which apps and models you want to make public
-----------------------------------------------------

Let's say you have a Django app called ``my_open_house`` with models ``beverage`` and ``snack`` that you want their data to de public. Use `public_admin.sites.PublicApp` to declare that:

::

    from public_admin.sites import PublicApp
    
    public_app = PublicApp("my_open_house", models=("beverage", "snack"))

Create your *Django Public Admin* instance
-------------------------------------------

Just like one would create a regular ``admin.py``, you can create a module `public_admin.sites.PublicAdminSite` and `public_admin.admin.PublicModelAdmin`:

::

    from public_admin.sites import PublicAdminSite, PublicApp
    

    public_app = PublicApp("my_open_house", models=("beverage", "snack"))
    public_admin = PublicAdminSite("dashboard", public_app)

The first argument is the name of this site in Django, and the second argument can be a single instance of `public_admin.sites.PublicApp` or a sequence of them.

Create and register your ``PublicModelAdmin``
---------------------------------------------

::

    from public_admin.admin import PublicModelAdmin

    from my_open_house.models import Beverage, Snack
    
    
    class BeverageModelAdmin(PublicModelAdmin):
        # ...


    class SnackModelAdmin(PublicModelAdmin):
        # ...


    public_admin.register(Beverage, BeverageModelAdmin)
    public_admin.register(Sanck, SanckModelAdmin)

Add your *Django Public Admin* URLs
-----------------------------------

In your ``urls.py``, import the `public_admin` (or whatever you've named it earlier) in your URLs file and create the endpoints:

::

    from django.urls import path

    from my_website.my_open_house.admin import public_admin


    url = [
        # …
        path("dashboard/", public_admin.urls)
    ]

Templates
---------

*Django Public Admin* comes with a template that hides from the UI elements related to user, login and logout. To use it, add ``"public_admin"`` to your ``INSTALLED_APPS`` **before** ``django.contrib.admin``:

::

    INSTALLED_APPS = [
        "public_admin",
        "django.contrib.admin",
        # ...
    ]

**If you decide not to use this template**, you have to create your own ``templates/admin/base.html`` file to avoid errors when rendering the template. Django will fail, for example, in rendering URLs that do not exist, which would be the case for login and logout.

