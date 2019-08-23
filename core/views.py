from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View
from django.shortcuts import redirect, render, reverse

from .models import Movie, Person, MovieImage
from .forms import MovieImageForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = self.movie_image_form()
        return context

    def movie_image_form(self):
        if self.request.user.is_authenticated:
            return MovieImageForm()
        return None


class PersonDetailView(DetailView):
    queryset = Person.objects.all_with_perfetch_movie()
    context_object_name = 'person'
    pk_url_kwarg = 'id'


class MovieImageUploadView(View):

    def get(self, request, slug):
        photos = MovieImage.objects.all()
        movie = Movie.objects.get(slug=slug)
        return render(self.request, 'core/imageupload/index.html', {'photos': photos, 'movie': movie})

    def post(self, request, slug):
        form = MovieImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            movie = Movie.objects.get(slug=slug)
            for photo in request.FILES.getlist('image'):
                instance = MovieImage.objects.create(
                    image=photo, movie=movie, user=request.user)
                data = {'is_valid': True, 'name': instance.image.file.name,
                        'url': instance.image.url}
        else:
            data = {'is_valid': False}

        return JsonResponse(data)
