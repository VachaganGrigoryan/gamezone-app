import graphene
import account.schema


class Query(
    account.schema.UserQuery,
    graphene.ObjectType
):
    pass


class Mutation(
    account.schema.UserMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
