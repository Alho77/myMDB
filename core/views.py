from django.views.generic import DetailView, ListView
from django.shortcuts import reverse

from .models import Movie, Person, Vote
from .forms import VoteForm


class MovieListView(ListView):
    model = Movie
    context_object_name = 'movies'
    paginate_by = 3


class MovieDetailView(DetailView):
    queryset = (Movie.objects.all_with_related_persons())
    context_object_name = 'movie'
    query_pk_and_slug = True
    pk_url_kwarg = "movie_id"
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated():
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(
                self.object, user)
            if vote.id:
                context['vote_form_url'] = reverse('core:vote_update', kwargs={
                                                   'movie_id': vote.movie.id, 'id': vote.id})
            else:
                context['vote_form_url'] = reverse('core:vote_create', kwargs={
                                                   'movie_id': self.object.id})
            context['vote_form'] = VoteForm(instance=vote)

            return context


class PersonDetailView(DetailView):
    queryset = Person.objects.all_with_perfetch_movie()
    context_object_name = 'person'
    pk_url_kwarg = 'id'
