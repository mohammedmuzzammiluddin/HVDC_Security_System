from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import SecurityPolicy, MitigationAction

@login_required
def defense_dashboard(request):
    policies = SecurityPolicy.objects.all()
    recent_actions = MitigationAction.objects.order_by('-executed_at')[:10]
    return render(request, 'defense/dashboard.html',
                  {'policies': policies, 'recent_actions': recent_actions})

@login_required
def toggle_policy(request, pk):
    policy = get_object_or_404(SecurityPolicy, pk=pk)
    if not request.user.is_admin():
        messages.error(request, 'Only admins can change policies.')
        return redirect('defense:dashboard')
    policy.is_enabled = not policy.is_enabled
    policy.save()
    messages.success(request, f'Policy {"enabled" if policy.is_enabled else "disabled"}.')
    return redirect('defense:dashboard')

@login_required
def execute_mitigation(request, action_name):
    if not request.user.is_admin():
        messages.error(request, 'Permission denied.')
        return redirect('defense:dashboard')
    MitigationAction.objects.create(
        action_name=action_name, triggered_by=request.user.username,
        status='executed', result=f'Action {action_name} executed successfully.'
    )
    messages.success(request, f'Mitigation action "{action_name}" executed.')
    return redirect('defense:dashboard')
