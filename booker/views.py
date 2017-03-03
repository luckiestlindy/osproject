from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context
from django.template.loader import render_to_string, get_template
from .forms import EventForm, SelectionForm
from .models import Event, Musician, Ensemble, Song, SelectionList
from django.core.mail import send_mail, EmailMessage
from reportlab.pdfgen import canvas

#def drip(request, pk):
#    event = get_object_or_404(Event, pk=pk)
#    return render(request, 'booker/emails/drip.html', {'event':event})
#
#def email_one(request):
#    subject = 'Testing an HTML email'
#    to = ['brentlind@mac.com',]
#    from_email = 'brentlind@gmail.com'
#    ctx = {
#        'user': 'steve',
#        'purchase': 'books',
#    }
#    message = get_template('booker/emails/drip.html').render(Context(ctx))
#    msg = EmailMessage(subject, message, to=to, from_email=from_email)
#    msg.content_subtype = 'html'
#    msg.send()
#    return HttpResponse ('it worked')
    
def send_selections(request, pk):
    event = get_object_or_404(Event, pk=pk)
    subject = 'Your Booking with the Oread Strings - Music Selections Form'
    to = [event.client_email]
    from_email = 'oreadstrings@gmail.com'
    var = {
        'client_name': event.client_name,
        'link': event.get_absolute_url(),
    }
    message = render_to_string('email/send_selections.txt', var)
    EmailMessage(subject, message,to=to, from_email=from_email).send()
    html = "You have succesfully sent the selection form to the client" 
    return render(request, 'booker/confirm.html', {'html': html} )

def selectionlist_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    selectionlist = get_object_or_404(SelectionList, pk=pk)
    return render(request, 'booker/selectionlist_detail.html', {'selectionlist': selectionlist, 'event':event})

def notifyadmin_selections(request, pk):
    subject = 'Client submitted Selections at Oreadstrings.com'
    to = ['oreadstrings@gmail.com']
    from_email = 'test@example.com'
    event = get_object_or_404(Event, pk=pk)
    var = {
        'client_name': event.client_name,
        'link': event.get_absolute_url(),
    }
    message = render_to_string('email/notifyadmin_selections.txt', var)
    EmailMessage(subject, message,to=to, from_email=from_email).send()
    return HttpResponse('notifyadmin_selections')

def selections(request,pk):
    event = get_object_or_404(Event, pk=pk)
    selectionlist = SelectionList.objects.get(pk=pk)
    form = SelectionForm(request.POST, instance=selectionlist)
    if request.method == 'POST':
        if form.is_valid():
            selections = form.save(commit=False)
            selections.author = request.user
            selections.save()
            notifyadmin_selections(request, pk=event.pk)
            return redirect ('selectionlist_detail', pk=event.pk)
    else:
        form = SelectionForm(instance=selectionlist)
    context = {'form':form, 'event':event}
    return render(request, 'booker/selection_form.html', context)

def notify_players(request, pk):
    event = get_object_or_404(Event, pk=pk)
    subject = 'Oread Strings - Event Details'
    musicians =[]
    def is_musician_assigned(musician_instance):
        var = musician_instance
        if var != None:
            email = var.email
        else:
            email = None
        return email 
    musicians = [
        is_musician_assigned(event.musician_one), 
        is_musician_assigned(event.musician_two),
        is_musician_assigned(event.musician_three),
        is_musician_assigned(event.musician_four),
        is_musician_assigned(event.musician_five),
    ]
    print (musicians)
    to = musicians
    from_email = 'test@example.com'
    var = {
        'event_date': event.event_date,
        'venue': event.venue_name,
    }
    message = render_to_string('email/notifyplayers.txt', var)
    EmailMessage(subject, message,to=to, from_email=from_email).send()
    date = event.event_date
    html = "You have succesfully notified your musicians of the event booking on %s" % date
    return render(request, 'booker/confirm.html', {'html': html} )
    
def contract_link(request, pk):
    event = get_object_or_404(Event, pk=pk)
    subject = 'Your Quote has arrived from the Oread Strings'
    to = [event.client_email]
    from_email = 'test@example.com'
    var = {
        'personal_message': event.quote_message,
        'client_name': event.client_name,
        'link':  event.pk
    }
    message = render_to_string('email/notifyclient.txt', var)
    EmailMessage(subject, message,to=to, from_email=from_email).send()
    fee = event.fee
    html = "You have succesfully forwarded your quote of %s to the client" % fee
    return render(request, 'booker/confirm.html', {'html': html} )

    
def contract_pdf(request, pk):
    event = get_object_or_404(Event, pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "attachment; filename=filename.pdf"
    p = canvas.Canvas(response)
    p.drawString(100,100, 'Hello World')
    p.showPage()
    p.save()
    return response

def contract(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'booker/contract.html', {'event': event})

def notifyadmin(request, pk):
    subject = 'New Booking Inquiry at Oreadstrings.com'
    to = ['oreadstrings@gmail.com']
    from_email = 'test@example.com'
    event = get_object_or_404(Event, pk=pk)
    var = {
        'client_name': event.client_name,
        'link': event.get_absolute_url(),
    }
    message = render_to_string('email/notifyadmin.txt', var)
    EmailMessage(subject, message,to=to, from_email=from_email).send()
    return HttpResponse('notifyadmin')


def index(request):
   return render(request, 'booker/index.html')

def ensembles(request):
    extra_context = {}
    ensembles = Ensemble.objects.all()
    extra_context['ensembles'] = ensembles
    return render(request, 'booker/ensembles.html', extra_context)

def musicians(request):
    extra_context = {}
    musicians = Musician.objects.all()
    extra_context['musicians'] = musicians
    return render(request, 'booker/musicians.html',extra_context )

def listen(request):
    extra_context = {}
    songs = Song.objects.all()
    extra_context['songs'] = songs
    return render(request, 'booker/listen.html', extra_context)

def contact(request):
    return render(request, 'booker/contact.html')

def bookings(request):
    if request.method == 'POST':
        form = EventForm(request.POST or None)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
#            print form.cleaned_data.get('client')
            event.save()
#            send_mail('test subject', 'hhereis the message', 'brentlind@gmail.com', ['brentlind@mac.com'], fail_silently=False,)
            notifyadmin(request, pk=event.pk)
            return redirect ('event_detail', pk=event.pk)
    else:
        form=EventForm()    
    context = {'form': form,}
    return render(request, 'booker/event_form.html', context)

def musician_detail(request, pk):
    musician = get_object_or_404(Musician, pk=pk)
    return render(request, 'booker/musician_detail.html', {'musician': musician})
                  
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'booker/success.html', {'event': event})
