from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password'
    }))

    con_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password'
    }))

    class Meta:
        model = Account
        fields = ['f_name', 'l_name', 'email', 'password', 'ph_number']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['f_name'].widget.attrs['placeholder'] = 'Enter Firstname'
        self.fields['l_name'].widget.attrs['placeholder'] = 'Enter Lastname'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'