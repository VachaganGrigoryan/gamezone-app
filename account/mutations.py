import strawberry

from jwtberry.mutations import auth_token
from jwtberry.types import JwtAuthResponse
from strawberry_django import auth


@strawberry.type
class AccountMutation:
    login: JwtAuthResponse = auth_token
    # refresh: JwtAuthResponse = refresh_token
    logout = auth.logout()
    # register: UserType = auth.register(UserInput)
