from django.test import TestCase
from django.test import RequestFactory

from homepage.views import HomePageView


class HomePageText(TestCase):

    def setUp(self):
        self.request = RequestFactory().get('/')
        self.view = HomePageView.as_view()

    def test_home_page_renders_template(self):
        response = self.view(self.request)
        self.assertEqual(response.template_name, ['home.html'])

    def test_home_page_returns(self):
        response = self.view(self.request)
        self.assertEqual(response.status_code, 200)
