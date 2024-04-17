import sys
import unittest
from os.path import abspath, dirname

sys.path.insert(0, abspath(dirname(__file__)) + "/../../")


from apps import create_app

app = create_app()


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_app(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sign Up", response.data)


if __name__ == "__main__":
    unittest.main()
