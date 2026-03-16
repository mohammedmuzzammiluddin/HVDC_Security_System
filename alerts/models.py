from django.db import models
from accounts.models import CustomUser

class Alert(models.Model):
    SEVERITY = [('info','Info'),('warning','Warning'),('danger','Danger'),('critical','Critical')]
    title = models.CharField(max_length=200)
    message = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY, default='info')
    source = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(CustomUser, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='resolved_alerts')

    class Meta: ordering = ['-created_at']
    def __str__(self): return f'{self.severity.upper()}: {self.title}'

class NotificationPreference(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email_on_critical = models.BooleanField(default=True)
    email_on_high = models.BooleanField(default=True)
    email_on_medium = models.BooleanField(default=False)
    dashboard_notifications = models.BooleanField(default=True)
    alert_sound = models.BooleanField(default=True)
    def __str__(self): return f'Prefs for {self.user.username}'
