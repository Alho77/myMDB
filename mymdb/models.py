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
    website = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title
