from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from book_module.models import Book
from .models import Borrow

@require_POST
@login_required
def toggle_borrow(request):
    book_id = request.POST.get('book_id')
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'کتاب یافت نشد'})

    borrow = Borrow.objects.filter(user=request.user, book=book, returned_at__isnull=True).first()

    if borrow:
        borrow.returned_at = timezone.now()
        borrow.save()
        return JsonResponse({
            'success': True,
            'message': 'کتاب با موفقیت بازگردانده شد',
            'action': 'returned',
            'available_count': book.available_count,
            'button_text': 'امانت گرفتن'
        })
    else:
        if book.available_count <= 0:
            return JsonResponse({
                'success': False,
                'message': 'کتاب در حال حاضر موجود نیست',
                'available_count': book.available_count
            })

        Borrow.objects.create(user=request.user, book=book)
        return JsonResponse({
            'success': True,
            'message': 'کتاب با موفقیت امانت گرفته شد',
            'action': 'borrowed',
            'available_count': book.available_count,
            'button_text': 'برگرداندن'
        })