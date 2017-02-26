from __future__ import unicode_literals
from django.urls import reverse
from django.db import models

# Create your models here.

class Musician(models.Model):
    name = models.CharField(max_length = 200)
    phone = models.CharField(max_length = 10, blank = True)
    email = models.EmailField(blank = True)
    instrument = models.CharField(max_length=100, choices=[('piano', 'piano'), ('violin','violin'), ('viola', 'viola'), ('cello', 'cello') ],)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='musicians', blank = True, null = True)
    website = models.URLField(max_length=200, blank = True)
    def __str__(self):
        return self.name

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
    event_type = models.CharField(max_length = 100, choices=[('wedding','wedding'), ('private event','private event'),('company event','company event'), ('other', 'other')])
    ensemble_type = models.ForeignKey(Ensemble, blank=True, null=True)
    event_date = models.DateField(auto_now = False)
    start_time_known = models.BooleanField(default=False)
    start_time = models.TimeField(auto_now= False, blank = True, null = True)
#    end_time = models.TimeField(auto_now= False, blank = True, null = True)
    event_duration = models.CharField(max_length = 100, choices=[('less than 1 hour', 'less than 1 hour'), ('1 hour', '1 hour'), ('2 hours', '2 hours'), ('3 hours', '3 hours'), ('4 hours', '4 hours'), ('more than 4 hours', 'more than 4 hours')], blank = True)
    performers_entire_duration = models.BooleanField(default=False)
    performers_duration = models.CharField(max_length = 100, choices=[('less than 1 hour', 'less than 1 hour'), ('1 hour', '1 hour'), ('2 hours', '2 hours'), ('3 hours', '3 hours'), ('4 hours', '4 hours'), ('more than 4 hours', 'more than 4 hours')], blank = True)
    performers_required_time = models.TimeField(auto_now= False, blank = True, null = True)
    city = models.CharField(max_length = 200, blank = True)
    address_known = models.BooleanField(default=False)
    venue_name = models.CharField(max_length = 200, blank = True)
    address = models.CharField(max_length = 200, blank = True)
    expected_guests = models.IntegerField(blank = True, null = True)
    contact_pref = models.CharField(max_length = 100, choices =[('email','email'), ('phone','phone')])
    comments = models.TextField(max_length = 800, blank = True)
    musician_one = models.ForeignKey(Musician, blank = True, null = True, related_name='musician_one')
    musician_two = models.ForeignKey(Musician, blank = True, null = True, related_name='musician_two')
    musician_three = models.ForeignKey(Musician, blank = True, null = True, related_name='musician_three')
    musician_four = models.ForeignKey(Musician, blank = True, null = True, related_name='musician_four')
    musician_five = models.ForeignKey(Musician, blank = True, null = True, related_name='musician_five')
    status = models.CharField(max_length=100, choices=[('inquiry','inquiry'), ('booked','booked'),('paid','paid')], default='inquiry')
    def __str__(self):
        event_label = (self.client_name, self.event_type)
        return '{}: {}- {}'.format(self.client_name, self.event_type, self.event_date)
    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})
