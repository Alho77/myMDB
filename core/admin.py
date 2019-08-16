from django.contrib import admin

from .models import Movie


class MovieAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'description',
              'year', 'image', 'runtime', 'rating', 'website')
    list_display = ('title', 'rating', 'runtime', 'year')
    list_filter = ('rating', 'year')
    search_fields = ['title', ]
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Movie, MovieAdmin)
