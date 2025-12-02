from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser, Profile

class SettingsTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='settingsuser',
            email='settings@example.com',
            password='StrongPass123!'
        )
        self.client.login(username='settingsuser', password='StrongPass123!')

    def test_settings_page_loads(self):
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Account Settings")

    def test_update_theme(self):
        response = self.client.post(reverse('settings'), {
            'theme': 'dark',
            'font': 'Arial',
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.theme, 'dark')
