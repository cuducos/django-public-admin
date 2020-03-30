# Draft for Django Public Admin

A public and read-only version of the [Django Admin](https://docs.djangoproject.com/en/3.0/ref/contrib/admin/).

## TODO list

- [ ] Make `pytest` run (maybe using `pytest-django`)
- [ ] Make tests pass
- [ ] Manual test (for example, replace [Jarbas](https://github.com/okfn-brasil/serenata-de-amor/tree/master/jarbas)'s `jarbas.public_html` by this module):
    - [ ] Spin up a Django application locally
    - [ ] Use Poetry to build a installable version of this package `django-public-admin`
    - [ ] Install this package `django-public-admin`
    - [ ] Test is it really works (document how to wire up things so we have instructions to add here)

## Instructions

1. Install this package
2. Import it in your `admin.py`: `from public_admin.sites import PublicAdminSite`
3. Create a `PublicAdminSite` instance with the name of your apps and models to be publicly accessible, for example: `public_admin = PublicAdminSite("dashboard", public_apps=("chamber_of_deputies",), public_models=("reimbursements",))`
4. Import the instance you just created in your `urls.py` to create the endpoints, for example: `path('dashboard/', public_admin.urls)`
