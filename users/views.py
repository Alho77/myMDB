from django.forms import ValidationError
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template.loader import render_to_string


def register_handler(request, form, header):
    """For handling user egistering in modal dialog"""

    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['is_valid'] = True
        else:
            data['is_valid'] = False

    context = {'form': form, 'header': header}
    data['html_form'] = render_to_string(
        'users/register_login.html', context, request)
    return JsonResponse(data)


def login_view(request):
    """Login the requested user"""

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse('core:movie_list'))
        else:
            raise ValidationError('Invalid Username or Password')
    else:
        data = dict()
        context = {'form': AuthenticationForm(), 'header': 'Login'}
        data['html_form'] = render_to_string(
            'users/register_login.html', context, request)
        return JsonResponse(data)
