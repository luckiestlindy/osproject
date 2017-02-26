from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from .forms import EventForm
from .models import Event, Musician, Ensemble, Song
from django.core.mail import send_mail, EmailMessage

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
#def success (request):
#    return render(request, 'booker/success.html')

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'booker/success.html', {'event': event})
#def event_edit(request, pk):
#    event = get_object_or_404(Post, pk=pk)
#    if request.method == "POST":
#        form = EventForm(request.POST, instance=event)
#        if form.is_valid():
#            event = form.save(commit=False)
#            event.author = request.user
#            event.published_date = timezone.now()
#            event.save()
#            return redirect('event_detail', pk=post.pk)
#    else:
#        form = EventForm(instance=event)
#    return render(request, 'booker/event_edit.html', {'form': form})

#def bookings(request):
#    form = EventForm(request.POST or None)
#    if form.is_valid():
#        instance = form.save(commit=False)
#        print form.cleaned_data.get('client')
#        instance.save()
#        
#    #    if request.method =='POST':
##        print request.POST.get("ensemble_type")
#    context = {'form': form,}
#    return render(request, 'booker/event_form.html', context)
