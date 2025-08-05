from encodings.punycode import adapt

from django.test import TestCase
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class CustomUserModelTest(TestCase):

    def test_create_user(self):
        user = CustomUser.objects.create_user(username='test-user', password='password1234')
        self.assertEqual(user.username, 'test-user')
        self.assertTrue(user.check_password("password1234"))
        self.assertTrue(user.usable_password)

    def test_create_superuser(self):
        admin_user = CustomUser.objects.create_superuser(username="admin-user", password="password1234")
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.usable_password)

    def test_change_usable_password(self):
        user = CustomUser.objects.create_user(username="test-user2", )
        user.usable_password = False
        user.save()
        self.assertFalse(user.usable_password)
