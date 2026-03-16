from django.contrib import admin
from .models import Alert, NotificationPreference

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'severity', 'is_resolved', 'created_at']
    list_filter = ['severity', 'is_resolved']

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_on_critical', 'email_on_high', 'dashboard_notifications']