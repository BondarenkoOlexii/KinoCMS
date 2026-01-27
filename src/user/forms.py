from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from src.user.models import User
from src.adminpanel.models.UserChoise import Language, Sex, City
from allauth.account.forms import SetPasswordForm

class UserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'real_adress', 'password', 'phone_number', 'city', 'date_of_birth', 'language', 'sex', 'credit_card']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'col-sm-6"'}),
            'last_name': forms.TextInput(attrs={'class': 'col-sm-6"'}),
            'username': forms.TextInput(attrs={'class': 'col-sm-6"'}),
            'email': forms.EmailInput(attrs={'class': 'col-sm-6"'}),
            'real_adress': forms.TextInput(attrs={'class': 'col-sm-6"'}),
            'password': forms.PasswordInput(attrs={'class': 'col-sm-6"'}),
            'phone_number': forms.TextInput(attrs={'class': 'col-sm-6"'}),
            'credit_card': forms.TextInput(attrs={'class': 'col-sm-6"'}),

            'sex': forms.RadioSelect(choices=Sex),
            'language': forms.RadioSelect(choices=Language),
            'city': forms.Select(choices=City),

            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'col-sm-6"'})
        }

class CustomChangePassword(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        place_holder = ['Пароль', 'Повторить пароль']
        index = 0
        for field in ['password1', 'password2', 'old_password']:
            if field != 'old_password':
                self.fields[field].widget.attrs.update({'class': 'form-control', 'placeholder': place_holder[index]})
                index += 1
