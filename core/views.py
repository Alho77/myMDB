from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.shortcuts import redirect, reverse

from .models import Movie, Person, Vote
from .forms import VoteForm


class MovieListView(ListView):
    model = Movie
    context_object_name = 'movies'
    paginate_by = 3


class MovieDetailView(DetailView):
    queryset = Movie.objects.all_with_related_persons_and_score()
    context_object_name = 'movie'
    query_pk_and_slug = True
    pk_url_kwarg = "movie_id"
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(
                self.object, user)
            if vote.id:
                context['vote_form_url'] = reverse('core:vote_update', kwargs={
                                                   'slug': vote.movie.slug, 'id': vote.id})
            else:
                context['vote_form_url'] = reverse('core:vote_create', kwargs={
                                                   'slug': self.object.slug})
            context['vote_form'] = VoteForm(instance=vote)

        return context


class PersonDetailView(DetailView):
    queryset = Person.objects.all_with_perfetch_movie()
    context_object_name = 'person'
    pk_url_kwarg = 'id'


class VoteCreateView(LoginRequiredMixin, CreateView):
    form_class = VoteForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['slug']
        return initial

    def get_success_url(self):
        movie = self.object.movie
        return reverse('core:movie_detail', kwargs={'movie_id': movie.id, 'slug': movie.slug})

    def render_to_response(self, context, **response_kwargs):
        movie = Movie.objects.get(slug=context['view'].kwargs['slug'])
        return redirect(reverse('core:movie_detail', kwargs={'movie_id': movie.id, 'slug': movie.slug}))


class VoteUpdateView(LoginRequiredMixin, UpdateView):
    form_class = VoteForm
    queryset = Vote.objects.all()

    def get_object(self, queryset=None):
        vote = super().get_object(queryset)
        user = self.request.user
        if vote.user != user:
            raise PermissionDenied('Cannot change the vote')
        return vote

    def get_success_url(self):
        movie = self.object.movie
        return reverse('core:movie_detail', kwargs={'movie_id': movie.id, 'slug': movie.slug})

    def render_to_response(self, context, **response_kwargs):
        movie = Movie.objects.get(slug=context['view'].kwargs['slug'])
        return redirect(reverse('core:movie_detail', kwargs={'movie_id': movie.id, 'slug': movie.slug}))
