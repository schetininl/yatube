from django.test import TestCase, Client
from .models import Post, User
# Create your tests here.

class PostsCasesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
                        username="TestUser", email="mail@mail.ru", password="kthvjynjd"
                )
        self.client.login(username='TestUser', password='kthvjynjd')
    
    def test_user_post(self):
        """Авторизованный пользователь может опубликовать пост (new)"""
        self.post = Post.objects.create(text="Test post", author=self.user)
        response = self.client.get("/TestUser/")
        self.assertEqual(response.context["posts_count"], 1)

    def test_logout_post(self):
        """Неавторизованный посетитель не может опубликовать пост (его редиректит на страницу входа)"""
        self.client.logout()
        response = self.client.get("/new/", follow=True)
        self.assertEqual([('/auth/login/?next=/new/', 302)], response.redirect_chain)

    def test_new_post(self):
        """После публикации поста новая запись появляется на главной странице сайта (index),
         на персональной странице пользователя (profile), и на отдельной странице поста (post)"""
        self.post = Post.objects.create(text=('Test post'), author=self.user)
        test_urls = [
            '',
            f'/{self.user.username}/',
            f'/{self.user.username}/{self.post.pk}/'
        ]
        for url in test_urls:
            response = self.client.get(url)
            self.assertContains(response, self.post.text)

    def test_user_postedit(self):
        """Авторизованный пользователь может отредактировать свой пост
         и его содержимое изменится на всех связанных страницах"""
        self.post = Post.objects.create(text="Test post", author=self.user)
        new_text = 'New Test'
        self.client.post(f'/{self.user.username}/{self.post.pk}/edit', {'text': new_text})
        test_urls = [
            '',
            f'/{self.user.username}/',
            f'/{self.user.username}/{self.post.pk}/'
        ]
        for url in test_urls:
            response = self.client.get(url)
            self.assertContains(response, new_text)


        