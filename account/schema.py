import graphene
from graphene_django.filter import DjangoFilterConnectionField

from account.filters import UserFilter
from account.models import User
from account.mutations import CreateUserMutation
from account.types import UserType


class UserQuery(graphene.ObjectType):
    # users = graphene.List(UserType)
    users = DjangoFilterConnectionField(
        UserType,
        filterset_class=UserFilter
    )
    user = graphene.Field(UserType, guid=graphene.UUID())

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, guid):
        return User.objects.get(guid=guid)


class UserMutation(graphene.ObjectType):
    create_user = graphene.Field(CreateUserMutation)


schema = graphene.Schema(query=UserQuery, mutation=UserMutation)

# import graphene
# from graphene_django.types import DjangoObjectType
# from account.models import User, Profile


# class UserType(DjangoObjectType):
#     class Meta:
#         model = User
#         fields = ("guid", "email")
#
#
# class UserQuery(graphene.ObjectType):
#     users = graphene.List(UserType)
#     user_by_guid = graphene.Field(UserType, id=graphene.String())
#
#     def resolve_users(root, info, **kwargs):
#         # Querying a list
#         return User.objects.all()
#
#     def resolve_user_by_guid(root, info, guid):
#         # Querying a single question
#         return User.objects.get(guid=guid)
#
#
# class ProfileType(DjangoObjectType):
#     class Meta:
#         model = Profile
#         fields = '__all__'
#
#
# schema = graphene.Schema(query=UserQuery)
