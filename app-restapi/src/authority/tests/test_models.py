from rest_framework.test import APITestCase
from authority.models import User


class TestModel(APITestCase):
    def test_creates_user(self):
        user = User.objects.create_user('arhan', 'ersinsenzek@yahoo.com', '1qazxsw234')
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, 'ersinsenzek@yahoo.com')

    def test_raises_error_when_no_username_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, username='', email='ersinsenzek@yahoo.com',
                          password='1qazxsw234')

    def test_raises_error_with_message_when_no_username_is_supplied(self):
        with self.assertRaisesMessage(ValueError, 'The given username must be set'):
            User.objects.create_user(username='', email='ersinsenzek@yahoo.com', password='1qazxsw234')

    def test_raises_error_when_no_email_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, username='arhan', email='', password='1qazxsw234')

    def test_raises_error_with_message_when_no_email_is_supplied(self):
        with self.assertRaisesMessage(ValueError, 'The given email must be set'):
            User.objects.create_user(username='arhan', email='', password='1qazxsw234')

    def test_creates_super_user_with_staf_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_staff=True.'):
            User.objects.create_superuser(username='arhan', email='', password='1qazxsw234', is_staff=False)

    def test_creates_super_user_with_super_user_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_superuser=True.'):
            User.objects.create_superuser(username='arhan', email='', password='1qazxsw234', is_superuser=False)

    def test_creates_super_user(self):
        user = User.objects.create_superuser('arhan', 'ersinsenzek@yahoo.com', '1qazxsw234')
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.email, 'ersinsenzek@yahoo.com')

        # user = User.objects.create_superuser('ersinsenzek@yahoo.com', '1qazxsw234')
        # self.assertIsInstance(user, User)
        # self.assertTrue(user.is_staff)
        # self.assertEqual(user.email, 'ersinsenzek@yahoo.com')
