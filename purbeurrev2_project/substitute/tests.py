from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Profile
from django.http import JsonResponse


class SignUpPageTestCase(TestCase):

    def test_signup_page_returns_200(self):
        response = self.client.get(reverse('substitute:signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_add_new_profile(self):
        old_profile = Profile.objects.count()
        response = self.client.post(reverse('substitute:signup'), {
            'username': 'fake-user',
            'email': 'fake@fake.com',
            'password1': 'Fake1234',
            'password2': 'Fake1234'
        })
        new_profile = Profile.objects.count()
        self.assertEqual(new_profile, old_profile+1)


class LogoutPageTestCase(TestCase):

    def test_logout_page_returns_200(self):
        response = self.client.get(reverse('substitute:logout'))
        self.assertEqual(response.status_code, 200)


class MyAccountPageTestCase(TestCase):

    def test_myaccount_page_returns_200(self):
        response = self.client.get(reverse('substitute:myaccount'))
        self.assertEqual(response.status_code, 200)


class IndexPageTestCase(TestCase):

    def test_index_page_returns_200(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_page_returns_302(self):
        form = {'query': 'fake'}
        response = self.client.post(reverse('index'), form)
        self.assertEqual(response.status_code, 302)


class ResultsPageTestCase(TestCase):

    def setUp(self):
        fake = Product.objects.create(
            keywords="fake keywords",
            compared_to="fake"
            )
        self.product = Product.objects.get(keywords="fake keywords")
        fake = Product.objects.create(tags="fake tags")
        self.alternatives = Product.objects.filter(
            tags__icontains=self.product.compared_to).exclude(
                                                id=self.product.id)

    def test_results_page_returns_200(self):
        query = "fake+keywords"
        product = self.product
        alternatives = self.alternatives
        response = self.client.get(reverse('substitute:results',
                                            args=(query,)))
        self.assertEqual(response.status_code, 200)

    def test_results_page_returns_404(self):
        query = "nothing+will+match"
        product = self.product
        alternatives = self.alternatives
        response = self.client.get(reverse('substitute:results',
                                            args=(query,)))
        self.assertEqual(response.status_code, 404)


class FavoritesPageTestCase(TestCase):

    def setUp(self):
        self.username = 'fakeuser'
        self.email = 'fake@fake.com'
        self.password = 'Fake1234'
        self.user = User.objects.create_user(self.username, self.email,
                                             self.password)

        fake = Product.objects.create(name="fake product")
        self.product = Product.objects.get(name="fake product")

        fake = Profile.objects.create(user=self.user)
        self.profile = Profile.objects.get(user=self.user)

        self.profile.favorite.add(self.product)

    def test_favorites_page_returns_200(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        favorites = Product.objects.filter(profiles=self.profile)
        response = self.client.get(reverse('substitute:favorites'))
        self.assertEqual(response.status_code, 200)


class DetailPageTestCase(TestCase):

    def setUp(self):
        fake = Product.objects.create(name="fake product")
        self.product = Product.objects.get(name="fake product")

    def test_detail_page_returns_200(self):
        product_id = self.product.id
        response = self.client.get(reverse('substitute:detail',
                                            args=(product_id,)))
        self.assertEqual(response.status_code, 200)


class ToggleFavTestCase(TestCase):

    def setUp(self):
        self.username = 'fakeuser'
        self.email = 'fake@fake.com'
        self.password = 'Fake1234'
        self.user = User.objects.create_user(self.username, self.email,
                                             self.password)
        fake = Product.objects.create(name="fake product")
        self.product = Product.objects.get(name="fake product")

        fake = Profile.objects.create(user=self.user)
        self.profile = Profile.objects.get(user=self.user)

    def test_togglefav_response_loggedin(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        profile = self.profile
        product_id = self.product.id
        toggle = 'on'
        response = self.client.post(reverse('substitute:togglefav'), {
            'product_id': product_id,
            'toggle': toggle
        })
        result = JsonResponse({"allowed": True})
        self.assertEqual(response.content, result.content)

    def test_togglefav_response_loggedout(self):
        product_id = self.product.id
        toggle = 'on'
        response = self.client.post(reverse('substitute:togglefav'), {
            'product_id': product_id,
            'toggle': toggle
        })
        result = JsonResponse({"allowed": False})
        self.assertEqual(response.content, result.content)

    def test_fav_is_registered(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        profile = self.profile
        product_id = self.product.id
        toggle = 'on'
        old_fav = profile.favorite.count()
        response = self.client.post(reverse('substitute:togglefav'), {
            'product_id': product_id,
            'toggle': toggle
        })
        new_fav = profile.favorite.count()
        self.assertEqual(new_fav, old_fav+1)

    def test_fav_is_removed(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        profile = self.profile
        profile.favorite.add(self.product)
        product_id = self.product.id
        toggle = 'off'
        old_fav = profile.favorite.count()
        response = self.client.post(reverse('substitute:togglefav'), {
            'product_id': product_id,
            'toggle': toggle
        })
        new_fav = profile.favorite.count()
        self.assertEqual(new_fav, old_fav-1)
