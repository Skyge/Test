from django.contrib import admin
from .models import Comment


class Commentadmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'text')


admin.site.register(Comment, Commentadmin)
