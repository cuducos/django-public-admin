from django.core.exceptions import ImproperlyConfigured


class UnauthorizedModelError(ImproperlyConfigured):
    """The registered model isn't listed in the public app"""

    pass
