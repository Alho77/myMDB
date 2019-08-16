from django.urls import path

from .views import MovieListView, MovieDetailView


app_name = 'core'
urlpatterns = [
    # list view
    path('', MovieListView.as_view(), name='movie_list'),
    # detail view
    path('<slug:slug>-<int:movie_id>/',
         MovieDetailView.as_view(), name='movie_detail'),
]
