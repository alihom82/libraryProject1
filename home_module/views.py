from django.shortcuts import render
from django.views.generic import TemplateView

from book_module.models import Book
from utils.convertors import group_list


class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_books = Book.objects.all().order_by('-release_date')[:4]
        context['latest_books_group'] = group_list(latest_books)
        context['latest_books'] = latest_books
        print(context['latest_books_group'])
        print(context['latest_books'])
        return context