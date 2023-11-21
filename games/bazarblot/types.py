import strawberry
import typing

@strawberry.type
class Player:
    username: str

@strawberry.type
class Rating:
    player: Player
    card_type: str
    rate: str


def get_players():
    return [
        Player(
            username="player1"
        ),
    ]
@strawberry.type
class BazarBlotQuery:
    players: typing.List[Player]=strawberry.field(resolver=get_players)


schema = strawberry.Schema(query=BazarBlotQuery)