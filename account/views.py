from django.shortcuts import render
from django.contrib.auth.mixins import AccessMixin
from account.models import User
# Create your views here.
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

