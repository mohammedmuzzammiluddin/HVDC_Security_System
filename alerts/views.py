from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Alert, NotificationPreference

@login_required
def alert_list(request):
    alerts = Alert.objects.all()
    active = alerts.filter(is_resolved=False)
    resolved = alerts.filter(is_resolved=True)[:20]
    return render(request, 'alerts/list.html',
                  {'active': active, 'resolved': resolved})

@login_required
def resolve_alert(request, pk):
    alert = get_object_or_404(Alert, pk=pk)
    alert.is_resolved = True
    alert.resolved_at = timezone.now()
    alert.resolved_by = request.user
    alert.save()
    messages.success(request, 'Alert resolved.')
    return redirect('alerts:list')

@login_required
def preferences(request):
    prefs, _ = NotificationPreference.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        prefs.email_on_critical = 'email_on_critical' in request.POST
        prefs.email_on_high = 'email_on_high' in request.POST
        prefs.email_on_medium = 'email_on_medium' in request.POST
        prefs.dashboard_notifications = 'dashboard_notifications' in request.POST
        prefs.alert_sound = 'alert_sound' in request.POST
        prefs.save()
        messages.success(request, 'Preferences saved.')
    pref_fields = [
        ('Email on Critical alerts', 'email_on_critical', prefs.email_on_critical),
        ('Email on High alerts', 'email_on_high', prefs.email_on_high),
        ('Email on Medium alerts', 'email_on_medium', prefs.email_on_medium),
        ('Dashboard notifications', 'dashboard_notifications', prefs.dashboard_notifications),
        ('Alert sound', 'alert_sound', prefs.alert_sound),
    ]
    return render(request, 'alerts/preferences.html', {'prefs': prefs, 'pref_fields': pref_fields})