from django import forms
from django.contrib.auth import get_user_model

from .models import MovieImage, Movie


class MovieImageForm(forms.ModelForm):
    class Meta:
        model = MovieImage
        fields = ('image', )
