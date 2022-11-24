from django.test import TestCase, Client

# Create your tests here.
c = Client()
response = c.get('/login/', {'username': 'lam123', 'password': '123456'})
response.status_code