from rest_framework.authtoken.models import Token
from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async


@database_sync_to_async
def gettoken(headers):
    if b'authorization' in headers:
        try:
            token_name, token_key = headers[b'authorization'].decode(
            ).split()
            if token_name == 'Token':
                token = Token.objects.get(key=token_key)
                return token.user
        except Token.DoesNotExist:
            return AnonymousUser()
    else:
        return AnonymousUser()


class TokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])        
        scope['user'] = await gettoken(headers)

        return await self.inner(scope, receive, send)


def TokenAuthMiddlewareStack(inner): return TokenAuthMiddleware(
    AuthMiddlewareStack(inner))
