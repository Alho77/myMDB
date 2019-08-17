from django.contrib import admin

from .models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'born', 'died')
    list_filter = ('first_name', 'last_name', 'born')
    search_fields = ['first_name', 'last_name']


admin.site.register(Person, PersonAdmin)
