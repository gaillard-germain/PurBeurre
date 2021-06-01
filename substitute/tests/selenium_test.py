from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager

from ..models import Product, Allergen


class PurBeurreSeleniumTestCase(StaticLiveServerTestCase):

    def setUp(self):
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        self.driver = webdriver.Firefox(
            executable_path=GeckoDriverManager().install(),
            firefox_options=opts
        )
        self.wait = WebDriverWait(self.driver, 1000)
        self.addCleanup(self.driver.quit)

        allergen = Allergen.objects.create(name='fake')

        product = Product.objects.create(
            id=1,
            name='fake product',
            brands='fake brand',
            tags='fake, test',
            ingredients='fake, fake',
            additives='E111, E222',
            labels='fake label',
            stores='super fake',
            link="https://fake-product.html",
            nutriscore="e",
            image_url='http://fake.jpg',
            keywords="fake keywords",
            compared_to="fake",
            last_modified_t=1
        )
        product.allergens.add(allergen)

        product = Product.objects.create(
            id=2,
            name='test product',
            brands='test brand',
            tags='fake, test',
            ingredients='test, test',
            additives='E111, E222',
            labels='test label',
            stores='super test',
            link="https://test-product.html",
            nutriscore="a",
            image_url='http://test.jpg',
            keywords="test try",
            compared_to="test",
            last_modified_t=1
        )
        product.allergens.add(allergen)

    def test_create_account_and_add_fav(self):
        self.driver.get(self.live_server_url)
        self.assertIn('Pur Beurre', self.driver.title)

        create_account = self.driver.find_element_by_id('create')
        ActionChains(self.driver).click(create_account).perform()
        self.wait.until(lambda driver:
                        self.driver.find_element_by_id("submit_new_user"))

        assert self.driver.current_url.endswith('/substitute/signup/')

        username = self.driver.find_element_by_id('id_username')
        email = self.driver.find_element_by_id('id_email')
        password1 = self.driver.find_element_by_id('id_password1')
        password2 = self.driver.find_element_by_id('id_password2')
        submit = self.driver.find_element_by_id('submit_new_user')

        username.send_keys('fake-user')
        email.send_keys('fake@foo.bar')
        password1.send_keys('nofxat411')
        password2.send_keys('nofxat411')
        submit.send_keys(Keys.RETURN)

        self.wait.until(lambda driver:
                        self.driver.find_element_by_id("search_input"))

        assert self.driver.current_url == '{}/'.format(self.live_server_url)

        search = self.driver.find_element_by_id('search_input')
        submit = self.driver.find_element_by_id('submit_search')

        search.send_keys('fake keywords')
        submit.send_keys(Keys.RETURN)

        self.wait.until(lambda driver:
                        self.driver.find_element_by_id("substitutes"))

        assert self.driver.current_url.endswith(
            '/substitute/results/fake+keywords/no%20filter/')

        self.driver.find_element_by_class_name("add-fav").click()
        self.wait.until(lambda driver:
                        self.driver.find_element_by_id("myfav"))
        myfav_link = self.driver.find_element_by_id("myfav")
        ActionChains(self.driver).click(myfav_link).perform()

        self.wait.until(lambda driver:
                        self.driver.find_element_by_id("favorites"))

        assert self.driver.current_url.endswith('/substitute/favorites/')
