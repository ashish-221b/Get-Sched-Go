#!/usr/bin/env python
import os
import sys
"""@package django
 This is the main driver program which runs and make calls to all other sub-applications mentioned in setting.py
 @details starts the server is runserver is called. It's function depends on arguments provided in it's call

 More Details
 @link https://docs.djangoproject.com/en/1.11/ref/django-admin/#django-admin-and-manage-py
"""
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "getSchedGo.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
