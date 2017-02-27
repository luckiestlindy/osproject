from django.contrib import admin

from .models import Event, Musician, Ensemble, Song

class MusicianAdmin(admin.ModelAdmin):
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
    list_filter = ('event_type', 'event_date','ensemble_type',)
    fieldsets = (
        ('Status', {
            'fields': ('status',)
        }),
        ('Client Details', {
            'fields': ('client_name','client_email', 'client_phone', 'contact_pref')
        }),
        ('Event Details', {
            'fields': ('event_type', 'event_date', 'start_time', 'event_duration','ensemble_type', 'performers_duration', 'performers_required_time', 'expected_guests')
        }),
        ('Venue Details', {
            'fields': ('venue_name', 'address', 'city')
        }),
        ('Performers', {
            'fields': ('musician_one', 'musician_two', 'musician_three', 'musician_four', 'musician_five')
        }),

    )

    
admin.site.register(Musician, MusicianAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Ensemble, EnsembleAdmin)
admin.site.register(Song, SongAdmin)

