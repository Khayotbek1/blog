from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',)



