# orders/urls.py

from django.urls import path
from .views import toggle_borrow

urlpatterns = [
    path('ajax/borrow-toggle/', toggle_borrow, name='borrow_toggle'),
]