from django.db import models
from accounts.models import CustomUser

class Report(models.Model):
    REPORT_TYPES = [
        ('threat_summary','Threat Summary'),
        ('vulnerability','Vulnerability Assessment'),
        ('compliance','Compliance Report'),
        ('incident','Incident Report'),
    ]
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    generated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)
    file_path = models.FileField(upload_to='reports/', blank=True, null=True)
    period_from = models.DateField()
    period_to = models.DateField()
    summary = models.TextField(blank=True)

    class Meta: ordering = ['-generated_at']
    def __str__(self): return f'{self.title} ({self.report_type})'
