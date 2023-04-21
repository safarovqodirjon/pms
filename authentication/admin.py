from django.contrib import admin
from django.utils.html import format_html

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_employee', 'is_manager', 'departament', 'user_img')
    list_filter = ('is_employee', 'is_manager', 'departament')
    search_fields = ('username', 'email', 'departament')

    def user_img(self, obj):
        if obj.image:
            return format_html(f'<a href={obj.image.url}><img src="{obj.image.url}" width="35px"></a>')

    user_img.short_description = 'user_image'


admin.site.register(CustomUser, CustomUserAdmin)
