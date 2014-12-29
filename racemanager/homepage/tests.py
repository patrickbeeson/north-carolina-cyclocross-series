from django.test import TestCase
from django.test import RequestFactory

from homepage.views import HomePageView
from races.models import Season


class HomePageText(TestCase):

    def setUp(self):
        self.request = RequestFactory().get('/')
        self.view = HomePageView.as_view()

        self.season = Season.objects.create(
            opening_year=2014,
            closing_year=2015,
            slug='2014-15',
            is_current_season=True,
        )

    def test_home_page_renders_template(self):
        response = self.view(self.request)
        self.assertEqual(response.template_name, ['home.html'])

    def test_home_page_returns(self):
        response = self.view(self.request)
        self.assertEqual(response.status_code, 200)

    def test_home_page_returns_season(self):
        response = self.view(self.request, current_season=self.season)
        self.assertEqual(response.context_data['current_season'], self.season)

    def tearDown(self):
        season = Season.objects.all()
        season.delete()
