"""
WSGI config for WifiATK project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import atexit

from django.core.wsgi import get_wsgi_application


def on_exit():
    #if 'runserver' in sys.argv or 'uwsgi' in sys.argv:
        # from wifiINFO.common import config as configer
    from wifiINFO.common import settings as configer

    config = configer.ConfigManager()
    # if wifiINFO.config.get_value('') is not None:
    #     # global host
    #     # global dnsmasq
    #     config.set(HOST_PID=None)
    config.on_exit()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WifiATK.settings')

atexit.register(on_exit)
application = get_wsgi_application()

