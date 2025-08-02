# orders/views.py

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from book_module.models import Book
from .models import Borrow
from django.utils import timezone

@require_POST
@login_required
def toggle_borrow(request):
    book_id = request.POST.get('book_id')
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'کتاب یافت نشد'})

    # بررسی آیا کاربر کتاب را قبلاً امانت گرفته ولی هنوز برنگردونده؟
    borrow = Borrow.objects.filter(user=request.user, book=book, returned_at__isnull=True).first()

    if borrow:
        # اگر در حال حاضر کتاب دستشه → برگرداندن
        borrow.returned_at = timezone.now()
        borrow.save()
        return JsonResponse({'success': True, 'message': 'کتاب با موفقیت برگردانده شد', 'action': 'returned'})
    else:
        # اگر موجود نباشه
        if not book.available_count:
            return JsonResponse({'success': False, 'message': 'کتاب در حال حاضر موجود نیست'})

        # امانت گرفتن
        Borrow.objects.create(user=request.user, book=book)
        book.available = False
        book.save()
        return JsonResponse({'success': True, 'message': 'کتاب با موفقیت امانت گرفته شد', 'action': 'borrowed'})