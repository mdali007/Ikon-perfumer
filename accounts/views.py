from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
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

            #for sending vrfcation msg
            current_url = get_current_site(request)
            m_subject = "please verify your account"
            messege = render_to_string('verify_email.html', {
                'user': user,
                'domain': current_url,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': default_token_generator.make_token(user)
            })
            mail_to = email
            send_mail = EmailMessage(m_subject, messege, to=[mail_to])
            send_mail.send()

            return redirect('/accounts/login/?command=verification&email='+email)    
    else:
        form = RegistrationForm()
    dict = {
        'form': form,
    }
    return render(request, 'register.html', dict)




def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'invalid login')
            return redirect('login')
         
    return render(request, 'signin.html')




@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    return redirect('login')




def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(id=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        messages.error(request, 'invalid activation link')
        return redirect('register')




@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'dashboard.html')



def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            current_url = get_current_site(request)
            m_subject = "Reset your password"
            messege = render_to_string('reset_password_email.html', {
                'user': user,
                'domain': current_url,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': default_token_generator.make_token(user)
            })
            mail_to = email
            send_mail = EmailMessage(m_subject, messege, to=[mail_to])
            send_mail.send()
            messages.success(request, 'password reset email has sent to your mail id')
            return redirect('login')

        else:
            messages.error(request, 'Account does not exist')
            return redirect('register')
    return render(request, 'forgotpassword.html')




def forgotpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(id=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'invalid activation link')
        return redirect('login')
    


def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        cn_password = request.POST['cn_password']
        if password == cn_password:
            uid = request.session.get('uid')
            user = Account.objects.get(id=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'password reset succes')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('resetpassword')
    else:
        return render(request, 'resetpassword.html')