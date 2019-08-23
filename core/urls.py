from django.urls import path

from . import views


app_name = 'core'
urlpatterns = [
    # list view
    path('', views.MovieListView.as_view(), name='movie_list'),
    # detail view
    path('<slug:slug>-<int:movie_id>/',
         views.MovieDetailView.as_view(), name='movie_detail'),
    # person detail
    path('person-<int:id>/', views.PersonDetailView.as_view(), name='person_detail'),
    path('movie_<slug:slug>/image/upload/',
         views.MovieImageUploadView.as_view(), name='image_upload'),

]
