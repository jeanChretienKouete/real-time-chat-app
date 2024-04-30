import unittest

if __name__ == "__main__":
    test_loader = unittest.TestLoader()
    suite = test_loader.discover("tests/functionnal")
    test_runner = unittest.TextTestRunner()
    test_runner.run(suite)
