#BLOG URLS

from django.urls import path
from blog import views

app_name='blog'

urlpatterns=[
    path('',views.home,name='home'),
    path('my_posts',views.my_posts, name='my_posts'),
    path('post_detail<int:pid>/',views.post_detail, name='post_detail'),
    path('post/<int:pid>/',views.post_actions, name='post_actions'),
    path('edit_post/<int:pid>/', views.edit_post, name='edit_post'),
    path('write_post',views.write_post, name='write_post')
]