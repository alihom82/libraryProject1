
from django.db import models
from django.conf import settings
from book_module.models import Book
from django.utils import timezone

class Borrow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrows')
    borrowed_at = models.DateTimeField(default=timezone.now)
    returned_at = models.DateTimeField(null=True, blank=True)

    def is_returned(self):
        return self.returned_at is not None

    def str(self):
        return f"{self.book.title} - {self.user.username} ({'برگشته' if self.is_returned() else 'امانت'})"