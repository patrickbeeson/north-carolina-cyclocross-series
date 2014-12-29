from django.contrib import admin

from races.models import Race, Location, Organizer, Season


class SeasonAdmin(admin.ModelAdmin):
    list_filter = ('is_current_season', 'opening_year', 'closing_year')
    list_display = ('__str__', 'is_current_season', 'opening_year', 'closing_year')
    list_editable = ['is_current_season']
    prepopulated_fields = {"slug": ("opening_year", "closing_year")}


class OrganizerAdmin(admin.ModelAdmin):
    pass


class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'address')


class RaceAdmin(admin.ModelAdmin):
    list_filter = ('date','season','location')
    search_fields = ('location', 'description')
    list_display = ('date', 'location', 'season')
    fieldsets = (
        (None, {
            'fields': ('date', 'season', 'location', 'organizer', 'description', 'flyer_upload',)
        }),
        ('Registration and results', {
            'classes': ('collapse',),
            'fields': ('pre_registration_link', 'results_upload', 'results_link')
        }),
    )

admin.site.register(Season, SeasonAdmin)
admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Race, RaceAdmin)
