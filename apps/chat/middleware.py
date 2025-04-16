from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.conf import settings


class JWTAuthMiddleware(BaseMiddleware):
    """
    A WebSocket middleware to handle JWT authentication.
    It checks for a valid token in the Authorization header and attaches the authenticated user to the scope.
    """

    async def __call__(self, scope, receive, send):
        # Import these inside the method to avoid AppRegistryNotReady error
        from rest_framework_simplejwt.tokens import UntypedToken
        from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
        from django.contrib.auth import get_user_model
        from rest_framework_simplejwt.backends import TokenBackend

        User = get_user_model()

        @database_sync_to_async
        def get_user(validated_token):
            """
            This function retrieves the user from the database using the user_id from the JWT token.
            If the user doesn't exist, it returns an AnonymousUser.
            """
            try:
                user_id = validated_token["user_id"]
                return User.objects.get(id=user_id)
            except User.DoesNotExist:
                return AnonymousUser()

        # Look for the token in headers
        headers = dict(scope.get("headers", []))
        authorization_header = headers.get(b"authorization", b"").decode("utf-8")

        token = None
        # Check Authorization header first
        if authorization_header.startswith("Bearer "):
            token = authorization_header.split(" ")[1]
        else:
            # Fallback to query parameters if no Authorization header
            from urllib.parse import parse_qs

            query_string = scope["query_string"].decode()
            query_params = parse_qs(query_string)
            token_list = query_params.get("token", [])
            if token_list:
                token = token_list[0]

        if token:
            try:
                # Important: Provide the signing key from settings
                token_backend = TokenBackend(
                    algorithm="HS256", signing_key=settings.SECRET_KEY
                )

                # Validate the token
                validated_token = token_backend.decode(token, verify=True)

                # Attach the user to the scope if the token is valid
                scope["user"] = await get_user(validated_token)
            except (InvalidToken, TokenError) as e:
                # If the token is invalid, assign an AnonymousUser to the scope
                scope["user"] = AnonymousUser()
        else:
            # If no token is provided, assign an AnonymousUser to the scope
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
