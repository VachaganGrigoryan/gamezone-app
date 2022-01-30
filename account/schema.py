import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from account.models import User, Profile


class UserType(DjangoObjectType):
    class Meta:
        model = User


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile


class Query(ObjectType):
    pass