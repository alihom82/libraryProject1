# orders/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('borrow-toggle/',views.toggle_borrow, name='borrow_toggle'),
]