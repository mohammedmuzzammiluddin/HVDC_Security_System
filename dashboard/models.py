from django.db import models

class SystemStatus(models.Model):
    STATUS_CHOICES = [('online','Online'),('warning','Warning'),('offline','Offline')]
    component = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='online')
    last_updated = models.DateTimeField(auto_now=True)
    details = models.TextField(blank=True)

    def __str__(self): return f'{self.component} - {self.status}'
