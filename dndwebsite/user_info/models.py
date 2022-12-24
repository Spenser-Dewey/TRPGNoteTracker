from django.contrib.auth.models import AbstractUser
from django import forms
from django.db import models

class Player(AbstractUser):
    username = models.CharField(max_length=120, unique=True)
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

class NewPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [ 'username', 'email', 'first_name', 'last_name', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }