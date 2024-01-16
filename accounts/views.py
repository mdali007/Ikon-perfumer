from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print('its working')
        if form.is_valid():
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            ph_number = form.cleaned_data['ph_number']
            username = email.split('@')[0]
            user = Account.objects.create_user(f_name=f_name, l_name=l_name, email=email, username=username,
                                               password=password)
            user.ph_number = ph_number
            user.save()
        return redirect('home')
            
    else:
        form = RegistrationForm()
    dict = {
        'form': form,
    }
    return render(request, 'register.html', dict)


def login(request):
    return render(request, 'signin.html')


def logout(request):
    return
