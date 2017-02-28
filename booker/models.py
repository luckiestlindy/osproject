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
    photo = models.ImageField(upload_to='musicians', blank = True, null = True)
    website = models.URLField(max_length=200, blank = True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('musician_detail', kwargs={'pk': self.pk})
    
class Ensemble(models.Model):
    name = models.CharField(max_length = 100) 
    description = models.CharField(max_length = 200, blank = True)
    members = models.IntegerField()
    photo = models.ImageField(upload_to='ensembles', blank = True, null = True)
    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=125)
    audio_file = models.FileField()
    ensemble = models.ForeignKey(Ensemble)
    def __str__(self):
        return self.name
    
class Event(models.Model):
    client_name = models.CharField(max_length = 200)
    client_phone = models.CharField(max_length = 10)
    client_email = models.EmailField()
    event_type = models.CharField(max_length = 100, choices=EVENT_TYPES)
    ensemble_type = models.ForeignKey(Ensemble, blank=True, null=True)
    event_date = models.DateField(auto_now = False)
    start_time_known = models.BooleanField(default=False)
    start_time = models.TimeField(auto_now= False, blank = True, null = True)
    event_duration = models.CharField(max_length = 100, choices=DURATIONS, blank = True)
    performers_entire_duration = models.BooleanField(default=False)
    performers_duration = models.CharField(max_length = 100, choices=DURATIONS, blank = True)
    performers_required_time = models.TimeField(auto_now= False, blank = True, null = True)
    city = models.CharField(max_length = 200, blank = True)
    address_known = models.BooleanField(default=False)
    venue_name = models.CharField(max_length = 200, blank = True)
    address = models.CharField(max_length = 200, blank = True)
    expected_guests = models.IntegerField(blank = True, null = True)
    contact_pref = models.CharField(max_length = 100, choices =CONTACT_METHODS)
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
#        event_label = (self.client_name, self.event_type)
        return '{}: {}- {}'.format(self.client_name, self.event_type, self.event_date)
    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})

    