[![PyPI](https://img.shields.io/pypi/v/django-public-admin)](https://pypi.org/project/django-public-admin/) [![Documentation Status](https://readthedocs.org/projects/django-public-admin/badge/?version=latest)](https://django-public-admin.readthedocs.io/en/latest/?badge=latest) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-public-admin)](https://pypi.org/project/django-public-admin/) [![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-public-admin)](https://pypi.org/project/django-public-admin/)

# Django Public Admin


A public and read-only version of the [Django Admin](https://docs.djangoproject.com/en/3.0/ref/contrib/admin/). A drop-in replacement for Django's native `AdminSite` and `ModelAdmin` for publicly accessible data. Check the [documentation](https://django-public-admin.readthedocs.io/en/latest/?badge=latest) for more information on how to use it.

## Contributing

We use `tox` to Run tests with Python 3.6, 3.7 and 3.8, and with Django 2 and 3. Also we use Black and `flake8`:

```console
$ poetry install
$ poetry run tox
```

### Docs

To build the docs we use [Sphinx](https://www.sphinx-doc.org/en/):

```
$ poetry run sphinx-build docs docs/_build/
```

Them just jump to `docs/_build/index.html`.

## License & Credits

This package is licensed under [MIT license](/LICENSE) and acknowledge [Serenata de Amor](https://github.com/okfn-brasil/serenata-de-amor) (© [Open Knowledge Brasil](https://br.okfn.org) and, previously, © [Data Science Brigade](https://github.com/datasciencebr)).
