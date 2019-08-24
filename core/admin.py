from django.contrib import admin

from . import models


class CategoryInline(admin.TabularInline):
    model = models.CategoryRelation
    extra = 1


class RoleInline(admin.TabularInline):
    model = models.Role
    extra = 1


class MovieAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'description', 'director',
              'year', 'image', 'runtime', 'rating', 'website')
    list_display = ('title', 'rating', 'runtime', 'year')
    list_filter = ('rating', 'year')
    inlines = (RoleInline, CategoryInline)
    search_fields = ['title', ]
    prepopulated_fields = {'slug': ('title',)}


class MovieImageAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'uploaded_at')
    list_filter = ('movie', 'user', 'uploaded_at')
    search_fields = ('movie', 'user')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'born', 'died')
    list_filter = ('first_name', 'last_name', 'born')
    inlines = (RoleInline,)
    search_fields = ['first_name', 'last_name']


class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    inlines = (CategoryInline,)
    search_fields = ('name',)


admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.Movie, MovieAdmin)
admin.site.register(models.MovieImage, MovieImageAdmin)
admin.site.register(models.Role)
admin.site.register(models.Category, CategoryAdmin)
