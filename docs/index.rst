Django Public Admin
===================

A public and read-only version of the `Django Admin <https://docs.djangoproject.com/en/3.0/ref/contrib/admin/>`_. A drop-in replacement for Django's native ``AdminSite`` and ``ModelAdmin`` for publicly accessible data.

How does it work
----------------

* `public_admin.sites.PublicApp` wraps Django apps and models you want to make public.
* `public_admin.sites.PublicAdminSite` works as a clone of Django's native `AdminSite`, but it looks at the HTTP request and the URL to decide whether they should exist in a public and read-only dashboard.
* `public_admin.admin.PublicModelAdmin` work as a clone of Django's native `ModelAdmin`, but what it does is to stop actions that would create, edit or delete objects.

Install
-------

::

    pip install django-public-admin

.. toctree::
   :maxdepth: 2
   :caption: Table of contents:

   usage
   example
   api

References
==========

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
