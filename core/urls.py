from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('page2/', views.page2, name='page2'),
    path('page3/', views.page3, name='page3'),
    path('api/history/', views.api_history, name='api_history'),
    path('api/prices/', views.api_prices, name='api_prices'),
]
