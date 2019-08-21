from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.shortcuts import redirect, reverse

from .models import Movie, Person


class MovieListView(ListView):
    model = Movie
    context_object_name = 'movies'
    paginate_by = 3


class MovieDetailView(DetailView):
    queryset = Movie.objects.all_with_related_persons()
    context_object_name = 'movie'
    query_pk_and_slug = True
    pk_url_kwarg = "movie_id"
    slug_url_kwarg = 'slug'


class PersonDetailView(DetailView):
    queryset = Person.objects.all_with_perfetch_movie()
    context_object_name = 'person'
    pk_url_kwarg = 'id'
