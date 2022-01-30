import graphene
from account.schema import UserQuery


class Query(UserQuery):
    pass


class Mutation():
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
