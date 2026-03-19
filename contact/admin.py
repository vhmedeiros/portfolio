from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "sent_at", "read"]
    list_filter = ["read"]
    search_fields = ["name", "email", "subject"]
    readonly_fields = ["name", "email", "subject", "message", "sent_at"]

    def has_add_permission(self, request):
        return False
