from django.contrib import admin
from . import models


# Register your models here.


admin.site.register(models.Book)
admin.site.register(models.Publisher)
admin.site.register(models.Author)
admin.site.register(models.Translator)
admin.site.register(models.Nationality)