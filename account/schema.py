import graphene
# from graphene_django.rest_framework.mutation import SerializerMutation

from account.models import User
from account.types import UserType


class UserQuery(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, guid=graphene.UUID())

    def resolve_users(self, info, **kwargs):
        return User.objects.all_users()

    def resolve_user(self, info, guid):
        return User.objects.get(guid=guid)


# class UserSerializer()
#
#
# class CreatePlayerMutation(SerializerMutation):
#     class Meta:
#         serializer_class = UserSerializer


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        guid = graphene.UUID(required=True)
        id = graphene.ID()

    # The class attributes define the response of the mutation
    question = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, text, guid):
        user = User.objects.get(guid=guid)
        user.text = text
        user.save()
        # Notice we return an instance of this mutation
        return CreateUserMutation(user=user)


class UserMutation(graphene.ObjectType):
    create_user = graphene.Field(CreateUserMutation)


schema = graphene.Schema(query=UserQuery)

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
