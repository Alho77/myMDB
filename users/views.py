from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
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
