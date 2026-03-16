from django.db import models
from accounts.models import CustomUser

class AttackScenario(models.Model):
    name = models.CharField(max_length=100)
    attack_type = models.CharField(max_length=50)
    description = models.TextField()
    parameters = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

    def __str__(self): return self.name

class SimulationRun(models.Model):
    STATUS = [('pending','Pending'),('running','Running'),('completed','Completed'),('failed','Failed')]
    scenario = models.ForeignKey(AttackScenario, on_delete=models.CASCADE)
    run_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    results = models.JSONField(default=dict)
    voltage_impact = models.FloatField(default=0.0)
    power_impact = models.FloatField(default=0.0)
    detection_time_ms = models.IntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta: ordering = ['-started_at']
