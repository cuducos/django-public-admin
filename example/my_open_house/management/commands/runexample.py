from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.commands.runserver import Command as BaseCommand


class Command(BaseCommand):
    help = "Run migration, collect static files and start the server."

    def handle(self, *args, **options):
        if not settings.DATABASES["default"]["NAME"].exists():
            call_command("migrate")
            get_user_model().objects.create_user(
                "admin", password="admin", is_staff=True, is_superuser=True
            )

        call_command("collectstatic", interactive=False)
        super(Command, self).handle(*args, **options)
