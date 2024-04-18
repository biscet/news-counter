from django.db import models
from django.contrib.auth.models import User

class News(models.Model):
    title = models.CharField(max_length=256)
    popularity = models.IntegerField(default=1)
    added_by = models.ManyToManyField(User)

    def __str__(self):
        return self.title