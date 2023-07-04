from typing import Optional, List, Annotated, Union

import strawberry

from django.contrib.auth.models import AbstractUser, Group, Permission


@strawberry.type
class TokenType:
    access: str
    refresh: str


@strawberry.type
class AuthenticationFailed:
    detail: str
    code: str
    # data: Optional[dict] = None


JwtAuthResponse = Annotated[
    Union[TokenType, AuthenticationFailed],
    strawberry.union("JwtAuthResponse", types=[TokenType, AuthenticationFailed]),
]


@strawberry.django.type(Permission)
class PermissionType:
    name: str
    codename: str


@strawberry.django.type(Group)
class GroupType:
    name: str
    permissions: Optional[List[PermissionType]] = None


@strawberry.django.type(AbstractUser)
class UserType:
    pk: strawberry.ID
    username: str
    email: str
    is_staff: bool = False
    is_active: bool = True
    is_superuser: bool = False
    is_authenticated: bool = False
    groups: Optional[List[GroupType]] = None
    user_permissions: Optional[List[PermissionType]] = None
