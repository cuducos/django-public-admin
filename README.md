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

### Steps to test it with Jarbas

- [ ] Deleting Jarbas's `public_html` module
- [ ] Instantiate a `public_admin` in the `dashbaord.admin` module, something like `public_html.PublicAdminSite("dashboard", public_apps=("chamber_of_deputies",), public_models=("reimbursements",))`
- [ ] Add `public_admin.urls` to the `dashboard/urls.py`
