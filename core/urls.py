from django.urls import path

from .views import MovieListView


app_name = 'core'
urlpatterns = [
    path('', MovieListView.as_view(), name='movie_list')
]
