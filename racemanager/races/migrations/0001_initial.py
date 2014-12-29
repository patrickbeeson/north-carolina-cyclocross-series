# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models
import racemanager.utils.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('city', models.CharField(help_text='Limited to 100 characters.', default='', max_length=100)),
                ('state', localflavor.us.models.USStateField(default='NC', max_length=2, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')])),
                ('zip_code', models.PositiveIntegerField(help_text='Limited to 5 characters.', max_length=5)),
                ('address', models.CharField(help_text='Limited to 200 characters. The numbered street         address of the race. For example: 151 Piedmont Ave.', default='', max_length=200)),
                ('description', models.TextField(help_text='Optional. A brief description of the location. This is         to help racers find the course.', blank=True, default='')),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
            ],
            options={
                'ordering': ['city'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(help_text='Limited to 200 characters. Should be a person, ideally.', default='', max_length=200)),
                ('phone', localflavor.us.models.PhoneNumberField(help_text='Optional. Phone numbers must be in XXX-XXX-XXXX format.', blank=True, max_length=20, null=True)),
                ('email', models.EmailField(help_text='Optional.', blank=True, max_length=75, default='')),
                ('website', models.URLField(help_text='Optional.', blank=True, default='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('date', models.DateField()),
                ('description', models.TextField(default='A brief description of the race course, ideally.')),
                ('pre_registration_link', models.URLField(help_text='Optional.', blank=True, default='')),
                ('flyer_upload', models.FileField(default='', help_text='Optional. PDF files only.', blank=True, upload_to='', validators=[racemanager.utils.validators.validate_file_type])),
                ('results_link', models.URLField(help_text='Optional.', blank=True, default='')),
                ('results_upload', models.FileField(default='', help_text='Optional. PDF files only.', blank=True, upload_to='', validators=[racemanager.utils.validators.validate_file_type])),
                ('location', models.ForeignKey(to='races.Location')),
                ('organizer', models.ForeignKey(to='races.Organizer')),
            ],
            options={
                'ordering': ['-date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('opening_year', models.PositiveSmallIntegerField(help_text='The year in which the season opens (i.e. 2014).')),
                ('closing_year', models.PositiveSmallIntegerField(help_text='The year in which the season ends (i.e. 2015).')),
                ('slug', models.SlugField(help_text='Will populate from opening and/or closing year fields.', unique=True)),
                ('results_link', models.URLField(help_text='Optional.', blank=True, default='')),
                ('results_upload', models.FileField(default='', help_text='Optional. PDF files only.', blank=True, upload_to='', validators=[racemanager.utils.validators.validate_file_type])),
                ('is_current_season', models.BooleanField(help_text='Indicates whether the season is the current season displayed', default=False)),
            ],
            options={
                'ordering': ['-closing_year'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='race',
            name='season',
            field=models.ForeignKey(to='races.Season'),
            preserve_default=True,
        ),
    ]
