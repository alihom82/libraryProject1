from collections import defaultdict

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView

from book_module.models import Book, Author


from borrow_module.models import Borrow


# Create your views here.



class BookListView(ListView):
    template_name = 'book_module/book_list.html'
    model = Book
    context_object_name = 'books'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        author = self.kwargs.get('pk')
        if author:
            author_pk = get_object_or_404(Author, pk=author, is_active=True, is_deleted=False)
            queryset = queryset.filter(author=author_pk)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authors = Author.objects.filter(is_active=True, is_deleted=False)
        context['authors'] = authors

        context['current_author_slug'] = self.kwargs.get('author')
        return context



class BookDetailView(DetailView):
    template_name = 'book_module/book_detail.html'
    model = Book
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        author_slug = self.kwargs.get('author')
        if author_slug:
            author = get_object_or_404(Author, url_title=author_slug, is_active=True, is_deleted=False)
            queryset = queryset.filter(author=author)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authors = Author.objects.filter(is_active=True, is_deleted=False)
        context['authors'] = authors
        context['current_author_slug'] = self.kwargs.get('author')
        book = self.get_object()
        user = self.request.user


        context['has_borrowed'] = False

        if user.is_authenticated:
            context['has_borrowed'] = Borrow.objects.filter(
                user=user,
                book=book,
                returned_at__isnull=True
            ).exists()

        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        book_id = request.POST.get("book_id")

        book = get_object_or_404(Book, pk=book_id)


        borrow = Borrow.objects.filter(user=user, book=book, returned_at__isnull=True).first()

        if borrow:

            borrow.returned_at = timezone.now()
            borrow.save()
            return JsonResponse({'success': True, 'message': 'کتاب با موفقیت برگردانده شد'})
        else:
            if book.available_count() == 0:
                return JsonResponse({'success': False, 'message': 'کتاب در حال حاضر موجود نیست'})

        Borrow.objects.create(user=user, book=book)
        borrow.save()
        return JsonResponse({'success': True, 'message': 'کتاب با موفقیت امانت گرفته شد'})