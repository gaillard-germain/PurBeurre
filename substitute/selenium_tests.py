from django.test import LiveServerTestCase
from selenium import webdriver


class PurBeurreTestCase(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.addCleanup(self.browser.quit)

    def test_create_account_and_add_fav(self):
        print('oooh')
        self.browser.get('http://127.0.0.1:8000/')
        self.assertIn('Pur Beurre', self.browser.title)
