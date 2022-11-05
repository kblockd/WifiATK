#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import atexit


def exit_status():
    if 'runserver' in sys.argv:
        os.remove('run.pid')


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WifiATK.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    atexit.register(exit_status)
    main()