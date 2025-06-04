from django.contrib import admin
from .models import MenuItem
from django.utils.html import format_html # For displaying image in admin

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'display_image_thumbnail', 'updated_at')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    ordering = ('category', 'name')

    # Add image to readonly_fields to show it in the form, or customize form for better display
    # fields = ('name', 'description', 'price', 'category', 'image', 'image_preview', 'is_available')
    # readonly_fields = ('image_preview',)


    def display_image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    display_image_thumbnail.short_description = 'Image'

admin.site.register(MenuItem, MenuItemAdmin)

from .models import ContactMessage # Add this import

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at', 'is_read')
    list_filter = ('is_read', 'submitted_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'message', 'submitted_at') # Make fields read-only in admin detail view

    def has_add_permission(self, request): # Prevent adding new messages from admin
        return False

admin.site.register(ContactMessage, ContactMessageAdmin)
