from django.urls import path
from . import views


urlpatterns = [
    path('', views.BookListView.as_view(), name='BookList'),
    path('author/<slug:author>/', views.BookListView.as_view(), name='BookAuthorList'),
    path('<slug:slug>/', views.BookDetailView.as_view(), name='BookDetail'),
]