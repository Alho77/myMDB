from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from mymdb.models import AbstractModel


class PersonManager(models.Manager):
    def all_with_perfetch_movie(self):
        """Return result base on person and avoid to proccess all the Person model"""

        qs = self.get_queryset()
        return qs.prefetch_related('directed', 'role_set__movie')


class Person(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    born = models.DateField()
    died = models.DateField(null=True, blank=True)

    objects = PersonManager()

    class Meta:
        ordering = ('first_name', 'last_name')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse("core:person_detail", kwargs={"id": self.id})


class MovieManager(models.Manager):
    def all_with_related_persons(self):
        qs = self.get_queryset()
        qs = qs.select_related('director')
        qs = qs.prefetch_related('actors')
        return qs


class Movie(AbstractModel):
    runtime = models.PositiveIntegerField()
    director = models.ForeignKey(
        to=Person, on_delete=models.SET_NULL, related_name='directed', null=True, blank=True)
    actors = models.ManyToManyField(
        to=Person, related_name='acting_credits', through='Role', blank=True)

    objects = MovieManager()

    def get_absolute_url(self):
        return reverse("core:movie_detail", kwargs={'movie_id': self.id, 'slug': self.slug})


class Role(models.Model):
    person = models.ForeignKey(to=Person, on_delete=models.DO_NOTHING)
    movie = models.ForeignKey(to=Movie, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('movie', 'person', 'name')

    def __str__(self):
        return f'{self.movie_id} - {self.person_id}: {self.name}'

    def get_absolute_url(self):
        return reverse("core:movie_detail", kwargs={"pk": self.pk})


class Vote(models.Model):
    UP = 1
    DOWN = -1
    CHOICE = ((UP, 'Like'), (DOWN, 'Dislike'))
    User = get_user_model()

    value = models.SmallIntegerField(choices=CHOICE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    voted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
