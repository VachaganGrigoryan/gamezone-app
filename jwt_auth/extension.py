from inspect import isawaitable
from typing import Callable, Any, Set

from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate
from graphql import GraphQLResolveInfo
from strawberry.extensions import SchemaExtension
from strawberry.types import ExecutionContext, Info
from strawberry.utils.await_maybe import AwaitableOrValue

from jwt_auth.helper import get_context, get_http_authorization
from jwt_auth.auth import authenticate as authenticate_async


class BaseJwtExtension(SchemaExtension):
    """Base class for the JWT extension"""

    def __init__(self, execution_context: ExecutionContext):
        super().__init__(execution_context=execution_context)
        self.cached_allow_any: Set[Any] = set()

        self.user = None
        self.request = None

    def on_request_start(self) -> None:
        self.request = get_context(self.execution_context)
        # self.request = self.execution_context.context["request"]

    def resolve_base(self, info: GraphQLResolveInfo, *args: str, **kwargs: Any) -> None:
        print("Resolve base")

        return self.request

    @sync_to_async
    def _auth_header(self):
        print("Auth header")
        is_anonymous = not hasattr(self.request, "user") or self.request.user.is_anonymous
        return is_anonymous and get_http_authorization(self.request) is not None


class JwtExtension(BaseJwtExtension):
    """Sync version of the JWT extension"""

    def resolve(
        self,
        _next: Callable,
        root: Any,
        info: GraphQLResolveInfo,
        *args: str,
        **kwargs: Any,
    ) -> AwaitableOrValue[object]:
        print("Sync resolve")
        self.resolve_base(info, *args, **kwargs)

        if self._auth_header():
            self.user = authenticate(request=self.request, **kwargs)
            if self.user is not None:
                setattr(info.context, 'user', self.user)
                print("Authenticated")

        return _next(root, info, *args, **kwargs)


class AsyncJwtExtension(BaseJwtExtension):
    """Async version of the JWT extension"""

    async def resolve(
        self,
        _next: Callable,
        root: Any,
        info: GraphQLResolveInfo,
        *args: str,
        **kwargs: Any,
    ) -> AwaitableOrValue[object]:
        print("Async resolve")
        self.resolve_base(info, *args, **kwargs)

        if await self._auth_header():
            print("Authenticate async")
            self.user = await authenticate_async(request=self.request, **kwargs)
            if self.user is not None:
                setattr(info.context, 'user', self.user)
                print("Authenticated")

        result = _next(root, info, *args, **kwargs)
        print("result", result)
        if isawaitable(result):
            result = await result

        return result
