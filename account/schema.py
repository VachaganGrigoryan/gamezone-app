import graphene
from graphene_django.types import DjangoObjectType
from account.models import User, Profile


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("guid", "email")


class UserQuery(graphene.ObjectType):
    users = graphene.List(UserType)
    user_by_guid = graphene.Field(UserType, id=graphene.String())

    def resolve_users(root, info, **kwargs):
        # Querying a list
        return User.objects.all()

    def resolve_user_by_guid(root, info, guid):
        # Querying a single question
        return User.objects.get(guid=guid)


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = '__all__'


schema = graphene.Schema(query=UserQuery)
