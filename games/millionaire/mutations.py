from random import sample
from uuid import uuid4

import strawberry
from asgiref.sync import sync_to_async
from jwtberry.permission import IsAuthenticated
from strawberry.types import Info

from . import models as m
from .types import Quiz


@strawberry.type
class MillionaireMutation:

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @sync_to_async
    def start(self, info: Info) -> Quiz:
        user = info.context.user
        quiz = m.Quiz.objects.filter(user=user, status=m.Quiz.QuizStatus.in_progress).first()
        if quiz is None:

            questions = m.Question.objects.all()
            try:
                random_questions = sample(list(questions), k=5)
            except ValueError:
                print(questions)

            quiz = Quiz.objects.create(user=user, title=str(uuid4()).upper())
            quiz.set_questions(random_questions)

        return quiz

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @sync_to_async
    def close(self, info: Info, guid: strawberry.ID) -> None:
        user = info.context.user
        quiz = m.Quiz.objects.filter(user=user, guid=guid).first()
        if quiz:
            quiz.set_status(m.Quiz.QuizStatus.closed)
