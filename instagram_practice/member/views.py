from django.contrib.auth import get_user_model, authenticate, login as django_login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import SignupForm

User = get_user_model()


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            username=username,
            password=password
        )
        if user is not None:
            django_login(request, user)
            return redirect('post_list')
        else:
            return HttpResponse('Login credentials invalid')
    else:
        return render(request, 'member/login.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                username=username,
                password=password,
            )
            return HttpResponse(f'{user.username}, {user.password}')
        print(form.cleaned_data)
        print(form.errors)
    else:
        form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'member/signup.html', context)
