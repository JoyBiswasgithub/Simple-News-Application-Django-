from django.contrib import admin

# Register your models here.
from .models import NewsPost

@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display=("id", "user", "title", "desc", "uploaded_at")
