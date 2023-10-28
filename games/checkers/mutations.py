import uuid
from datetime import datetime
from typing import List

import strawberry
from asgiref.sync import sync_to_async
from jwtberry.permission import IsAuthenticated
from strawberry.field_extensions import InputMutationExtension
from strawberry.types import Info
from typing_extensions import Annotated

from .game import init_game, update_board
from . import models
from core.json import JSON


@strawberry.mutation
# @login_required
def create_board(owner: str, color: str, length: int) -> JSON:
    return init_game(owner, color, length)


@strawberry.mutation(permission_classes=[IsAuthenticated])
def update_board_in_game(guid: strawberry.ID, grid_changes: List[List[int]]) -> JSON:
    return update_board(guid=guid, grid_changes=grid_changes)
