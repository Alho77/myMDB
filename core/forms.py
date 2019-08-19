from django import forms
from django.contrib.auth import get_user_model

from .models import Movie, Vote

User = get_user_model()


class VoteForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        User.objects.all(), widget=forms.HiddenInput, disabled=True)
    movie = forms.ModelChoiceField(
        Movie.objects.all(), widget=forms.HiddenInput, disabled=True)
    value = forms.ChoiceField(
        choices=Vote.CHOICE, widget=forms.RadioSelect, label='Vote')

    class Meta:
        model = Vote
        fields = ('user', 'movie', 'value')
