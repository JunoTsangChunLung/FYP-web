from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput

# Registration Form
class createUserForm(UserCreationForm):
    class Meta:

        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(createUserForm, self).__init__(*args, **kwargs)

#Login Form
class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

#Update Form
class UpdateUserForm(forms.ModelForm):

    password = None

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].required = True

    class Meta:
        model = User

        fields = ['username']
        exclude = ['password1', 'password2']
