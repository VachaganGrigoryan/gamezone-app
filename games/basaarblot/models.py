from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    high_score = models.IntegerField(default=0)
    game_level = models.CharField(max_length=10, choices=[('beginner', 'Beginner'),
                                                          ('intermediate', 'Intermediate'),
                                                          ('advanced', 'Advanced')],
                                                            default='beginner')

    def __str__(self):
        return self.user.username

class GameSession(models.Model):
    session_name = models.CharField(max_length=255)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)


class PlayerGameSession(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE)


class Card(models.Model):
    card_name = models.CharField(max_length=255)
    card_type = models.CharField(max_length=50)
    card_color = models.CharField(max_length=20, null=True, blank=True)

class Interaction(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50)
    action_timestamp = models.DateTimeField()
