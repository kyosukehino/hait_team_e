from django.contrib import admin
from django.urls import path
from .views import mainfunc, hiyoshifunc



urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', mainfunc, name='main'),
    path('hiyoshi/', hiyoshifunc, name='hiyoshi'),
    
]
