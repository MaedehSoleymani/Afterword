#BLOG URLS

from django.urls import path
from blog import views

app_name='blog'

urlpatterns=[
    path('',views.home,name='home'),
    path('post/<int:pid>/',views.post_detail, name='post_detail'),
    path('author_dashboard',views.author_dashboard, name='author_dashboard'),
    path('author_dashboard/post/<int:pid>/',views.post_actions, name='post_actions'),
    path('author_dashboard/edit_post/<int:pid>/', views.edit_post, name='edit_post'),
    path('author_dashboard/write_post',views.write_post, name='write_post')
]