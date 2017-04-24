from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string, get_template
from .forms import EventForm, SelectionsForm
from .models import Event, Musician, Ensemble, Song, Selection
# from schedule import *
from schedule.models import Calendar
from schedule.models import Event as S_Event
from django.core.mail import EmailMessage, send_mail

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from weasyprint import HTML
from oreadstrings.constants import paypal_reciever_email, base_url, paypal_logo_url, os_admin_email, image_url_base, os_admin_email_to

from django.core.urlresolvers import reverse
from paypal.standard.forms import PayPalPaymentsForm
# from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
import logging
from datetime import timedelta, time
from datetime import datetime as dt
from django.utils import timezone
logger = logging.getLogger('testlogger')


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    pk = ipn_obj.invoice
    event = get_object_or_404(Event, pk=pk)
    if ipn_obj.payment_status == 'Completed':
        logger.info('Paypal IPN object received')
        if ipn_obj.receiver_email != paypal_reciever_email:
            logger.error('PayPal Error: incorrect reciever email!')
            return
        if ipn_obj.payment_gross != event.deposit:
            logger.error('PayPal Error: incorrect deposit amount!')
            return
        if ipn_obj.custom == "Deposit Payment":
            event.deposit_recieved = True
            event.save()
            logger.info('Paypal Success: deposit payment recieved, status updated')
    else:
        logger.error('Paypal Failure: IPN object status is not complete')


valid_ipn_received.connect(show_me_the_money)


def show_me_the_error(sender, **kwargs):
    logger.error('Paypal Error: invalid IPN received')
    logger.error(sender)


invalid_ipn_received.connect(show_me_the_error)


def view_that_asks_for_money(request, pk, custom):
    custom = custom
    event = get_object_or_404(Event, pk=pk)
    item_name = 'Deposit for {0} on {1}'.format(event.event_type, event.event_date)
    cancel_return = '{0}/payment_cancel/{1}'.format(base_url, event.pk)
    return_url = '{0}/payment_success/{1}'.format(base_url, event.pk)
    paypal_dict = {
        "business": paypal_reciever_email,
        "image_url": paypal_logo_url,
        "amount": event.deposit,
        "item_name": item_name,
        "invoice": event.pk,
        "button_subtype": "services",
        "notify_url": base_url + reverse('paypal-ipn'),
        "return_url": return_url,
        "cancel_return": cancel_return,
        "custom": custom,
        "no_shipping": 1,
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form, 'event': event}
    return context


def request_balance(request, pk):
    event = get_object_or_404(Event, pk=pk)
    custom = 'Balance Payment'
    context = view_that_asks_for_money(request, pk, custom)
    balance = event.fee - event.deposit
    html = 'Welcome back, {0}.  You have a balance of ${1} for your'
    ' upcoming {2} on {3}.  Please click the Paypal button below to '
    'pay the remainder of your fee.'.format(event.client_name, balance, event.event_type, event.event_date)
    messages.info(request, html)
    return render(request, 'booker/summary.html', context)


def add_to_calendar(pk):
    event = get_object_or_404(Event, pk=pk)
    title = '{0} - {1}'.format(event.client_name, event.event_type)
    description = '<a href="{0}/event/{1}"</a>'.format(base_url, event.pk)
    start_time = time(19, 0, 0)
    # current_tz = timezone.get_current_timezone()

    def get_start_time():
        if event.start_time is None:
            start_time = time(19, 0, 0)
        else:
            start_time = event.start_time
        return start_time
    start_time = get_start_time()
    start = dt.combine(event.event_date, start_time)
    start = timezone.make_aware(start, timezone.get_current_timezone())
    end = start + timedelta(hours=4)
    occurrence = S_Event(start=start, end=end, title=title, description=description)
    occurrence.save()
    cal = Calendar.objects.get(pk=1)
    cal.events.add(occurrence)


def contract(request, pk):
    add_to_calendar(pk)
    custom = 'Deposit Payment'
    context = view_that_asks_for_money(request, pk, custom)
    return render(request, 'booker/contract.html', context)


def payment_success(request, pk):
    event = get_object_or_404(Event, pk=pk)
    balance = event.fee - event.deposit
    # balance_duedate = event.balance_duedate
    if event.balance_duedate is None:
        balance_duedate = event.event_date
    else:
        balance_duedate = event.balance_duedate
    html = 'Thank You {0}, your deposit of ${1} has been received. '
    'Your booking on {2} is now confirmed.  The balance of your fee,'
    ' ${3} will be due on {4}.'.format(event.client_name, event.deposit, event.event_date, balance, balance_duedate)
    messages.success(request, html)
    return render(request, 'booker/summary.html', {'event': event})


def payment_cancel(request, pk):
    # event = get_object_or_404(Event, pk=pk)
    custom = 'Deposit Payment'
    html = 'You have cancelled your Paypal deposit process.  '
    'Click the link below to try again or contact us at {0} with'
    ' any questions. Your booking is not confirmed until a deposit is received.'.format(os_admin_email)
    messages.warning(request, html, )
    context = view_that_asks_for_money(request, pk, custom)
    # return render(request, 'booker/payment_cancel.html', {'event': event})
    return render(request, 'booker/contract.html', context)


def html_email(to, subject, context):
    context['url_link'] = image_url_base
    message = get_template('email/os-email-template.html').render(Context(context))
    msg = EmailMessage(subject, message, os_admin_email, to)
    msg.content_subtype = 'html'
    msg.send()


def contract_pdf(request, pk):
    event = get_object_or_404(Event, pk=pk)
    html_string = render_to_string('booker/contract_pdf.html', {'event': event})
    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf')
    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = "attachment; filename=Oread Strings Contract"
        return response
    return response


