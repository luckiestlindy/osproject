from django import forms
from .models import Event, SelectionList, Selection


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
            'start_time': 'What is the approximate start time of your event?',
            'performers_required_time': 'What time are the perfomers required?',
            'venue_name': 'Please enter the name of the venue here (if applicable)',
            'address': 'Please enter the venue address here',
            'event_outdoors': 'Will your event take place outdoors?',
            'comments': 'Please add any or questions or comments here. Thank you!'
            
        }
class SelectionForm(forms.ModelForm):
    def __init__(self,arrangement,*args,**kwargs):
        super (SelectionForm,self ).__init__(*args,**kwargs) # populates the post
#        print(arrangement.id)
        
#        self.fields['website'].queryset = Website.objects.filter(organization__primary_account=request.user)
        self.fields['prelude_one'].queryset = Selection.objects.get(arrangement=1)
#        self.fields['client'].queryset = Client.objects.filter(company=company)
    class Meta:
        model = SelectionList
#        fields = '__all__'
        exclude = ['event','bridesmaids',]
        labels = {
            'prelude_one': 'Prelude Selection 1',
            'prelude_two': 'Prelude Selection 2',
            'prelude_three': 'Prelude Selection 3',
            'prelude_four': 'Prelude Selection 4',
            'prelude_five': 'Prelude Selection 5',
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