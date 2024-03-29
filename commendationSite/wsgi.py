"""
WSGI config for commendationSite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "commendationSite.settings")
load_dotenv(BASE_DIR / ".env")

application = get_wsgi_application()
