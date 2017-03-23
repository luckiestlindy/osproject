from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string, get_template
from .forms import EventForm, SelectionsForm
from .models import Event, Musician, Ensemble, Song, Selection
from django.core.mail import send_mail, EmailMessage

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from weasyprint import HTML
from oreadstrings.constants import *


from django.core.urlresolvers import reverse
# from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
import logging

# Get an instance of a logger
logger = logging.getLogger(os.heroku)

# Create your models here.
def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the business field request. (The user could tamper
        # with those fields on payment form before send it to PayPal)
        if ipn_obj.receiver_email != PAYPAL_RECIEVER_EMAIL:
            print('email wrong')
            # logger.error('email wrong')
            # Not a valid payment
            return
        # ALSO: for the same reason, you need to check the amount
        # received etc. are all what you expect.

        # Undertake some action depending upon `ipn_obj`.
        # if ipn_obj.custom == "Upgrade all users!":
            # Users.objects.update(paid=True)
    else:
        print('this happened')
        # logger.error('email right')
        # pass

valid_ipn_received.connect(show_me_the_money)



def view_that_asks_for_money(request, pk):
    event = get_object_or_404(Event, pk = pk)
    item_name = 'Deposit for {0} on {1}'.format(event.event_type, event.event_date)
    cancel_return = 'https://oreadstrings.herokuapp.com/payment_cancel/{0}'.format(event.pk)
    return_url = 'https://oreadstrings.herokuapp.com/payment_success/{0}'.format(event.pk)
    paypal_dict = {
        "business": "oreadstrings@gmail.com",
        "image_url": "https://s3.us-east-2.amazonaws.com/oreadstrings-assets/images/fullcolor_pp.jpg",
        "amount": event.deposit,
        "item_name": item_name,
        "invoice": event.pk,
        "button_subtype":"services",
        "notify_url": "https://oreadstrings.herokuapp.com" + reverse('paypal-ipn'),
        "return_url": return_url,
        "cancel_return": cancel_return,
        # "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
    }
    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form, 'event':event}
    return context
    # return render(request, "booker/contract.html", context)


def contract(request, pk):
    context = view_that_asks_for_money(request, pk)
    # event = get_object_or_404(Event, pk=pk)
    return render(request, 'booker/contract.html', context)

def payment_success(request, pk):
    event = get_object_or_404(Event, pk = pk)
    html = 'Thank You {0}, your deposit of ${1} has been received. Your booking on {2} is now confirmed'.format(event.client_name, event.deposit, event.event_date,)
    messages.success(request, html)
    return render(request, 'booker/success.html', {'event': event})

def payment_cancel(request, pk):
    event = get_object_or_404(Event, pk = pk)
    html = 'You have cancelled your Paypal deposit process.  Click the link below to try again or contact us at {0} with any questions. Your booking is not confirmed until a deposit is received.'.format(os_admin_email)
    messages.warning(request, html, )
    context = view_that_asks_for_money(request, pk)
    # return render(request, 'booker/payment_cancel.html', {'event': event})
    return render(request, 'booker/contract.html', context)


def html_email(to, subject, context):
    message = get_template('email/os-email-template.html').render(Context(context))
    msg = EmailMessage(subject, message, os_admin_email, to )
    msg.content_subtype = 'html'
    msg.send()
    
def contract_pdf(request, pk):
    event = get_object_or_404(Event, pk=pk)
    html_string = render_to_string('booker/pdftest.html', {'event':event})
    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');
    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = "attachment; filename=Oread Strings Contract"
        return response
    return response


# Not finished - Start
def get_musicians(pk):
    event = get_object_or_404(Event, pk=pk)
    musicians = {}
    m1 = event.musician_one.name
    m2 = event.musician_two.name
    m3 = event.musician_three.name
    musicians = [m1,m2, m3]
    print(musicians)
    return musicians

def upcoming(request):
    events = Event.objects.all()
    musicians = get_musicians(12)
    print('test', musicians)
    # print(events)
    context = {'events':events, 'musicians':musicians}
    return render(request, 'booker/upcoming.html', context)
# Not finished - End


def send_selections(request, pk):
    event = get_object_or_404(Event, pk=pk)
    subject = 'Your Booking with the Oread Strings - Music Selections Form'
    to = [event.client_email]
    from_email = 'oreadstrings@gmail.com'
    context = {
        'client_name': event.client_name,
        'link': event.get_absolute_url(),
    }
    message = render_to_string('email/send_selections.txt', context)
    EmailMessage(subject, message,to=to, from_email=from_email).send()
    html = "You have succesfully forwarded the selection form to %s" % event.client_name
    messages.success(request, html)
    return render(request, 'booker/base.html')

def selections_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    html = 'Thank You {0}, you have successfully submitted your musical selections for your event on {1}'.format(event.client_name, event.event_date)
    messages.success(request, html)
    return render(request, 'booker/selections_detail.html', {'event':event})

