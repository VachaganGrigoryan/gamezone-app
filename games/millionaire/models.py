import uuid

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models


class Answer(models.Model):
    guid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        unique=True,
        verbose_name=_('GUID'),
        help_text=_('The unique identifier.'),
    )
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='question')
    selected = models.ForeignKey('Option', on_delete=models.CASCADE, related_name='selected')

    class Meta:
        db_table = 'millionaire_quiz_answers'

        verbose_name_plural = _("Quiz Answers")
        unique_together = ['quiz', 'question']
        ordering = ['pk']

    def __str__(self):
        return self.selected.body


class Quiz(models.Model):
    class QuizStatus(models.TextChoices):
        in_progress = 'InProgress'
        closed = 'Closed'
        done = 'Done'

    guid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        unique=True,
        verbose_name=_('GUID'),
        help_text=_('The unique identifier.'),
    )
    title = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user')
    questions = models.ManyToManyField('Question', max_length=5, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)
    total = models.PositiveIntegerField(default=0)
    status = models.CharField(choices=QuizStatus.choices, default=QuizStatus.in_progress, max_length=12)

    class Meta:
        db_table = 'millionaire_quizzes'
        verbose_name_plural = _("Quizzes")
        ordering = ['pk']

    def __str__(self):
        return self.title

    def election(self, question_id, answer):
        question = self.questions.get(id=question_id)
        option = question.get_option(answer)

        quiz_answer = self.is_answered_question(question_id)
        if quiz_answer:
            return quiz_answer

        quiz_answer = Answer.objects.create(
            quiz=self,
            question=question,
            selected=option
        )
        if option.correct:
            self.total += question.coin
            self.save()
        return quiz_answer

    def set_status(self, status):
        self.status = status
        self.save()

    def set_questions(self, questions):
        self.questions.set(questions)
        self.save()

    def get_next_question(self):
        return self.questions.all().filter(~models.Q(pk__in=self.answers.values('question'))).first()

    def is_answered_question(self, question_id):
        return self.answers.all().filter(question__id=question_id).first()


class Question(models.Model):
    class Complexity(models.TextChoices):
        easy = 'Easy'
        medium = 'Medium'
        hard = 'Hard'
        difficult = 'Difficult'

    guid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        unique=True,
        verbose_name=_('GUID'),
        help_text=_('The unique identifier.'),
    )
    content = models.TextField(blank=False)
    coin = models.PositiveIntegerField(default=0)
    complexity = models.TextField(
        max_length=12,
        choices=Complexity.choices,
        default=Complexity.easy
    )

    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'millionaire_questions'
        verbose_name_plural = _("Questions")
        ordering = ['pk']

    def get_option(self, answer):
        return self.options.all().filter(body=answer).first()

    def __repr__(self):
        return f"Question('{self.id}', '{self.content}')"

    def __str__(self):
        return self.content


class Option(models.Model):
    guid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        unique=True,
        verbose_name=_('GUID'),
        help_text=_('The unique identifier.'),
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    body = models.TextField(blank=False)
    correct = models.BooleanField(default=False)

    class Meta:
        db_table = 'millionaire_question_options'
        verbose_name_plural = _("Question Options")
        ordering = ['pk']

    def __str__(self):
        return self.body