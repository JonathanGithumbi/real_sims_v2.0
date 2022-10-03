from django.test import SimpleTestCase
from django.urls import reverse, resolve
from user_account.views import *
from django.contrib.auth.views import *

class TestUrls(SimpleTestCase):
    def test_login_url_resolves(self):
        url = reverse('login')
        # print(resolve(url))
        self.assertEqual(resolve(url).func, login_user)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        # print(resolve(url))
        self.assertEqual(resolve(url).func, logout_view)

    def test_password_change_url_resolves(self):
        url = reverse('password_change')
        # print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, PasswordChangeView)

    def test_password_change_done_url_resolves(self):
        url = reverse('password_change_done')
        # print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, PasswordChangeDoneView)

    def test_password_reset_url_resolves(self):
        url = reverse('password_reset')
        # print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, PasswordResetView)

    def test_password_reset_done_url_resolves(self):
        url = reverse('password_reset_done')
        # print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, PasswordResetDoneView)


    def test_password_reset_confirm_url_resolves(self):
        url = reverse('password_reset_confirm',args=['uid','token'])
        # print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, PasswordResetConfirmView)

    def test_password_reset_complete_url_resolves(self):
        url = reverse('password_reset_complete')
        # print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, PasswordResetCompleteView)

    def test_oauth_url_resolves(self):
        url = reverse('oauth')
        # print(resolve(url))
        self.assertEqual(resolve(url).func, oauth)

    def test_callback_url_resolves(self):
        url = reverse('callback')
        # print(resolve(url))
        self.assertEqual(resolve(url).func, callback)

    def test_connected_url_resolves(self):
        url = reverse('connected')
        # print(resolve(url))
        self.assertEqual(resolve(url).func, connected)

    def test_qbo_request_url_resolves(self):
        url = reverse('qbo_request')
        # print(resolve(url))
        self.assertEqual(resolve(url).func, qbo_request)

    def test_revoke_url_resolves(self):
        url = reverse('revoke')
        # print(resolve(url))
        self.assertEqual(resolve(url).func, revoke)

    def test_refresh_url_resolves(self):
        url = reverse('refresh')
        # print(resolve(url))
        self.assertEqual(resolve(url).func, refresh)

    def test_user_info_url_resolves(self):
        url = reverse('user_info')
        # print(resolve(url))
        self.assertEqual(resolve(url).func, user_info)
