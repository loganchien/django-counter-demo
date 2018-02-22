from django.urls import include, path

from . import views

urlpatterns = [
    path('counter1', views.counter1, name='counter1'),
    path('counter2', views.counter2, name='counter2'),
    path('counter3', views.counter3, name='counter3'),
    path('counter4', views.counter4, name='counter4'),
]
