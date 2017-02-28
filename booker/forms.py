from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['musician_one', 'musician_two', 'musician_three', 'musician_four', 'musician_five', 'status', 'fee', 'deposit', 'deposit_duedate', 'balance_duedate', 'deposit_recieved','balance_recieved', 'quote_message',]
    
        widgets = {
            'event_date': forms.DateInput(attrs={'class':'datepicker'}),
            'start_time': forms.TimeInput( attrs={'class': 'timepicker'}),
            'end_time': forms.TimeInput(attrs={'class': 'timepicker'}),
            'performers_required_time': forms.TimeInput(attrs={'class': 'timepicker'}),
            'client_email': forms.EmailInput(),
        }
        labels = {
            'client_name': 'Your name:',
            'client_phone': 'Your phone number:',
            'client_email': 'Your email:',
            'event_type': 'Select Event Type',
            'ensemble_type': 'Select Ensemble Type',
            'event_date': 'What is the date of your event?',
            'start_time_known': 'Do you know the start time for your event?',
            'start_time': 'What is the start time of your event?',
            'performers_entire_duration': 'Will the performers be need for the entire event?',
            'performers_duration': 'How long will they be needed?',
            'performers_required_time': 'What time are the perfomers required?',
            'city': 'In which city will your event be held?',
            'address_known': 'Do you know the name/address for your event venue?',
            'venue_name': 'Please enter the name of the venue here (if applicable)',
            'address': 'Please enter the venue address here',
            'guests': 'How many guests do you expect? (optional)',
            'contact_pref': 'How would prefer to be contacted?',
            'comments': 'Please add any or questions or comments here. Thank you!'
            
        }
       