from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser

class AuthFlowTests(TestCase):
    def test_signup_redirects_to_dashboard(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        # After signup, should redirect to dashboard
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())

    def test_login_with_username_redirects_to_dashboard(self):
        user = CustomUser.objects.create_user(
            username='loginuser',
            email='login@example.com',
            password='StrongPass123!'
        )
        response = self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'StrongPass123!',
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_with_email_redirects_to_dashboard(self):
        user = CustomUser.objects.create_user(
            username='emailuser',
            email='email@example.com',
            password='StrongPass123!'
        )
        response = self.client.post(reverse('login'), {
            'username': 'email@example.com',  # using email instead of username
            'password': 'StrongPass123!',
        })
        self.assertRedirects(response, reverse('dashboard'))
