# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import os
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'public_admin',
    'tests'
)

DEFAULT_FILE_STORAGE = 'tests.storage.MyFileSystemStorage'

SECRET_KEY = 'foobar'
