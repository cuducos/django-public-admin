from shutil import rmtree

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Cleans up temporary files from previous runs (e.g.: SQLite database "
        "file and staticfiles directory)."
    )

    def handle(self, *args, **options):
        if settings.TMP_DIR.exists():
            rmtree(settings.TMP_DIR)
