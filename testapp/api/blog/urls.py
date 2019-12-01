from django.contrib import admin
from django.urls import path, include

from testapp.api.blog import views

urlpatterns = [
    path('create_blog', views.create_blog),

    path('upload_post_photo', views.upload_post_photo),
    path('create_post', views.create_post),
]
