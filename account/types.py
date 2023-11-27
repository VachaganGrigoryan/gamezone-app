from typing import List

import strawberry
from jwtberry.permission import IsAuthenticated
from strawberry import auto

from django.contrib.auth import get_user_model
from account import models


@strawberry.django.type(get_user_model())
class UserType:
    guid: strawberry.ID
    email: auto
    profile: 'ProfileType'

    @strawberry.field()
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(is_superuser=False, is_active=True)


@strawberry.django.input(get_user_model())
class UserInput:
    first_name: auto
    last_name: auto
    email: auto
    password: auto


@strawberry.django.type(models.Profile)
class ProfileType:
    avatar: str
    banner: str

    bio: str
    address: str
    country: str
    region: str
    city: str
    zip_code: str

    created_at: str
    updated_at: str


@strawberry.type
class AccountQuery:

    @strawberry.field(permission_classes=[IsAuthenticated])
    def me(self, info) -> UserType:
        return info.context.user

    # user: UserType = strawberry.django.field()
    # users: List[UserType] = strawberry.django.field()
