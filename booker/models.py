from __future__ import unicode_literals
from django.urls import reverse
from django.db import models
from booker.choices import *
# Create your models here.

class Musician(models.Model):
    name = models.CharField(max_length = 200)
    phone = models.CharField(max_length = 10, blank = True)
    email = models.EmailField(blank = True)
    instrument = models.CharField(max_length=100, choices=INSTRUMENT_TYPES)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='booker/musicians', blank = True, null = True)
    website = models.URLField(max_length=200, blank = True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('musician_detail', kwargs={'pk': self.pk})
    
class Ensemble(models.Model):
    name = models.CharField(max_length = 100) 
    description = models.CharField(max_length = 200, blank = True)
    members = models.IntegerField()
    photo = models.ImageField(upload_to='booker/ensembles', blank = True, null = True)
    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=125)
    audio_file = models.FileField(upload_to='booker/songs', blank=True, null=True)
    ensemble = models.ForeignKey(Ensemble)
    def __str__(self):
        return self.name
    
class Event(models.Model):
    client_name = models.CharField(max_length = 200)
    client_phone = models.CharField(max_length = 10)
    client_email = models.EmailField()
    event_type = models.CharField(max_length = 100, choices=EVENT_TYPES)
    wedding_options = models.CharField(max_length = 100, choices=WEDDING_OPTIONS, default = '1')
    ensemble_type = models.ForeignKey(Ensemble, blank=True, null=True)
    event_date = models.DateField(auto_now = False)
    start_time = models.TimeField(auto_now= False, blank = True, null = True)
    performers_required_time = models.TimeField(auto_now= False, blank = True, null = True)
    venue_name = models.CharField(max_length = 200, blank = True)
    address = models.CharField(max_length = 200, blank = True)
    event_outdoors = models.CharField(max_length = 20, choices=OUTDOOR_CHOICES, default = '1')
    comments = models.TextField(max_length = 800, blank = True)
    musician_one = models.ForeignKey(Musician, blank = True, null = True, related_name='musician_one')
    musician_two = models.ForeignKey(Musician, blank = True, null = True, related_name='musician_two')
    musician_three = models.ForeignKey(Musician, blank = True, null = True, related_name='musician_three')
    musician_four = models.ForeignKey(Musician, blank = True, null = True, related_name='musician_four')
    musician_five = models.ForeignKey(Musician, blank = True, null = True, related_name='musician_five')
    status = models.CharField(max_length=100, choices=BOOKING_STATUS, default='inquiry')
    fee = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)
    deposit = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)
    deposit_duedate = models.DateField(auto_now = False, blank=True, null=True)
    balance_duedate = models.DateField(auto_now = False, blank=True, null=True)
    deposit_recieved = models.BooleanField(default=False)
    balance_recieved = models.BooleanField(default=False)
    quote_message = models.TextField(max_length = 800, blank = True)
    def __str__(self):
        return '{}: {}- {}'.format(self.client_name, self.event_type, self.event_date)
    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})


class Selection(models.Model):
    name = models.CharField(max_length = 200)
    composer = models.CharField(max_length = 200, blank = True)
    arrangement = models.ManyToManyField(Ensemble, blank=True, related_name = 'arrangement')
    def __str__(self):
        return self.name
    
class SelectionList(models.Model):
    event = models.OneToOneField(Event,on_delete=models.CASCADE, null=False, primary_key=True, related_name='event')
    prelude_one = models.ForeignKey(Selection, blank=True, null=True, related_name = 'prelude_one')
    prelude_two = models.ForeignKey(Selection, blank=True, null=True, related_name = 'prelude_two')
    prelude_three = models.ForeignKey(Selection, blank=True, null=True, related_name = 'prelude_three')
    prelude_four = models.ForeignKey(Selection, blank=True, null=True, related_name = 'prelude_four')
    prelude_five = models.ForeignKey(Selection, blank=True, null=True, related_name = 'prelude_five')
    processional = models.ForeignKey(Selection, blank=True, null=True, related_name = 'processional')
    num_grandmothers = models.IntegerField(null=True, blank=True)
    num_mothers = models.IntegerField(null=True, blank=True)
    num_bridesmaids = models.IntegerField(null=True, blank=True)
    num_flowers = models.IntegerField(null=True, blank=True)
    num_rings = models.IntegerField(null=True, blank=True)
    bridal = models.ForeignKey(Selection, blank=True, null=True, related_name = 'bridal')
    unity = models.ForeignKey(Selection, blank=True, null=True, related_name = 'unity')
    communion = models.ForeignKey(Selection, blank=True, null=True, related_name = 'communion')
    recessional = models.ForeignKey(Selection, blank=True, null=True, related_name = 'recessional')
    def __str__(self):
        return '{} {} ({}) Selections'.format(self.event.client_name, self.event.event_type, self.event.event_date)