from django.shortcuts import render
from .forms import RegistrationForm

# Create your views here.
def register(request):
    form = RegistrationForm()
    dict = {
        'form': form,
    }
    return render(request, 'register.html', dict)


def login(request):
    return render(request, 'signin.html')


def logout(request):
    return