# Not finished - Start
def get_musicians(pk):
    event = get_object_or_404(Event, pk=pk)
    musicians = []
    m1 = event.musician_one.name
    m2 = event.musician_two.name
    m3 = event.musician_three.name
    musicians = [m1, m2, m3]
    print(musicians)
    return musicians


def upcoming(request):
    events = Event.objects.all()
    musicians = get_musicians(12)
    print('test', musicians)
    # print(events)
    context = {'events': events, 'musicians': musicians}
    return render(request, 'booker/upcoming.html', context)
# Not finished - End


def send_selections(request, pk):
    event = get_object_or_404(Event, pk=pk)
    subject = 'Your Booking with the Oread Strings - Music Selections Form'
    to = [event.client_email]
    message = 'The Oread Strings have sent you a link to help plan your upcoming event. Please click below to fill out the musicial selection form. Thanks and have a lovely day.'
    link = '{0}/selections/{1}/form'.format(base_url, event.pk)
    context = {
        'name': event.client_name,
        'message': message,
        'link': link,
    }
    html_email(to, subject, context)
    html = "You have succesfully forwarded the selection form to %s" % event.client_name
    messages.success(request, html)
    return render(request, 'booker/base.html')


def selections_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    html = 'Thank You {0}, you have successfully submitted your musical selections for your event on {1}'.format(event.client_name, event.event_date)
    messages.success(request, html)
    return render(request, 'booker/selections_detail.html', {'event': event})


def notifyadmin_selections(request, pk):
    subject = 'Client submitted Selections at Oreadstrings.com'
    to = [os_admin_email_to]
    event = get_object_or_404(Event, pk=pk)
    message = '{0} has submitted a new list of selections for their event through the Oread Strings form. Please click here the link to view the selections.  Thanks and have a lovely day.'.format(event.client_name)
    link = '{0}/selections/{1}'.format(base_url, event.pk)
    context = {
        'name': 'Ellen',
        'message': message,
        'link': link,
    }
    html_email(to, subject, context)
    return HttpResponse('notifyadmin_selections')


def selections_form(request, pk):
    event = get_object_or_404(Event, pk=pk)
    ensemble_type = event.ensemble_type
    selections = Selection.objects.filter(arrangement=ensemble_type)
    print(selections)
    form = SelectionsForm(request.POST, instance=event)
    if request.method == 'POST':
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            notifyadmin_selections(request, pk=event.pk)
            return redirect('selections_detail', pk=event.pk)
    else:
        form = SelectionsForm(instance=event)
    context = {'form': form, 'event': event, 'selections': selections}
    return render(request, 'booker/selections_form.html', context)


def notify_players(request, pk):
    event = get_object_or_404(Event, pk=pk)
    musicians = []

    def is_musician_assigned(musician_instance):
        musician = musician_instance
        if musician is not None:
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
        if j[0] is None:
            print('this:', j[0])
        else:
            musicians_contacts.append(j)
    for j, k in musicians_contacts:
        m_names.append(j)
        m_emails.append(k)
    m_names_str = ('%s' % ', '.join(map(str, m_names)))
    to = m_emails
    # from_email = os_admin_email
    subject = 'Oread Strings - Event Details'
    link = '{0}/event/{1}'.format(base_url, event.pk)
    message = 'You have been confirmed for an Oread Strings {0} booking on {1}.'
    ' Please click the link for the full details.'.format(event.event_type, event.event_date)
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
    link = '{0}/contract/{1}'.format(base_url, event.pk)
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


def notifyadmin(request, pk):
    event = get_object_or_404(Event, pk=pk)
    subject = 'New Booking Inquiry at Oreadstrings.com'
    to = [os_admin_email]
    message = 'You have a new booking inquiry from {0} for an event on {1}. Please click the link to see the details'.format(event.client_name, event.event_date)
    link = '{0}/admin/booker/event/{1}/change/'.format(base_url, event.pk)
    context = {
        'name': 'Ellen',
        'message': message,
        'link': link,
    }
    html_email(to, subject, context)
    return HttpResponse('notifyadmin')


def index(request):
    musicians = Musician.objects.all()
    ensembles = Ensemble.objects.all()
    context = {'musicians': musicians, 'ensembles': ensembles}
    return render(request, 'booker/index.html', context)


def listen(request):
    songs = Song.objects.all().order_by('ensemble')
    context = {'songs': songs, }
    return render(request, 'booker/listen.html', context)


def bookings(request):
    if request.method == 'POST':
        form = EventForm(request.POST or None)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            print('valid')
#            print form.cleaned_data.get('client')
            event.save()
            notifyadmin(request, pk=event.pk)
            # messages.success(request, 'Your booking was updated successfully!')  # <-
            return redirect('event_inquiry_confirm', pk=event.pk)
        else:
            print('error')
            # messages.warning(request, 'Please correct the error below.', extra_tags='alert')  # <-
    else:
        form = EventForm()
    context = {'form': form, }
    return render(request, 'booker/event_form.html', context)


def musician_detail(request, pk):
    musician = get_object_or_404(Musician, pk=pk)
    return render(request, 'booker/musician_detail.html', {'musician': musician})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'booker/summary.html', {'event': event})


def event_inquiry_confirm(request, pk):
    event = get_object_or_404(Event, pk=pk)
    html = "Thank you {0}! Your booking inquiry has been recieved. Your custom quote will be emailed to you at {1} within 3 business days. Have a great day!".format(event.client_name, event.client_email)
    messages.success(request, html)
    return render(request, 'booker/summary.html', {'event': event})
