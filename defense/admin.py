from django.contrib import admin
from .models import SecurityPolicy, MitigationAction

@admin.register(SecurityPolicy)
class SecurityPolicyAdmin(admin.ModelAdmin):
    list_display = ['name', 'policy_type', 'is_enabled', 'created_at']
    list_filter = ['policy_type', 'is_enabled']

@admin.register(MitigationAction)
class MitigationActionAdmin(admin.ModelAdmin):
    list_display = ['action_name', 'triggered_by', 'status', 'executed_at']
    list_filter = ['status', 'is_automated']