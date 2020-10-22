from functools import update_wrapper

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_protect

from public_admin.exceptions import UnauthorizedModelError


class PublicApp:
    """Holds the permission strings for each model in a Django app. `name`
    should be the name of a Django app as string, and `models` should be a
    sequence of strings with the name of the models to allowed in a public
    admin."""

    def __init__(self, name, models):
        self.name = name
        self.permissions = tuple(f"{name}.view_{model}" for model in models)


class DummyUser(AnonymousUser):
    """Mimics the Django's native `AnonymousUser` injecting permissions to view
    objects from certain Django apps and models.`pubic_apps` should be a
    sequence of instances of `public_admin.sites.PublicApp`."""

    def __init__(self, public_apps, *args, **kwargs):
        self.public_apps = set(app.name for app in public_apps)
        self.permissions = set(
            permission.lower()
            for public_app in public_apps
            for permission in public_app.permissions
        )
        super().__init__(*args, **kwargs)

    def has_module_perms(self, app_label):
        """Only grant permission if the `app` was passed as a
        `public_admin.sites.PublicApp`."""
        return app_label in self.public_apps

    def has_perm(self, permission, obj=None):
        """Only grant permission if the app and model were passed in a
        `public_admin.sites.PublicApp`."""
        return permission.lower() in self.permissions


class PublicAdminSite(AdminSite):
    """Mimics the Django's native `AdminSite` but removing URLs and permissions
    that does not match the idea of a public admin. `name` is the name of this
    admin site (the string Django uses to build the URL names, for example),
    and `pubic_apps` can be one instance of `public_admin.sites.PublicApp` or a
    sequence of them."""

    def __init__(self, name="public_admin", public_apps=()):
        super().__init__(name=name)
        self._actions, self._global_actions = {}, {}

        if isinstance(public_apps, PublicApp):
            public_apps = (public_apps,)
        self.dummy_user = DummyUser(public_apps)

    @staticmethod
    def valid_url(url):
        """This method removes URLs based on their path."""
        forbidden = (
            "auth",
            "login",
            "logout",
            "password",
            "add",
            "delete",
        )
        return all(label not in url.pattern.regex.pattern for label in forbidden)

    @property
    def urls(self):
        """List the URLs in this admin site."""
        urls = (url for url in self.get_urls() if self.valid_url(url))
        return list(urls), "admin", self.name

    def has_permission(self, request):
        """Blocks all non-GET requests."""
        return request.method == "GET"

    def admin_view(self, view, cacheable=False):
        """Injects the `public_admin.sites.DummyUser` in every request in this
        admin site."""

        def inner(request, *args, **kwargs):
            request.user = self.dummy_user
            if not self.has_permission(request):
                return HttpResponseForbidden()
            return view(request, *args, **kwargs)

        if not getattr(view, "csrf_exempt", False):
            inner = csrf_protect(inner)

        return update_wrapper(inner, view)

    def register(self, model, admin_class=None, **options):
        """Verifies whether the model about to be registered is allowed in this
        public admin site"""
        permission = f"{model._meta.app_label}.view_{model._meta.model_name}"
        if not self.dummy_user.has_perm(permission):
            msg = f"{model._meta.object_name} is not listed in this public app."
            raise UnauthorizedModelError(msg)
        return super(PublicAdminSite, self).register(model, admin_class)
