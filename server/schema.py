import graphene
from account.schema import UserQuery, UserType


class Query(
    UserQuery,
    graphene.ObjectType
):
    pass


class Mutation(
    UserType,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query)
