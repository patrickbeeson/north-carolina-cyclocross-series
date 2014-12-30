import datetime

from django.test import TestCase
from django.test import RequestFactory

from homepage.views import HomePageView
from races.models import Season, Organizer, Location, Race


class HomePageTest(TestCase):

    def setUp(self):
        self.request = RequestFactory().get('/')
        self.view = HomePageView.as_view()

        self.season = Season.objects.create(
            opening_year=2014,
            closing_year=2015,
            slug='2014-15',
            is_current_season=True,
        )

        self.organizer = Organizer.objects.create(
            name='Joe Organizer',
            phone='555-555-5555',
            email='joe@gmail.com',
            website='http://racenow.com',
        )

        self.location = Location.objects.create(
            city='Winston-Salem',
            state='NC',
            zip_code=27101,
            address='151 Piedmont Avenue',
            description='Take the first left past the golf course.'
        )

        self.race_this_weekend = Race.objects.create(
            date=datetime.date(2015, 1, 3),
            season=self.season,
            location=self.location,
            organizer=self.organizer,
            description='A very muddy race.',
            pre_registration_link='http://pre-reg.com',
        )
        self.race_this_month = Race.objects.create(
            date=datetime.date(2015, 1, 10),
            season=self.season,
            location=self.location,
            organizer=self.organizer,
            description='A very muddy race.',
            pre_registration_link='http://pre-reg.com',
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

    def test_home_page_returns_upcoming_races_for_weekend(self):
        response = self.view(self.request, weekend_race_list=self.race_this_weekend)
        self.assertEqual(response.context_data['weekend_race_list'][0], self.race_this_weekend)

    def test_home_page_returns_upcoming_races_for_month(self):
        response = self.view(self.request, remaining_races_for_month_list=self.race_this_month)
        self.assertEqual(response.context_data['remaining_races_for_month_list'][0], self.race_this_month)

    def tearDown(self):
        season = Season.objects.all()
        season.delete()
        organizer = Organizer.objects.all()
        organizer.delete()
        location = Location.objects.all()
        location.delete()
        race = Race.objects.all()
        race.delete()
