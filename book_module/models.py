
from django.db import models
from django.utils.text import slugify


# Create your models here.

class Nationality(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='نام کشور')
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=100, unique=True, verbose_name='نام در url', allow_unicode=True)

    class Meta:
        verbose_name = 'کشور'
        verbose_name_plural = 'کشور ها'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if  self.slug != slugify(self.name) or self.slug == "":
            self.slug = slugify(self.name, allow_unicode=True)
            print('test۲')
        super().save(*args, **kwargs)



class Author(models.Model):
    first_name = models.CharField(max_length=200, verbose_name='نام')
    last_name = models.CharField(max_length=200, verbose_name='نام خانوادگی')
    url_title = models.SlugField(max_length=300, verbose_name='نام در url', db_index=True, default='', null=False, blank=True, allow_unicode=True)
    is_deleted = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    nationality = models.ForeignKey(Nationality, on_delete=models.CASCADE, verbose_name='ملیت')

    class Meta:
        verbose_name = 'نویسنده'
        verbose_name_plural = 'نویسنده ها'

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        if  self.url_title != slugify(self.first_name + ' ' + self.last_name) or self.url_title == "":
            self.url_title = slugify(self.first_name + ' ' + self.last_name, allow_unicode=True)
        super().save(*args, **kwargs)


class Translator(models.Model):
    first_name = models.CharField(max_length=200, verbose_name='نام')
    last_name = models.CharField(max_length=200, verbose_name='نام خانوادگی')
    url_title = models.SlugField(max_length=300, verbose_name='نام در url', db_index=True, default='', null=False, blank=True, allow_unicode=True)
    is_deleted = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'مترجم'
        verbose_name_plural = 'مترجم ها'

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        if  self.url_title != slugify(self.first_name + ' ' + self.last_name) or self.url_title == "":
            self.url_title = slugify(self.first_name + ' ' + self.last_name, allow_unicode=True)
        super().save(*args, **kwargs)


class Publisher(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام')
    url_title = models.SlugField(max_length=300, verbose_name='نام در url', db_index=True, null=False, blank=True, allow_unicode=True)
    is_deleted = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'ناشر'
        verbose_name_plural = 'ناشر ها'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if  self.url_title != slugify(self.name) or self.url_title == "":
            self.url_title = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Book(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان', db_index=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='نویسنده', related_name='author')
    page = models.PositiveIntegerField(verbose_name='صفحه')
    min_age = models.PositiveIntegerField(verbose_name='حداقل سن')
    translator = models.ForeignKey(Translator, on_delete=models.CASCADE, verbose_name='مترجم',related_name='translator')
    image = models.ImageField(upload_to='images/books', null=True, blank=True, verbose_name='تصویر کتاب')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, verbose_name='ناشر', related_name='publisher')
    count = models.PositiveIntegerField(default=0, verbose_name='تعداد')
    release_date = models.DateField(auto_now_add=True, editable=False, verbose_name='تاریخ عرضه')
    slug = models.SlugField(null=False, db_index=True, blank=True, max_length=200, unique=True,
                            verbose_name='عنوان در url', allow_unicode=True)
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    is_deleted = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        if  self.slug != slugify(self.title) or self.slug == "":
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def available_count(self):
        # شمارش تعداد کتاب‌های در حال امانت (برنگشته)
        borrowed_count = self.borrows.filter(returned_at__isnull=True).count()
        return self.count - borrowed_count

    @property
    def is_available(self):
        return self.available_count > 0