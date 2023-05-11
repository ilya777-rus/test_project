from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('triangulate/', triangulate, name='triangulate'),
    path('triangulate/inter/', inter, name='inter'),

]