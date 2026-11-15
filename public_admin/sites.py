from collections.abc import Callable, Iterable, Sequence
from functools import update_wrapper
from importlib import import_module
from typing import Any, Literal

from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import AnonymousUser
from django.db.models import Model
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.urls.resolvers import URLPattern, URLResolver
from django.views.decorators.csrf import csrf_protect

from public_admin.exceptions import UnauthorizedModelError

try:
    import_module("import_export.admin")
    HAS_IMPORT_EXPORT = True
except ImportError:
    HAS_IMPORT_EXPORT = False


class PublicApp:
    """Holds the permission strings for each model in a Django app. `name`
    should be the name of a Django app as string, and `models` should be a
    sequence of strings with the name of the models to allowed in a public
    admin."""

    def __init__(self, name: str, models: Iterable[str]) -> None:
        self.name = name
        self.permissions: tuple[str, ...] = tuple(
            f"{name}.view_{model}" for model in models
        )


class DummyUser(AnonymousUser):
    """Mimics the Django's native `AnonymousUser` injecting permissions to view
    objects from certain Django apps and models.`pubic_apps` should be a
    sequence of instances of `public_admin.sites.PublicApp`."""

    def __init__(
        self, public_apps: Iterable[PublicApp], *args: Any, **kwargs: Any
    ) -> None:
        self.public_apps: set[str] = set(app.name for app in public_apps)
        self.permissions: set[str] = set(
            permission.lower()
            for public_app in public_apps
            for permission in public_app.permissions
        )
        super().__init__(*args, **kwargs)

    def has_module_perms(self, module: str) -> bool:
        """Only grant permission if the `app` was passed as a
        `public_admin.sites.PublicApp`."""
        return module in self.public_apps

    def has_perm(self, perm: str, obj: Model | None = None) -> bool:
        """Only grant permission if the app and model were passed in a
        `public_admin.sites.PublicApp`."""
        return perm.lower() in self.permissions


class PublicAdminSite(AdminSite):
    """Mimics the Django's native `AdminSite` but removing URLs and permissions
    that does not match the idea of a public admin. `name` is the name of this
    admin site (the string Django uses to build the URL names, for example),
    and `pubic_apps` can be one instance of `public_admin.sites.PublicApp` or a
    sequence of them."""

    def __init__(
        self,
        name: str = "public_admin",
        public_apps: PublicApp | Sequence[PublicApp] = (),
    ) -> None:
        super().__init__(name=name)
        self._actions, self._global_actions = {}, {}

        if isinstance(public_apps, PublicApp):
            public_apps = (public_apps,)
        self.dummy_user = DummyUser(public_apps)
        self._export_url_names: set[str] = set()

    @staticmethod
    def valid_url(url: URLResolver | URLPattern) -> bool:
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
    def urls(self) -> tuple[list[URLResolver | URLPattern], Literal["admin"], str]:
        """List the URLs in this admin site."""
        urls = (url for url in self.get_urls() if self.valid_url(url))
        return list(urls), "admin", self.name

    def has_permission(self, request: HttpRequest) -> bool:
        """Blocks all non-GET requests, except POST requests to export views
        registered by Django import / export (its export form only reads
        data)."""
        if request.method == "GET":
            return True

        if not HAS_IMPORT_EXPORT:
            return False

        name = getattr(request.resolver_match, "url_name", None)
        return (
            name is not None
            and request.method == "POST"
            and name in self._export_url_names
        )

    def admin_view(self, view: Callable[..., HttpResponse], cacheable: bool = False):
        """Injects the `public_admin.sites.DummyUser` in every request in this
        admin site."""

        def inner(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            setattr(request, "user", self.dummy_user)
            if not self.has_permission(request):
                return HttpResponseForbidden()
            return view(request, *args, **kwargs)

        if getattr(view, "csrf_exempt", False):
            return update_wrapper(inner, view)
        return update_wrapper(csrf_protect(inner), view)

    def register(
        self,
        model_or_iterable: type[Model],
        admin_class: type[ModelAdmin] | None = None,
        **options: Any,
    ) -> None:
        """Verifies whether the model about to be registered is allowed in this
        public admin site"""
        meta = getattr(model_or_iterable, "_meta")
        permission = f"{meta.app_label}.view_{meta.model_name}"
        if not self.dummy_user.has_perm(permission):
            msg = f"{meta.object_name} is not listed in this public app."
            raise UnauthorizedModelError(msg)
        super().register(model_or_iterable, admin_class)

        # permissions are based on the model admin class and not on URL names
        # (which anyone can choose in `get_urls`)
        model_admin = self._registry[model_or_iterable]
        if HAS_IMPORT_EXPORT:
            from import_export.admin import ExportMixin, ImportMixin

            if isinstance(model_admin, ExportMixin):
                name = "%s_%s_export" % model_admin.get_model_info()
                self._export_url_names.add(name)

            # set in the instance because the import / export mixins come before
            # `PublicModelAdmin` in the MRO, so an override there would never run
            if isinstance(model_admin, ImportMixin):
                model_admin.has_import_permission = lambda request: False
