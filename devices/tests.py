from django.test import TestCase

class DummyTestCase(TestCase):

    def test_stupid(self):
        self.assertEqual(1, 2)