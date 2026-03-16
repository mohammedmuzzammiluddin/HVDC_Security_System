# threat_detection/admin.py
from django.contrib import admin
from .models import ThreatLog, AIModel

@admin.register(ThreatLog)
class ThreatLogAdmin(admin.ModelAdmin):
    list_display = ['attack_type', 'severity', 'confidence_score', 'detected_at', 'is_confirmed']
    list_filter = ['attack_type', 'severity', 'is_confirmed']
    search_fields = ['source_ip', 'description']
    date_hierarchy = 'detected_at'

@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'version', 'accuracy', 'f1_score', 'is_active', 'uploaded_at']
    list_filter = ['is_active']