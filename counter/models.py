from django.db import models


class Counter(models.Model):
    num_counts = models.IntegerField(default=0)
