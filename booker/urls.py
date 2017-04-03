from django.conf.urls import url
# from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^listen/$', views.listen, name='listen'),
    url(r'^bookings/$', views.bookings, name='bookings'),
    url(r'^event/(?P<pk>\d+)/$', views.event_detail, name='event_detail'),
    url(r'^event/(?P<pk>\d+)/success/$', views.event_inquiry_confirm, name='event_inquiry_confirm'),

    url(r'^selections/(?P<pk>\d+)/$', views.selections_detail, name='selections_detail'),
    url(r'^selections/(?P<pk>\d+)/form/$', views.selections_form, name='selections_form'),
    url(r'^send_selections/(?P<pk>\d+)/$', views.send_selections, name='send_selections'),
    url(r'^notify_players/(?P<pk>\d+)/$', views.notify_players, name='notify_players'),

    url(r'^contract/(?P<pk>\d+)/$', views.contract, name='contract'),
    url(r'^contract/(?P<pk>\d+)/balance$', views.request_balance, name='request_balance'),
    url(r'^contract/pdf/(?P<pk>\d+)/$', views.contract_pdf, name='contract_pdf'),
    url(r'^contract/link/(?P<pk>\d+)/$', views.contract_link, name='contract_link'),
    url(r'^payment_success/(?P<pk>\d+)/$', views.payment_success, name='payment_success'),
    url(r'^payment_cancel/(?P<pk>\d+)/$', views.payment_cancel, name='payment_cancel'),

    url(r'^musician/(?P<pk>\d+)/$', views.musician_detail, name='musician_detail'),
    url(r'^upcoming/$', views.upcoming, name='upcoming'),
]
