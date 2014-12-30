import datetime
import logging
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeopyError, GeocoderTimedOut
from localflavor.us.models import USStateField, PhoneNumberField

from django.db import models
from django.core.urlresolvers import reverse

from racemanager.utils.validators import validate_file_type

TODAY = datetime.date.today()
CURRENT_MONTH = datetime.date.today().month

logger = logging.getLogger(__name__)


def get_flyers_upload_path(instance, filename):
    "Customize upload path for race flyers"
    return os.path.join(
        "flyers/{season}/{date}/{flyer}".format(
            season=instance.season,
            date=instance.date.strftime('%Y_%b_%d'),
            flyer=filename
        )
    )


def get_results_upload_path(instance, filename):
    "Customize upload path for race results"
    return os.path.join(
        "results/{season}/{date}/{results}".format(
            season=instance.season,
            date=instance.date.strftime('%Y_%b_%d'),
            results=filename
        )
    )


def get_season_results_upload_path(instance, filename):
    "Customize upload path for season results"
    return os.path.join(
        "results/{season}/{results}".format(
            season=instance,
            results=filename
        )
    )



class CurrentSeasonManager(models.Manager):
    """
    Manager to get current season specified, or the latest by closing date.
    """
    def get_queryset(self):
        return super(CurrentSeasonManager, self).get_queryset().filter(is_current_season=True).latest('closing_year')


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
        upper_limit = TODAY + datetime.timedelta(days=(6 - TODAY.weekday()))
        lower_limit = TODAY + datetime.timedelta(days=(5 - TODAY.weekday()))
        return super(UpcomingRacesForWeekendManager, self).get_queryset().filter(date__range=(lower_limit, upper_limit))


class UpcomingRacesForMonthManager(models.Manager):
    """
    Manager to get this month's upcoming races after this weekend.
    """
    def get_queryset(self):
        upper_limit = TODAY + datetime.timedelta(days=(6 - TODAY.weekday()))
        lower_limit = TODAY + datetime.timedelta(days=(5 - TODAY.weekday()))
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
        default='',
        upload_to=get_season_results_upload_path,
        validators=[validate_file_type]
    )
    is_current_season = models.BooleanField(
        help_text='Indicates whether the season is the current season displayed',
        default=False
    )
    objects = models.Manager()
    current_season = CurrentSeasonManager()

    class Meta:
        ordering = ['-closing_year']

    def get_absolute_url(self):
        return reverse('current_season_race_list', args=[str(self.slug)])

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
    phone = PhoneNumberField(
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

    class Meta:
        ordering = ['name']

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
        if self.latitude and self.longitude:
            return
        else:
            try:
                geolocator = Nominatim()
                location = geolocator.geocode('{} {}'.format(self.address, self.zip_code))
                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
                    super(Location, self).save(*args, **kwargs)
            except Exception as err:
                logger.error('There was a problem geocoding this address: {}'.format(err))



class Race(models.Model):
    """
    A race within a series.
    """
    date = models.DateField()
    season = models.ForeignKey(Season)
    location = models.ForeignKey(Location)
    organizer = models.ForeignKey(Organizer)
    description = models.TextField(
        help_text='A brief description of the race course, ideally.',
        default='',
        blank=True,
    )
    pre_registration_link = models.URLField(
        help_text='Optional.',
        blank=True,
        default=''
    )
    flyer_upload = models.FileField(
        help_text='Optional. PDF files only.',
        blank=True,
        default='',
        upload_to=get_flyers_upload_path,
        validators=[validate_file_type]
    )
    results_link = models.URLField(
        help_text='Optional.',
        blank=True,
        default=''
    )
    results_upload = models.FileField(
        help_text='Optional. PDF files only.',
        blank=True,
        default='',
        upload_to=get_results_upload_path,
        validators=[validate_file_type]
    )
    objects = models.Manager()
    upcoming_races = UpcomingRaceManager()
    upcoming_races_for_weekend = UpcomingRacesForWeekendManager()
    upcoming_races_for_month = UpcomingRacesForMonthManager()

    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse('race_detail', args=[int(self.pk)])

    def __str__(self):
        return ('{}, {}'.format(self.date.strftime('%Y %b %d'), self.location.city))
