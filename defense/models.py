from django.db import models
from accounts.models import CustomUser

class SecurityPolicy(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    policy_type = models.CharField(max_length=50, choices=[
        ('encryption','Encryption'),
        ('authentication','Authentication'),
        ('firewall','Firewall Rules'),
        ('ids','Intrusion Detection'),
        ('backup','Backup & Recovery'),
    ])
    is_enabled = models.BooleanField(default=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    config_data = models.JSONField(default=dict)
    def __str__(self): return self.name

class MitigationAction(models.Model):
    STATUS = [('pending','Pending'),('executed','Executed'),('failed','Failed')]
    action_name = models.CharField(max_length=100)
    triggered_by = models.CharField(max_length=50)
    executed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    result = models.TextField(blank=True)
    is_automated = models.BooleanField(default=False)
    class Meta: ordering = ['-executed_at']

