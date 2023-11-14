from typing import Optional, List

import strawberry
from asgiref.sync import sync_to_async
from jwtberry.permission import IsAuthenticated
from strawberry import auto
from strawberry.types import Info

from . import models as m


@strawberry.django.type(model=m.Question)
class Question:
    guid: strawberry.ID
    content: auto
    coin: auto
    complexity: auto


@strawberry.django.type(model=m.Quiz)
class Quiz:
    guid: strawberry.ID
    title: auto

    total: auto
    status: auto
    created_at: auto

    @strawberry.field()
    @sync_to_async
    def question(self) -> Optional[Question]:
        question = self.get_next_question()
        if question is None:
            self.set_status(m.Quiz.QuizStatus.done)

        return question

    @classmethod
    def all(cls, info) -> List[m.Quiz]:
        return m.Quiz.objects.all()

    @classmethod
    async def get_object_by_guid(cls, info, guid) -> m.Quiz:
        return await m.Quiz.objects.filter(guid=guid).afirst()


@strawberry.type
class MillionaireQuery:

    @strawberry.django.field(
        permission_classes=[IsAuthenticated]
    )
    async def game(self, info: Info, guid: str) -> Quiz:
        return await Quiz.get_object_by_guid(info, guid)

    @strawberry.django.field(
        permission_classes=[IsAuthenticated]
    )
    def histories(self, info: Info) -> List[Quiz]:
        return Quiz.all(info)
