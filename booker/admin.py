from django.contrib import admin
from .models import Event, Musician, Ensemble, Song, Selection
from django.contrib import admin
from image_cropping import ImageCroppingMixin

# class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
#     pass

# admin.site.register(MyModel, MyModelAdmin)

class SelectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'composer', )
    list_filter = ('arrangement',)

class MusicianAdmin(ImageCroppingMixin,admin.ModelAdmin):
    list_display = ('name', 'instrument', 'website')
    list_filter = ('instrument',)

class EnsembleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    
class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'ensemble',)
    list_filter = ('ensemble',)
    
class EventAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'event_type', 'event_date', 'status',)
    list_editable = ('status',)
    list_filter = ('event_type', 'status','ensemble_type',)
    fieldsets = (
        ('Status', {
            'fields': ('status',)
        }),
        ('Client Details', {
            'fields': ('client_name','client_email', 'client_phone', )
        }),
        ('Event Details', {
            'fields': ('event_type','ensemble_type', 'event_date', 'start_time', 'performers_required_time', 'wedding_options','comments','prelude_one', 'prelude_two', 'prelude_three', 'prelude_four', 'prelude_five', 'processional', 'num_grandmothers', 'num_mothers', 'num_bridesmaids', 'num_flowers', 'num_rings', 'bridal', 'unity', 'communion', 'recessional',)
        }),
        ('Venue Details', {
            'fields': ('venue_name', 'address', 'event_outdoors' )
        }),
        ('Performers', {
            'fields': ('musician_one', 'musician_two', 'musician_three', 'musician_four', 'musician_five')
        }),
        ('Contract', {
            'fields': ('fee','deposit', 'deposit_duedate', 'balance_duedate','deposit_recieved', 'balance_recieved', )
        }),
        ('Message to Client', {
            'fields': ('quote_message',)
        }),
        )
    class Media:
        js = ('booker/js/event.js',)
       
       


    
admin.site.register(Musician, MusicianAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Ensemble, EnsembleAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Selection, SelectionAdmin)


