from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class MemoryGameResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    moves = models.IntegerField(default=0)
    time = models.CharField(max_length=10,default='00:00')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Moves: {self.moves}, Time: {self.time},Timestamp:{self.timestamp}"


class MathQuizScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Score: {self.score}, Date:{self.date}"


class MemoryMeastroScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Level: {self.level}, Date:{self.date}"


class HitTheCatScore(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    score=models.IntegerField()
    gamespeed=models.IntegerField()
    time=models.IntegerField()
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Score:{self.score} - GameSpeed:{self.gamespeed} - Time: {self.time} - Date : {self.date}"


