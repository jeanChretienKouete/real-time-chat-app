import sys
import unittest
from os.path import abspath, dirname
from unittest.mock import patch

sys.path.insert(0, abspath(dirname(__file__)) + "/../../")


from apps import create_app
from models.user import User

app = create_app()


class TestUser(unittest.TestCase):
    def setUp(self):
        app.test_request_context().push()
        self.client = app.test_client()

    @patch("apps.user.routes.render_template")
    def test_register_page(self, mock_render_template) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        mock_render_template.assert_called_with("pages/signup.jinja")

    @patch("apps.user.routes.render_template")
    def test_login_page(self, mock_render_template) -> None:
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        mock_render_template.assert_called_with("pages/login.jinja")

    @patch("apps.user.routes.User")
    @patch("apps.user.routes.bcrypt")
    @patch("apps.user.routes.login_user", return_value=True)
    def test_login(self, mock_login_user, mock_bcrypt, mock_user) -> None:
        user = User(email="test@example.com", password="password")
        mock_user.query.filter_by.return_value.first.return_value = user
        mock_bcrypt.check_password_hash.return_value = True

        response = self.client.post(
            "/login", data={"email": "test@example.com", "password": "password"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Your are logged in succesfully", response.data)

    @patch("apps.user.routes.login_required", return_value=lambda f: f)
    @patch("apps.user.routes.logout_user")
    @patch("apps.user.routes.redirect")
    def test_logout_without_login(
        self, mock_redirect, mock_logout_user, mock_login_required
    ) -> None:
        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
