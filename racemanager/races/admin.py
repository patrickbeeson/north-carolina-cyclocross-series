from django.contrib import admin

from races.models import Race, Location, Organizer, Season


class SeasonAdmin(admin.ModelAdmin):
    pass


class OrganizerAdmin(admin.ModelAdmin):
    pass


class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'address')


class RaceAdmin(admin.ModelAdmin):
    list_filter = ('date','season','location')
    search_fields = ('location', 'description')
    list_display = ('date', 'location', 'season')
