import datetime
from geopy.exc import GeopyError, GeocoderTimedOut
import os
import tempfile

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.test import RequestFactory
from django.core.urlresolvers import reverse

from races.models import Location, Race, Season, Organizer
from races.views import RaceDetailView, CurrentSeasonRaceListView
from settings import base


class RaceTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        tempfile.tempdir = os.path.join(
            base.MEDIA_ROOT, 'flyers/2014-15/2015_01_03'
        )
        # tf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        # tf.close()
        tf_invalid = tempfile.NamedTemporaryFile(delete=False, suffix='.doc')
        tf_invalid.close()

        # self.flyer_upload = tf.name
        self.flyer_upload_invalid = tf_invalid.name

        self.season = Season.objects.create(
            opening_year=2014,
            closing_year=2015,
            slug='2014-2015',
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

        self.race = Race.objects.create(
            date=datetime.date(2015, 1, 3),
            season=self.season,
            location=self.location,
            organizer=self.organizer,
            description='A very muddy race.',
            pre_registration_link='http://pre-reg.com',
            flyer_upload=self.flyer_upload_invalid
        )

        self.bad_location = Location.objects.create(
            city='Nowhere',
            state='NC',
            zip_code=45321,
            address='111 Main Street',
        )

    def test_race_view_renders_template(self):
        pk = self.race.pk
        request = self.factory.get(reverse('race_detail', kwargs={'pk': pk}))
        response = RaceDetailView.as_view()(request, pk=pk)
        self.assertEqual(response.template_name[0], 'races/race_detail.html')

    def test_race_view_returns(self):
        pk = self.race.pk
        request = self.factory.get(reverse('race_detail', kwargs={'pk': pk}))
        response = RaceDetailView.as_view()(request, pk=pk)
        self.assertEqual(response.status_code, 200)

    def test_season_view_renders_template(self):
        slug = self.season.slug
        request = self.factory.get(reverse('current_season_race_list', kwargs={'slug': slug}))
        response = CurrentSeasonRaceListView.as_view()(request, slug=slug)
        self.assertEqual(response.template_name[0], 'races/current_season_race_list.html')

    def test_season_view_returns(self):
        slug = self.season.slug
        request = self.factory.get(reverse('current_season_race_list', kwargs={'slug': slug}))
        response = CurrentSeasonRaceListView.as_view()(request, slug=slug)
        self.assertEqual(response.status_code, 200)

    def test_geocoding_bad_data(self):
        self.assertIsNone(self.bad_location.latitude and self.bad_location.longitude)


    def test_invalid_file_type(self):
        race = self.race
        self.assertRaises(ValidationError, race.full_clean)


    def tearDown(self):
        os.remove(self.flyer_upload)
        os.remove(self.flyer_upload_invalid)
        season = Season.objects.all()
        season.delete()
        organizer = Organizer.objects.all()
        organizer.delete()
        location = Location.objects.all()
        location.delete()
        race = Race.objects.all()
        race.delete()
