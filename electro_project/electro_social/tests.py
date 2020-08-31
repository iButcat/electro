from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

class TestPostClass(TestCase):
    def setUp(self):
        User.objects.create_user(username="Butcat")
        Profile.objects.create(user="Butcat")

    def test_if_create_and_associate(self):
        get_user_butcat = Profile.objects.get(username="Butcat")
