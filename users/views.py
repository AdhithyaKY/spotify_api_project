from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from spotify.utils import get_user_tokens
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # automatically hashes the password for the db
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            messages.success(
                request, f'{first_name.capitalize()}, your account has been created! You are now able to login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):

    result = get_user_tokens(request.user)
    if result is None:
        results = {'is_auth': False}
    else:
        results = {'is_auth': True}

    return render(request, 'users/profile.html', results)
