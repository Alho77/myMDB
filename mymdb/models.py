from django.db import models

# Rating choices
NOT_RATED = 0
RATED_G = 1
RATED_PG = 2
RATED_R = 3
RATING = ((NOT_RATED, 'NR - Not Rated'), (RATED_G, 'G - General Audience'),
          (RATED_PG, 'PG - Parental Guidance'), (RATED_R, 'R - Restricted'))


class AbstractModel(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True)
    year = models.PositiveIntegerField()
    rating = models.IntegerField(choices=RATING, default=NOT_RATED)
    image = models.ImageField(upload_to='movies/%Y/%m/%d', blank=True)
    website = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class PersonManager(models.Manger):
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
