import datetime
from geopy.exc import GeopyError, GeocoderTimedOut

from django.test import TestCase
from django.test import RequestFactory

from races.models import Location


class HomePageText(TestCase):
    def setUp(self):
        self.bad_location = Location.objects.create(
            city='Nowhere',
            state='NC',
            zip_code=45321,
            address='111 Main Street',
        )


    def test_geocoding_bad_data(self):
        self.assertIsNone(self.bad_location.latitude and self.bad_location.longitude)


    def test_file_upload_validation(self):
        pass


    def tearDown(self):
        location = Location.objects.all()
        location.delete()
