from functools import update_wrapper

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_protect


class PublicApp:
    def __init__(self, name, models):
        self.name = name
        self.permissions = tuple(f"{name}.view_{model}" for model in models)


class DummyUser(AnonymousUser):
    def __init__(self, public_apps, *args, **kwargs):
        self.public_apps = set(app.name for app in public_apps)
        self.permissions = set(
            permission
            for public_app in public_apps
            for permission in public_app.permissions
        )
        super().__init__(*args, **kwargs)

    def has_module_perms(self, app_label):
        return app_label in self.public_apps

    def has_perm(self, permission, obj=None):
        return permission in self.permissions


class PublicAdminSite(AdminSite):
    def __init__(self, name="public_admin", public_apps=()):
        super().__init__(name=name)
        self._actions, self._global_actions = {}, {}

        if isinstance(public_apps, PublicApp):
            public_apps = (public_apps,)
        self.dummy_user = DummyUser(public_apps)

    @staticmethod
    def valid_url(url):
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
        urls = (url for url in self.get_urls() if self.valid_url(url))
        return list(urls), "admin", self.name

    def has_permission(self, request):
        return request.method == "GET"

    def admin_view(self, view, cacheable=False):
        def inner(request, *args, **kwargs):
            request.user = self.dummy_user
            if not self.has_permission(request):
                return HttpResponseForbidden()
            return view(request, *args, **kwargs)

        if not getattr(view, "csrf_exempt", False):
            inner = csrf_protect(inner)

        return update_wrapper(inner, view)
