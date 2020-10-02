from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('log-in', views.LogIn, name='log_in'),
    path('log-out', views.LogOut, name='log_out'),
    path('sign-up', views.signup, name='sign_up'),
    path('rules', views.rules, name='rules'),
    path('myProfile', views.myProfile, name='myProfile'),
    path('myMatches', views.myMatches, name='myMatches'),
    path('play', views.play, name='play'),
    path('validate-room-name/<str:room_name>/', views.validate_room_name, name='validate-room-name'),
    path('<str:room_name>/', views.room, name='room'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
