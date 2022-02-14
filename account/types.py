from graphene import relay
from graphene_django.types import DjangoObjectType
from account.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ['guid', 'first_name', 'last_name']
        exclude = ('password',)
        interfaces = (relay.Node, )
