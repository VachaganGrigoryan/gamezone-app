import strawberry
from strawberry import auto

from django.contrib.auth import get_user_model
from account import models


@strawberry.django.type(models.User)
class UserType:
    guid: strawberry.ID
    first_name: auto
    last_name: auto
    email: auto
    profile: 'ProfileType'

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(is_superuser=False, is_active=True)


@strawberry.django.input(models.User)
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
