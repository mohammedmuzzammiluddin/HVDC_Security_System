from django.contrib import admin
from .models import AttackScenario, SimulationRun

@admin.register(AttackScenario)
class AttackScenarioAdmin(admin.ModelAdmin):
    list_display = ['name', 'attack_type', 'is_active']
    list_filter = ['attack_type', 'is_active']

@admin.register(SimulationRun)
class SimulationRunAdmin(admin.ModelAdmin):
    list_display = ['scenario', 'run_by', 'status', 'started_at']
    list_filter = ['status']