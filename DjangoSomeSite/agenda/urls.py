from django.urls import path
# from django.views.generic import RedirectView

from . import views


app_name = 'agenda'
urlpatterns = [
    path('', views.list_event, name='index'),
    path('history/', views.list_history, name='history'),
    path('event/<int:event_id>', views.new_event, name='new'),
    path('event/submit/', views.submit_event, name='submit'),
    path('event/delete/<int:event_id>', views.delete_event, name='delete'),
    path('api/', views.list_json),
]
