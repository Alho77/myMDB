from django.contrib import admin

from .models import Movie, Person


class MovieAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'description', 'director',
              'year', 'image', 'runtime', 'rating', 'website')
    list_display = ('title', 'rating', 'runtime', 'year')
    list_filter = ('rating', 'year')
    search_fields = ['title', ]
    prepopulated_fields = {'slug': ('title',)}


class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'born', 'died')
    list_filter = ('first_name', 'last_name', 'born')
    search_fields = ['first_name', 'last_name']


admin.site.register(Person, PersonAdmin)
admin.site.register(Movie, MovieAdmin)
