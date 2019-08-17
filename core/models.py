from django.db import models

from mymdb.models import AbstractModel, Person


class Movie(AbstractModel):
    runtime = models.PositiveIntegerField()
    director = models.ForeignKey(
        to=Person, on_delete=models.SET_NULL, related_name='directed', null=True, blank=True)
    actors = models.ManyToManyField(
        to=Person, related_name='acting_credits', through='Role', blank=True)


class Role(models.Model):
    person = models.ForeignKey(to=Person, on_delete=models.DO_NOTHING)
    movie = models.ForeignKey(to=Movie, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('movie', 'person', 'name')

    def __str__(self):
        return f'{self.movie_id} - {self.person_id}: {self.name}'
