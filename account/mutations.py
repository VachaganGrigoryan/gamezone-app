import graphene
from graphene_django.rest_framework.mutation import SerializerMutation

from account.serializers import UserSerializer


class CreateUserMutation(SerializerMutation):
    class Meta:
        serializer_class = UserSerializer


# class UpdateUserMutation(graphene.Mutation):
#     class Arguments:
#         # The input arguments for this mutation
#         guid = graphene.UUID(required=True)
#         id = graphene.ID()
#
#     # The class attributes define the response of the mutation
#     question = graphene.Field(UserType)
#
#     @classmethod
#     def mutate(cls, root, info, text, guid):
#         user = User.objects.get(guid=guid)
#         user.text = text
#         user.save()
#         # Notice we return an instance of this mutation
#         return CreateUserMutation(user=user)
