import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_chat_app.settings')
django.setup()  # Set up Django before importing any models

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from apps.chat.middleware import JWTAuthMiddleware
# Import your routing configuration
from apps.chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})