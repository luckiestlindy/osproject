from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
# from django_pdfkit import PDFView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^ensembles/$', views.ensembles, name='ensembles'),
    # url(r'^musicians/$', views.musicians, name='musicians'),
    url(r'^listen/$', views.listen, name='listen'),
    # url(r'^contact/$', views.contact, name='contact'),
    url(r'^bookings/$', views.bookings, name='bookings'),
    url(r'^event/(?P<pk>\d+)/$', views.event_detail, name='event_detail'),
    url(r'^event/(?P<pk>\d+)/success/$', views.event_inquiry_confirm, name='event_inquiry_confirm'),
    
    url(r'^selections/(?P<pk>\d+)/$', views.selections_detail, name='selections_detail'),
    url(r'^selections/(?P<pk>\d+)/form/$', views.selections_form, name='selections_form'),
    
    url(r'^send_selections/(?P<pk>\d+)/$', views.send_selections, name='send_selections'), 

    url(r'^contract/(?P<pk>\d+)/$', views.contract, name='contract'),
    url(r'^notify_players/(?P<pk>\d+)/$', views.notify_players, name='notify_players'),
    url(r'^contract/pdf/(?P<pk>\d+)/$', views.contract_pdf, name='contract_pdf'),
    url(r'^contract/link/(?P<pk>\d+)/$', views.contract_link, name='contract_link'),
    url(r'^musician/(?P<pk>\d+)/$', views.musician_detail, name='musician_detail'),
    url(r'^upcoming/$', views.upcoming, name='upcoming'),
    # url(r'^cashmoney/(?P<pk>\d+)/$', views.view_that_asks_for_money, name='view_that_asks_for_money'),
    
    url(r'^payment_success/(?P<pk>\d+)/$', views.payment_success, name='payment_success'),
    url(r'^payment_cancel/(?P<pk>\d+)/$', views.payment_cancel, name='payment_cancel'),
    # url(r'^pdf_generation/(?P<pk>\d+)/$', views.pdf_generation, name='pdf_generations'),
    # url(r'^template/$', views.template, name='template'),
    # url(r'^my-pdf/$', PDFView.as_view(template_name='my-pdf.html'), name='my-pdf'),
    # url(r'^books/$', views.books_plain_old_view, name='books_plain_old_view'),

#    url(r'^drip/(?P<pk>\d+)/$', views.drip, name='drip'),
#    url(r'^email_one$', views.email_one, name='email_one'),
    # url(r'^payment/$', views.email_one, name='payment'),
] 
