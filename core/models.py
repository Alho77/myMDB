from django.db import models

from mymdb.models import AbstractModel


class Movie(AbstractModel):
    runtime = models.PositiveIntegerField()
