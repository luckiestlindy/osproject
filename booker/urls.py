from django.conf.urls import url
#from booker.views import EventCreate, EventUpdate, EventDelete
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ensembles/$', views.ensembles, name='ensembles'),
    url(r'^musicians/$', views.musicians, name='musicians'),
    url(r'^listen/$', views.listen, name='listen'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^bookings/$', views.bookings, name='bookings'),
#    url(r'^bookings/success/$', views.success, name='success'),
#    url(r'^events/$', views.event_list, name='event_list'),
    url(r'^event/(?P<pk>\d+)/$', views.event_detail, name='event_detail'),
    
#    url(r'^event/(?P<pk>\d+)/edit/$', views.event_edit, name='event-edit'),
#    url(r'^events/new/$', views.event_new, name='event_new'),
    
#    url(r'event/add/$', EventCreate.as_view(), name='event-add'),
#    url(r'event/(?P<pk>[0-9]+)/$', EventUpdate.as_view(), name='event-update'),
#    url(r'event/(?P<pk>[0-9]+)/delete/$', EventDelete.as_view(), name='event-delete'),
    # ex: /polls/5/
#    url(r'^(?P<client_id>[0-9]+)/client/$', views.detail, name='detail'),
    # ex: /polls/5/results/
#    url(r'^(?P<client_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
#    url(r'^(?P<client_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
