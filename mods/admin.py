from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from mptt.models import TreeManyToManyField
from mptt.admin import DraggableMPTTAdmin
from .models import *

# Register your models here.

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    
@admin.register(GameBackground)
class GameBackgroundAdmin(admin.ModelAdmin):
    list_display = ("__str__", "game", "artist")

@admin.register(Mod)
class ModAdmin(admin.ModelAdmin):
    list_display = ("title", "game", "author")
    prepopulated_fields = {"slug": ("title",)}


class TagAdmin(DraggableMPTTAdmin):
    pass
admin.site.register(Tag, TagAdmin)