# Need to test email
def notifyadmin_selections(request, pk):
    subject = 'Client submitted Selections at Oreadstrings.com'
    to = ['oreadstrings@gmail.com']
    # from_email = 'test@example.com'
    event = get_object_or_404(Event, pk=pk)
    # var = {
    #     'client_name': event.client_name,
    #     'link': event.get_absolute_url(),
    # }
    message = '{0} has submitted a new list of selections for their event through the Oread Strings form.  Please click here the link to view the selections.  Thanks and have a lovely day.'.format(event.client_name)
    link = 'http://oreadstrings.com/selections/{0}'.format(event.pk)
    context = {
        'name': 'Ellen',
        'message': message, 
        'link': link,
    }
    html_email(to, subject, context)
    # message = render_to_string('email/notifyadmin_selections.txt', var)
    # EmailMessage(subject, message,to=to, from_email=from_email).send()
    return HttpResponse('notifyadmin_selections')

def selections_form(request,pk):
    event = get_object_or_404(Event, pk=pk)
    ensemble_type = event.ensemble_type
    selections = Selection.objects.filter(arrangement = ensemble_type)
    print (selections)
    form = SelectionsForm(request.POST, instance=event)
    if request.method == 'POST':
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            notifyadmin_selections(request, pk=event.pk)
            return redirect ('selections_detail', pk=event.pk)
    else:
        form = SelectionsForm(instance=event)
    context = {'form':form, 'event':event, 'selections':selections}
    return render(request, 'booker/selections_form.html', context)

def notify_players(request, pk):
    event = get_object_or_404(Event, pk=pk)
    musicians =[]
    def is_musician_assigned(musician_instance):
        musician = musician_instance
        if musician != None:
            email = musician.email
            name = musician.name
        else:
            email = None
            name = None
        return name, email
    musicians = [
        is_musician_assigned(event.musician_one), 
        is_musician_assigned(event.musician_two),
        is_musician_assigned(event.musician_three),
        is_musician_assigned(event.musician_four),
        is_musician_assigned(event.musician_five),
    ]
    musicians_contacts = []
    m_emails = []
    m_names = []
    for j in musicians:
        if j[0] == None:
            print('this:',j[0])
        else:
            musicians_contacts.append(j)
    for j,k in musicians_contacts:
        m_names.append(j)
        m_emails.append(k)
    m_names_str = ('%s' % ', '.join(map(str, m_names)))
    to = m_emails
    from_email = os_admin_email
    subject = 'Oread Strings - Event Details'
    link = 'http://oreadstrings.com/event/{0}'.format(event.pk) 
    message = 'You have been confirmed for an Oread Strings {0} booking on {1}. Please click the link for the full details.'.format(event.event_type, event.event_date)
    context = {
        'name': m_names_str,
        'message': message,
        'link': link,
    }
    html_email(to, subject, context)
    date = event.event_date
    html = "You have succesfully notified your musicians of the event booking on {0}".format(date)
    messages.success(request, html)
    return render(request, 'booker/base.html')


    
def contract_link(request, pk):
    event = get_object_or_404(Event, pk=pk)
    subject = 'Your Quote has arrived from the Oread Strings'
    to = [event.client_email]
    link = 'http://www.oreadstrings.com/contract/{0}'.format(event.pk)
    message = '{0}  Please click the link below to view your custom quote.'.format(event.quote_message)
    context = {
        'name': event.client_name, 
        'message': message,
        'link': link,
    }
    html_email(to, subject, context)
    client = event.client_name
    html = "You have succesfully forwarded your quote to the client {0}".format(client)
    messages.success(request, html)
    return render(request, 'booker/base.html')

    

# def contract(request, pk):
#     event = get_object_or_404(Event, pk=pk)
#     return render(request, 'booker/contract.html', {'event': event})

def notifyadmin(request, pk):
    event = get_object_or_404(Event, pk=pk)
    subject = 'New Booking Inquiry at Oreadstrings.com'
    to = [os_admin_email]
    message = 'You have a new booking inquiry from {0} for an event on {1}. Please click the link to see the details'.format(event.client_name, event.event_date)
    context = {
        'name': 'Ellen',
        'message': message,
        'link': event.get_absolute_url(),
    }
    html_email(to, subject, context)
    return HttpResponse('notifyadmin')


def index(request):
   musicians = Musician.objects.all()
   ensembles = Ensemble.objects.all()
   context = {'musicians': musicians, 'ensembles':ensembles}
   return render(request, 'booker/index.html', context)

def listen(request):
    extra_context = {}
    songs = Song.objects.all()
    extra_context['songs'] = songs
    return render(request, 'booker/listen.html', extra_context)

def bookings(request):
    if request.method == 'POST':
        form = EventForm(request.POST or None)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            print('valid')
#            print form.cleaned_data.get('client')
            event.save()
#            send_mail('test subject', 'hhereis the message', 'brentlind@gmail.com', ['brentlind@mac.com'], fail_silently=False,)
            notifyadmin(request, pk=event.pk)
            # messages.success(request, 'Your booking was updated successfully!')  # <-
            return redirect ('event_detail', pk=event.pk)
        else:
            print('error')
            # messages.warning(request, 'Please correct the error below.', extra_tags='alert')  # <-
    else:
        form=EventForm()    
    context = {'form': form,}
    return render(request, 'booker/event_form.html', context)

def musician_detail(request, pk):
    musician = get_object_or_404(Musician, pk=pk)
    return render(request, 'booker/musician_detail.html', {'musician': musician})
                  
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    html = "Thank you {0}! Your booking inquiry has been recieved. Your custom quote will be emailed to you at {1} within 3 business days.  Have a great day!".format(event.client_name, event.client_email)
    messages.success(request, html)
    return render(request, 'booker/success.html', {'event': event})
