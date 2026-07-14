from django.test import TestCase
from django.urls import reverse
from .models import Post

class BlogViewsTestCase(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title='Тест', content='Текст')

    def test_home_view(self):
        response = self.client.get(reverse('blog:home'))
        self.assertEqual(response.status_code, 200)

    def test_post_list_view(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тест')

    def test_post_detail_view(self):
        response = self.client.get(reverse('blog:post_detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Текст')
