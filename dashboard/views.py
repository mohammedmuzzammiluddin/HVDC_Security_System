# dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from monitoring.models import HVDCReading
from threat_detection.models import ThreatLog, AIModel
from alerts.models import Alert
from vulnerability.models import Vulnerability
from defense.models import MitigationAction
from accounts.models import CustomUser
from .models import SystemStatus
from django.utils import timezone
from datetime import timedelta

@login_required
def home(request):
    if request.user.is_admin():
        return admin_dashboard(request)
    return user_dashboard(request)

def admin_dashboard(request):
    now = timezone.now()
    last_24h = now - timedelta(hours=24)
    last_7d  = now - timedelta(days=7)

    ctx = {
        # User stats
        'total_users': CustomUser.objects.count(),
        'admin_count': CustomUser.objects.filter(role='admin').count(),
        'analyst_count': CustomUser.objects.filter(role='analyst').count(),
        'viewer_count': CustomUser.objects.filter(role='viewer').count(),
        'recent_users': CustomUser.objects.order_by('-date_joined')[:5],

        # Threat stats
        'threats_24h': ThreatLog.objects.filter(detected_at__gte=last_24h).count(),
        'threats_7d': ThreatLog.objects.filter(detected_at__gte=last_7d).count(),
        'critical_threats': ThreatLog.objects.filter(severity='critical').count(),
        'threat_type_counts': {
            'dos': ThreatLog.objects.filter(attack_type='dos', detected_at__gte=last_7d).count(),
            'fdi': ThreatLog.objects.filter(attack_type='fdi', detected_at__gte=last_7d).count(),
            'cmd': ThreatLog.objects.filter(attack_type='cmd_manip', detected_at__gte=last_7d).count(),
            'replay': ThreatLog.objects.filter(attack_type='replay', detected_at__gte=last_7d).count(),
            'normal': ThreatLog.objects.filter(attack_type='normal', detected_at__gte=last_7d).count(),
        },
        'recent_threats': ThreatLog.objects.order_by('-detected_at')[:8],

        # System health
        'active_alerts': Alert.objects.filter(is_resolved=False).count(),
        'critical_alerts': Alert.objects.filter(is_resolved=False, severity='critical').count(),
        'latest_reading': HVDCReading.objects.order_by('-timestamp').first(),
        'system_statuses': SystemStatus.objects.all(),

        # AI model
        'active_model': AIModel.objects.filter(is_active=True).first(),
        'total_models': AIModel.objects.count(),

        # Vulnerability
        'open_vulns': Vulnerability.objects.filter(status='open').count(),
        'critical_vulns': Vulnerability.objects.filter(severity='critical', status='open').count(),

        # Mitigation
        'recent_mitigations': MitigationAction.objects.order_by('-executed_at')[:5],
        'mitigations_today': MitigationAction.objects.filter(executed_at__gte=last_24h).count(),

        'is_admin_view': True,
    }
    return render(request, 'dashboard/admin_home.html', ctx)

def user_dashboard(request):
    now = timezone.now()
    last_24h = now - timedelta(hours=24)

    ctx = {
        'threats_24h': ThreatLog.objects.filter(detected_at__gte=last_24h).count(),
        'active_alerts': Alert.objects.filter(is_resolved=False).count(),
        'my_alerts': Alert.objects.filter(is_resolved=False).order_by('-created_at')[:5],
        'latest_reading': HVDCReading.objects.order_by('-timestamp').first(),
        'recent_threats': ThreatLog.objects.order_by('-detected_at')[:6],
        'threat_counts': {
            'dos': ThreatLog.objects.filter(attack_type='dos', detected_at__gte=last_24h).count(),
            'fdi': ThreatLog.objects.filter(attack_type='fdi', detected_at__gte=last_24h).count(),
            'cmd': ThreatLog.objects.filter(attack_type='cmd_manip', detected_at__gte=last_24h).count(),
        },
        'open_vulns': Vulnerability.objects.filter(status='open').count(),
        'is_admin_view': False,
    }
    return render(request, 'dashboard/user_home.html', ctx)