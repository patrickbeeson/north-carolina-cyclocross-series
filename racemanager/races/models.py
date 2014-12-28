import datetime
from geopy.geocoders import Nominatim
from localflavor.us.models import USStateField, PhoneNumberField

from django.db import models


TODAY = datetime.datetime.today()
CURRENT_MONTH = datetime.datetime.today().month


class CurrentSeasonManager(models.Manager):
    """
    Manager to get current season specified, or the latest by closing date.
    """
    def get_queryset(self):
        return super(CurrentSeasonManager, self).get_queryset().filter(is_current_season).latest()[0]


class UpcomingRaceManager(models.Manager):
    """
    Manager to get upcoming races.
    """
    def get_queryset(self):
        return super(UpcomingRaceManager, self).get_queryset().filter(date__gte=TODAY)


class UpcomingRacesForWeekendManager(models.Manager):
    """
    Manager to get upcoming weekend's races.
    """
    def get_queryset(self):
        upper_limit = today + datetime.timedelta(days=(6 - today.weekday()))
        lower_limit = today + datetime.timedelta(days=(5 - today.weekday()))
        return super(UpcomingRacesForWeekendManager, self).get_queryset().filter(date__range=(lower_limit, upper_limit))


class UpcomingRacesForMonthManager(models.Manager):
    """
    Manager to get this month's upcoming races after this weekend.
    """
    def get_queryset(self):
        upper_limit = today + datetime.timedelta(days=(6 - today.weekday()))
        lower_limit = today + datetime.timedelta(days=(5 - today.weekday()))
        return super(UpcomingRacesForMonthManager, self).get_queryset().filter(date__month=CURRENT_MONTH).exclude(date__range=(lower_limit, upper_limit))


class Season(models.Model):
    """
    A season to hold races for a given year range.
    """
    opening_year = models.PositiveSmallIntegerField(
        help_text='The year in which the season opens (i.e. 2014).',
    )
    closing_year = models.PositiveSmallIntegerField(
        help_text='The year in which the season ends (i.e. 2015).',
    )
    slug = models.SlugField(
        help_text='Will populate from opening and/or closing year fields.',
        unique=True
    )
    results_link = models.URLField(
        help_text='Optional.',
        blank=True,
        default=''
    )
    results_upload = models.FileField(
        help_text='Optional. PDF files only.',
        blank=True,
        default=''
    )
    is_current_season = models.BooleanField(
        help_text='Indicates whether the season is the current season displayed',
        default=False
    )
    objects = models.Manager()
    current_season = CurrentSeasonManager()

    class Meta:
        ordering = ['-closing_year']

    def __str__(self):
        return ('{}-{}'.format(self.opening_year, str(self.closing_year)[2:4]))


class Organizer(models.Model):
    """
    A person or entity organizing the race.
    """
    name = models.CharField(
        max_length=200,
        help_text='Limited to 200 characters. Should be a person, ideally.',
        default=''
    )
    phone = USPhoneNumberField(
        help_text='Optional. Phone numbers must be in XXX-XXX-XXXX format.',
        blank=True,
        null=True
    )
    email = models.EmailField(
        help_text='Optional.',
        blank=True,
        default=''
    )
    website = models.URLField(
        help_text='Optional.',
        blank=True,
        default=''
    )

    def __str__(self):
        return self.name

class Location(models.Model):
    """
    A race location.
    """
    city = models.CharField(
        max_length=100,
        help_text='Limited to 100 characters.',
        default=''
    )
    state = USStateField(
        default='NC'
    )
    zip_code = models.PositiveIntegerField(
        max_length=5,
        help_text='Limited to 5 characters.'
    )
    address = models.CharField(
        max_length=200,
        help_text='Limited to 200 characters. The numbered street \
        address of the race. For example: 151 Piedmont Ave.',
        default=''
    )
    description = models.TextField(
        help_text='Optional. A brief description of the location. This is \
        to help racers find the course.',
        blank=True,
        default=''
    )
    latitude = models.FloatField(
        blank=True,
        null=True
    )
    longitude = models.FloatField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['city']

    def __str__(self):
        return self.address

    def save(self, *args, **kwargs):
        """
        Geocode the location based on address and zip code.
        """
        geolocator = Nominatim()
        location = geolocator.geocode('{} {}'.format(self.address, self.zip_code))
        self.latitude = location.latitude
        self.longitude = location.longitude
        super(Location, self).save(*args, **kwargs)


class Race(models.Model):
    """
    A race within a series.
    """
    date = models.DateField()
    season = models.ForeignKey(Season)
    location = ForeignKey(Location)
    organizer = ForeignKey(Organizer)
    description = models.TextField(
        default='A brief description of the race course, ideally.'
    )
    pre_registration_link = models.URLField(
        help_text='Optional.',
        blank=True,
        default=''
    )
    flyer_upload = models.FileField(
        help_text='Optional. PDF files only.',
        blank=True,
        default=''
    )
    results_link = models.URLField(
        help_text='Optional.',
        blank=True,
        default=''
    )
    results_upload = models.FileField(
        help_text='Optional. PDF files only.',
        blank=True,
        default=''
    )
    objects = models.Manager()
    upcoming_races = UpcomingRaceManager()
    upcoming_races_for_weekend = UpcomingRacesForWeekendManager()
    upcoming_races_for_month = UpcomingRacesForMonthManager()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return ('{}, {}'.format(self.date.strftime('%Y %b %d'), self.location.city))
