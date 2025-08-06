from django.urls import path
from . import views


urlpatterns = [
    path('', views.BookListView.as_view(), name='BookList'),
    path('author/<int:pk>/', views.BookListView.as_view(), name='BookAuthorList'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='BookDetail'),
]