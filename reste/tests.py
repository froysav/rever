from django.test import TestCase
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
import warnings
@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    url = reverse('register')
    data = {
        'first_name': 'Rahmatjon',
        'last_name': 'Ruslanov',
        'email': 'ruslanovrahmet@gmail.com',
        'username': 'Rahmet97',
        'password1': 'ab1234cd',
        'password2': 'ab1234cd'
    }

    response = client.post(url, data, format='json')
    assert response.status_code == 201