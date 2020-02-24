from django.test import TestCase, Client
from .models import Post, User, Group
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

    def test_img(self):
        """Тесты проверяют: страницу конкретной записи с картинкой: на странице есть тег <img>
        что на главной странице, на странице профайла и на странице группы пост с картинкой отображается корректно, с тегом 
        что срабатывает защита от загрузки файлов не-графических форматов"""
        self.group = Group.objects.create(title="TestGroup", slug="testgroup", description="TestDesc")
        with open('/Users/salexbin/Pictures/image.jpg', 'rb') as fp:
            self.client.post ('/new/', {'group': '1','text': 'Test post', 'image': fp})
        test_urls = [
            '',
            '/TestUser/',
            '/TestUser/1/',
            '/group/testgroup/'
        ]
        for url in test_urls:
            response = self.client.get(url)
            self.assertContains(response, '<img')

        with open('/Users/salexbin/Pictures/Untitled.rtf', 'rb') as fp:
            self.client.post ('/new/', {'group': '1','text': 'Test post', 'image': fp})
        response = self.client.get('/TestUser/')
        self.assertEqual(response.context["posts_count"], 1) 


class CacheCaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
                        username="TestUser", email="mail@mail.ru", password="kthvjynjd"
                )
        self.client.login(username='TestUser', password='kthvjynjd')
    
    def test_cache_index(self):
        """Тестирование функции кэша на главной странице"""
        self.post = Post.objects.create(text="Test post", author=self.user)
        response = self.client.get("")
        self.assertNotContains(response, "Test post")


class followCaseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
                        username="TestUser", email="mail@mail.ru", password="kthvjynjd"
                )
        self.user2 = User.objects.create_user(
                        username="TestUser2", email="mail2@mail.ru", password="kthvjynjd"
                )
        self.user3 = User.objects.create_user(
                        username="TestUser3", email="mail3@mail.ru", password="kthvjynjd"
                )
        self.client.login(username="TestUser", password="kthvjynjd")
        self.post = Post.objects.create(text="Test post", author=self.user3)

    def test_follow_unfollow(self):
        """Авторизованный пользователь может подписываться на других пользователей и удалять их из подписок."""
        self.client.get('/TestUser2/follow')
        response = self.client.get('/TestUser/')
        self.assertEqual(response.context["follow"], 1)
        self.client.get('/TestUser2/unfollow')
        response = self.client.get('/TestUser/')
        self.assertEqual(response.context["follow"], 0)
    

    def test_news_lent(self):
        """Новая запись пользователя появляется в ленте тех, кто на него подписан и не появляется в ленте тех, кто не подписан на него."""
        self.client.get('/TestUser3/follow')
        response = self.client.get('/follow/')
        self.assertContains(response, 'Test post')
        self.client.logout()
        self.client.login(username='TestUser2', password='kthvjynjd')
        response = self.client.get('/follow/')
        self.assertNotContains(response, 'Test post')
    

    def test_comments(self):
        """Только авторизированный пользователь может комментировать посты."""
        self.client.post ('/TestUser3/1/comment', {'text': 'Test comment'})
        response = self.client.get('/TestUser3/1/')
        self.assertContains(response, 'Test comment')

        self.client.logout()
        self.client.post ('/TestUser3/1/comment', {'text': 'Test comment2'})
        response = self.client.get('/TestUser3/1/')
        self.assertNotContains(response, 'Test comment2')
        