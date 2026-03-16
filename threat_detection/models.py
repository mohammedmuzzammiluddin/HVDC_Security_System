from django.db import models
from accounts.models import CustomUser

class ThreatLog(models.Model):
    ATTACK_TYPES = [
        ('normal','Normal'),
        ('dos','Denial of Service'),
        ('fdi','False Data Injection'),
        ('cmd_manip','Command Manipulation'),
        ('replay','Replay Attack'),
    ]
    SEVERITY = [('low','Low'),('medium','Medium'),('high','High'),('critical','Critical')]
    detected_at = models.DateTimeField(auto_now_add=True)
    attack_type = models.CharField(max_length=20, choices=ATTACK_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY, default='medium')
    source_ip = models.GenericIPAddressField(blank=True, null=True)
    confidence_score = models.FloatField(default=0.0)
    dc_voltage = models.FloatField()
    dc_current = models.FloatField()
    active_power = models.FloatField()
    network_packet_rate = models.IntegerField(default=0)
    communication_latency = models.FloatField(default=0.0)
    description = models.TextField(blank=True)
    is_confirmed = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(CustomUser, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='reviewed_threats')

    class Meta: ordering = ['-detected_at']

    def __str__(self): return f'{self.attack_type} | {self.severity} | {self.detected_at}'

class AIModel(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    file_path = models.CharField(max_length=500)
    accuracy = models.FloatField(default=0.0)
    precision = models.FloatField(default=0.0)
    recall = models.FloatField(default=0.0)
    f1_score = models.FloatField(default=0.0)
    threshold = models.FloatField(default=0.5)
    is_active = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    trained_on = models.IntegerField(default=0, help_text='Number of training samples')

    def __str__(self): return f'{self.name} v{self.version}'
