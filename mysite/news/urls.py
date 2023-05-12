from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('triangulate/', triangulate, name='triangulate'),
    path('triangulate/inter/', inter, name='inter'),
    path('triangulate/vallin/', vallin, name='vallin'),

]