from django import forms
from .models import Event, Selection, Musician
from django.forms import ModelForm
# from versatileimagefield.fields import SizedImageCenterpointClickDjangoAdminField

# class MusiciansForm(VersatileImageTestModelForm):
# class MusicianForm(VersatileImageTestModelForm):
#     image = SizedImageCenterpointClickDjangoAdminField(required=False)
#     class Meta:
#         model = Musician
#         fields = ('image')

class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args,**kwargs)
        self.fields['client_name'].widget.attrs['class'] = 'form-control' 
        # self.fields['client_name'].widget.attrs['placeholder'] = 'required' 
        self.fields['client_email'].widget.attrs['class'] = 'form-control' 
        # self.fields['client_email'].widget.attrs['placeholder'] = 'required' 
        self.fields['client_phone'].widget.attrs['class'] = 'form-control'
        # self.fields['client_phone'].widget.attrs['placeholder'] = 'required' 
        self.fields['event_type'].widget.attrs['class'] = 'form-control' 
        # self.fields['client_name'].widget.attrs['placeholder'] = 'required' 
        self.fields['ensemble_type'].widget.attrs['class'] = 'form-control' 
        self.fields['event_date'].widget.attrs['class'] = 'form-control datepicker' 
        self.fields['start_time'].widget.attrs['class'] = 'form-control timepicker'  
        self.fields['performers_required_time'].widget.attrs['class'] = 'form-control timepicker'  
        self.fields['venue_name'].widget.attrs['class'] = 'form-control'  
        self.fields['address'].widget.attrs['class'] = 'form-control'  
        self.fields['event_outdoors'].widget.attrs['class'] = 'form-control'  
        self.fields['comments'].widget.attrs['class'] = 'form-control' 
        self.fields['wedding_options'].widget.attrs['class'] = 'form-control'  
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['musician_one', 'musician_two', 'musician_three', 'musician_four', 'musician_five', 'status', 'fee', 'deposit', 'deposit_duedate', 'balance_duedate', 'deposit_recieved','balance_recieved', 'quote_message','prelude_one','prelude_two', 'prelude_three', 'prelude_four', 'prelude_five', 'processional', 'num_grandmothers', 'num_mothers', 'num_bridesmaids', 'num_flowers', 'num_rings', 'bridal', 'unity', 'communion', 'recessional']
    
        widgets = {
            # 'event_date': forms.DateInput(attrs={'class':'datepicker'}),
            # 'start_time': forms.TimeInput( attrs={'class': 'timepicker'}),
            # 'end_time': forms.TimeInput(attrs={'class': 'timepicker'}),
            # 'performers_required_time': forms.TimeInput(attrs={'class': 'timepicker'}),
            'client_email': forms.EmailInput(),
            # self.fields['client_name'].widget.attrs['class'] = 'form-control'            
        }
        labels = {
            'client_name': 'Your name: (required)' ,
            'client_phone': 'Your phone number: (required)',
            'client_email': 'Your email: (required)',
            'event_type': 'Select Event Type (required)',
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
        self.fields['prelude_one'].widget.attrs['class'] = 'form-control'
        self.fields['prelude_one'].queryset = queryset
        self.fields['prelude_two'].widget.attrs['class'] = 'form-control'
        self.fields['prelude_two'].queryset = queryset
        self.fields['prelude_three'].widget.attrs['class'] = 'form-control'
        self.fields['prelude_three'].queryset = queryset
        self.fields['prelude_four'].widget.attrs['class'] = 'form-control'
        self.fields['prelude_four'].queryset = queryset
        self.fields['prelude_five'].widget.attrs['class'] = 'form-control'
        self.fields['prelude_five'].queryset = queryset
        self.fields['processional'].widget.attrs['class'] = 'form-control'
        self.fields['processional'].queryset = queryset
        self.fields['bridal'].widget.attrs['class'] = 'form-control'
        self.fields['bridal'].queryset = queryset
        self.fields['unity'].widget.attrs['class'] = 'form-control'
        self.fields['unity'].queryset = queryset
        self.fields['communion'].widget.attrs['class'] = 'form-control'
        self.fields['communion'].queryset = queryset
        self.fields['recessional'].widget.attrs['class'] = 'form-control'
        self.fields['recessional'].queryset = queryset
        self.fields['num_grandmothers'].widget.attrs['class'] = 'form-control'
        self.fields['num_mothers'].widget.attrs['class'] = 'form-control'
        self.fields['num_bridesmaids'].widget.attrs['class'] = 'form-control'
        self.fields['num_rings'].widget.attrs['class'] = 'form-control'
        self.fields['num_flowers'].widget.attrs['class'] = 'form-control'
        # prelude_one = forms.ModelChoiceField(queryset=queryset)
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
        # widgets = {
            # 'prelude_one': forms.ChoiceField(attrs={'class':'form-control'}),
            # 'start_time': forms.TimeInput( attrs={'class': 'timepicker'}),
            # 'end_time': forms.TimeInput(attrs={'class': 'timepicker'}),
            # 'performers_required_time': forms.TimeInput(attrs={'class': 'timepicker'}),
            # 'client_email': forms.EmailInput(),
        # }

   