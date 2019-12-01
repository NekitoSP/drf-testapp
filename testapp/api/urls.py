from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('blog/', include('testapp.api.blog.urls')),
]
