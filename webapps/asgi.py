"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import channels.asgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapps.settings")
channel_layer = channels.asgi.get_channel_layer()