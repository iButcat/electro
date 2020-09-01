from django.test import TestCase, SimpleTestCase
from .models import Post
from electro_social.models import Profile

class TestPostPages(SimpleTestCase):
    def test_posts_list_page_status_code(self):
        response = self.client.get('/posts/list')
        self.assertEqual(response.status_code, 301)
