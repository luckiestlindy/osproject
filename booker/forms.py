from django import forms
from .models import Event, Selection


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['musician_one', 'musician_two', 'musician_three', 'musician_four', 'musician_five', 'status', 'fee', 'deposit', 'deposit_duedate', 'balance_duedate', 'deposit_recieved','balance_recieved', 'quote_message','prelude_one','prelude_two', 'prelude_three', 'prelude_four', 'prelude_five', 'processional', 'num_grandmothers', 'num_mothers', 'num_bridesmaids', 'num_flowers', 'num_rings', 'bridal', 'unity', 'communion', 'recessional']
    
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
            'start_time': 'What is the approximate start time of your event?',
            'performers_required_time': 'What time are the perfomers required?',
            'venue_name': 'Please enter the name of the venue here (if applicable)',
            'address': 'Please enter the venue address here',
            'event_outdoors': 'Will your event take place outdoors?',
            'comments': 'Please add any or questions or comments here. Thank you!'
            
        }
class SelectionsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SelectionsForm, self).__init__(*args,**kwargs)
        arrangement = Event.objects.get(pk = self.instance.id)
        queryset = Selection.objects.filter(arrangement=arrangement.ensemble_type)
        self.fields['prelude_one'].queryset = queryset
        self.fields['prelude_two'].queryset = queryset
        self.fields['prelude_three'].queryset = queryset
        self.fields['prelude_four'].queryset = queryset
        self.fields['prelude_five'].queryset = queryset
        self.fields['processional'].queryset = queryset
        self.fields['bridal'].queryset = queryset
        self.fields['unity'].queryset = queryset
        self.fields['communion'].queryset = queryset
        self.fields['recessional'].queryset = queryset
    class Meta:
        model = Event
        fields = ['prelude_one', 'prelude_two','prelude_three', 'prelude_four', 'prelude_five', 'processional', 'num_grandmothers', 'num_mothers', 'num_bridesmaids', 'num_rings', 'num_flowers', 'bridal', 'unity', 'communion', 'recessional',]
        # exclude = ['event','bridesmaids',]
        labels = {
            'prelude_one': 'Prelude Selection 1',
            'prelude_two': 'Prelude Selection 2',
            'prelude_three': 'Prelude Selection 3',
            'prelude_four': 'Prelude Selection 4',
            'prelude_five': 'Prelude Selection 5',
            'processional': 'Processional 1',
            'num_grandmothers': "How many Grandmothers?",
            'num_mothers': "How many Mothers?",
            'num_bridesmaids': "How many Bridesmaids?",
            'num_rings': 'How many ring bearers?',
            'num_flowers': 'How many  flower girls?',
            'bridal': 'Bridal Entrance:',
            'unity': 'Unity/Candle Ceremony:',
            'communion': 'Communion Ceremony:',
            'recessional': 'Recessional:',
        }

   