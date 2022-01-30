import graphene
from graphene import ObjectType
from graphene_django.types import DjangoObjectType
from account.models import User, Profile


class UserType(DjangoObjectType):
    class Meta:
        model = User


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile


class UserQuery(ObjectType):
    pass