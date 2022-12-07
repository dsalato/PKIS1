from django import forms
from django.core.exceptions import ValidationError
from polls.models import User


class RegisterUserForm(forms.ModelForm):

    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput)

    password2 = forms.CharField(label='Пароль повторно',
                                widget=forms.PasswordInput)

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError({
                'password2': ValidationError('Введенные пароли не совпадают', code='password_error')
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password2', 'photo']


class ProfileUpdate(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.CharField(required=False)
    photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',  'photo']