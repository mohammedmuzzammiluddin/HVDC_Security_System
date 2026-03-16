# dashboard/admin.py
from django.contrib import admin
from .models import SystemStatus

@admin.register(SystemStatus)
class SystemStatusAdmin(admin.ModelAdmin):
    list_display = ['component', 'status', 'last_updated']
    list_filter = ['status']