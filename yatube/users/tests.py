from django.test import TestCase, Client
from django.core import mail


class ProfileCasesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post ('/auth/signup/', {'first_name': 'Test', 'last_name': 'User', 
            'username': 'TestUser', 'email': 'mail@mail.ru', 'password1': 'kthvjynjd', 
                'password2': 'kthvjynjd'})
    
    def test_send_email(self):
        """Пользователь регистрируется и ему отправляется письмо с подтверждением регистраци"""
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Подтверждение регистрации на Yatube')
        self.assertEqual(mail.outbox[0].to, ['mail@mail.ru'])
    
    def test_user_profile(self):
        """После регистрации пользователя создается его персональная страница (profile)"""
        response = self.client.get("/TestUser/")
        self.assertEqual(response.status_code, 200)


class ErrorsCasesTests(TestCase):
    def test_404(self):
        """При запросе несуществующей страницы возвращается страница 404"""
        self.client = Client()
        response = self.client.get("/TestUser/")
        self.assertEqual(response.status_code, 404)

