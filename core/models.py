from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse
from django.template.defaultfilters import slugify

from mymdb.models import AbstractModel

User = get_user_model()


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


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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
    category = models.ManyToManyField(
        to=Category, related_name='categorized', through='CategoryRelation', blank=True)

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


class CategoryRelation(models.Model):
    category = models.ForeignKey(to=Category, on_delete=models.DO_NOTHING)
    movie = models.ForeignKey(to=Movie, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('category', 'movie')


def movie_dir_with_uuid(instance, filename):
    """
    Store all movie's images in a directory and generate unique name
    for each file
    """

    title = instance.movie.title
    slug = slugify(title)
    return f'movies/{slug}/{uuid4().hex}.png'


class MovieImage(models.Model):
    image = models.ImageField(upload_to=movie_dir_with_uuid)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
