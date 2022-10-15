from django.urls import path

from . import views


app_name = 'login'
urlpatterns = [
    path('', views.login_user, name='index'),
    path('submit/', views.submit_login, name='submit'),
    path('logout/', views.logout_user, name='logout')
]
