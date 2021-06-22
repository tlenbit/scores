from django.db import models


class Score(models.Model):
    event_id = models.IntegerField()
    created_at = models.DateTimeField()
    score_idx = models.IntegerField()
    score1 = models.IntegerField()
    score2 = models.IntegerField()
