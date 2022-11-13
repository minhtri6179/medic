from typing import Any
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from requests import request

# Create your views here.
class LoginRequiredView(LoginRequiredMixin):
    login_url: Any = 'login'
