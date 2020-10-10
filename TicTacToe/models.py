from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    room_name = models.CharField(blank=False, max_length=100, null=False, unique=True)

    # player 1 is the creator of the room
    player1 = models.ForeignKey(to=User, blank=False, on_delete=models.DO_NOTHING, related_name='player1')

    player2 = models.ForeignKey(to=User, blank=True, on_delete=models.DO_NOTHING, null=True, related_name='player2')
    winner = models.CharField(blank=True, max_length=1000, null=True, unique=True)
    total_matches = models.IntegerField(blank=True, null=True, default=5)
    score_player1 = models.IntegerField(blank=True, null=True, default=0)
    score_player2 = models.IntegerField(blank=True, null=True, default=0)
    STATUS_CHOICES = [('0', 'Game Over'), ('1', 'In Progress')]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return self.room_name

    def publish(self):
        self.save()
