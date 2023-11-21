from typing import List

import strawberry
from asgiref.sync import sync_to_async
from jwtberry.permission import IsAuthenticated

from .game import init_game, update_board
from core.json import JSON


@strawberry.type
class CheckersMutation:

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @sync_to_async
    def create_board(self, owner: str, color: str, length: int) -> JSON:
        return init_game(owner, color, length)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @sync_to_async
    def update_board_in_game(self, guid: strawberry.ID, grid_changes: List[List[int]]) -> JSON:
        return update_board(guid=guid, grid_changes=grid_changes)
