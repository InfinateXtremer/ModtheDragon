from django.contrib import admin

from .models import *

# Register your models here.


@admin.register(Author)
class ModAdmin(admin.ModelAdmin):
    list_display = ("user","display_name",)