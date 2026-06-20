#ACCOUNTS URLS

from django.urls import path
from . import views

app_name='accounts'

urlpatterns=[
    path('signup',views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout',views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/add_message', views.add_message, name='add_message'),
    path('dashboard/my_messages/<int:lid>/', views.letter_actions, name='letter_actions'),    
    path('dashboard/my_messages', views.my_messages, name='my_messages'),
    path('dashboard/edit_message/<int:lid>/', views.edit_message, name='edit_message'),
    path('dashboard/send_message/<int:lid>/', views.send_message, name='send_message'),
    path('dashboard/contacts', views.contacts, name='contacts'),
    path('dashboard/account_settings', views.account_settings, name='account_settings'),
    path('verify-email/<str:token>/', views.receive_confirm_email, name='receive_confirm_email'),
    path('reset_password/<str:token>/', views.receive_reset_password, name='receive_reset_password'),
    path('forgot_password',views.forgot_password, name='forgot_password')
]