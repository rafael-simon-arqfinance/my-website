from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('page2/', views.page2, name='page2'),
    path('page3/', views.page3, name='page3'),
]
