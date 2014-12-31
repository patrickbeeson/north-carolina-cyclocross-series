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
NEXT_MONTH = (datetime.date.today().month + 1) % 12 or 12
UPPER_LIMIT = TODAY + datetime.timedelta(days=(6 - TODAY.weekday()))
LOWER_LIMIT = TODAY + datetime.timedelta(days=(5 - TODAY.weekday()))

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


class ResultsMixin(object):
    """
    Mixin object to allow getting of results across models.
    """

    def has_results(self):
        "Determine if results are available in either form."
        if self.results_link or self.results_upload:
            return True

    def get_results(self):
        "Gets the results in whatever form is made available."
        if self.results_link and self.results_upload:
            return [self.results_link, self.results_upload]
        elif self.results_link:
            return self.results_link
        elif self.results_upload:
            return self.results_upload


class CurrentSeasonManager(models.Manager):
    """
    Manager to get current season specified, or the latest by closing date.
    """
    def get_queryset(self):
        return super(CurrentSeasonManager, self).get_queryset().filter(is_current_season=True).latest('closing_year')


class PastRaceManager(models.Manager):
    """
    Manager to get past races.
    """
    def get_queryset(self):
        return super(PastRaceManager, self).get_queryset().filter(date__lt=TODAY)


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
        return super(UpcomingRacesForWeekendManager, self).get_queryset().filter(date__range=(LOWER_LIMIT, UPPER_LIMIT))


class UpcomingRacesForMonthManager(models.Manager):
    """
    Manager to get this month's upcoming races after this weekend.
    """
    def get_queryset(self):
        return super(UpcomingRacesForMonthManager, self).get_queryset().filter(date__month=CURRENT_MONTH).exclude(date__range=(LOWER_LIMIT, UPPER_LIMIT))


class UpcomingRacesForNextMonthManager(models.Manager):
    """
    Manager to get next month's upcoming races after this weekend.
    """
    def get_queryset(self):
        return super(UpcomingRacesForNextMonthManager, self).get_queryset().filter(date__month=NEXT_MONTH).exclude(date__range=(LOWER_LIMIT, UPPER_LIMIT))


class Season(ResultsMixin, models.Model):
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

    @property
    def current_season_has_ended(self):
        "Determine if current season has ended"
        if self.race_set.all():
            if self.race_set.last().date < TODAY:
                return True

    def get_absolute_url(self):
        return reverse('races:current_season_race_list', args=[str(self.slug)])

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
        default='',
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

    @property
    def has_geocode(self):
        "Check whether the location has coordinates"
        if self.latitude and self.longitude:
            return True


class Race(ResultsMixin, models.Model):
    """
    A race within a series.
    """
    date = models.DateField()
    season = models.ForeignKey(Season)
    location = models.ForeignKey(Location)
    organizer = models.ForeignKey(Organizer)
    description = models.TextField(
        help_text='A brief description of the race course, ideally. No HTML or formatting is allowed.',
        default=''
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
    upcoming_races_for_next_month = UpcomingRacesForNextMonthManager()
    past_races = PastRaceManager()

    @property
    def has_expired(self):
        "Function to determine whether the race is in the past"
        if self.date < TODAY:
            return True

    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse('races:race_detail', args=[str(self.season.slug), int(self.pk)])

    def __str__(self):
        return ('{}, {}'.format(self.date.strftime('%Y %b %d'), self.location.city))
