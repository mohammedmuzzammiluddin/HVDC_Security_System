from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import AttackScenario, SimulationRun
import random, time

@login_required
def scenario_list(request):
    scenarios = AttackScenario.objects.filter(is_active=True)
    runs = SimulationRun.objects.filter(run_by=request.user).order_by('-started_at')[:10]
    return render(request, 'simulation/scenarios.html', {'scenarios': scenarios, 'runs': runs})

@login_required
def run_scenario(request, pk):
    scenario = get_object_or_404(AttackScenario, pk=pk)
    start_time = time.time()
    # Simulate attack effect on HVDC parameters
    if scenario.attack_type == 'dos':
        voltage_impact = random.uniform(-15, -5)
        power_impact = random.uniform(-30, -10)
    elif scenario.attack_type == 'fdi':
        voltage_impact = random.uniform(10, 25)
        power_impact = random.uniform(5, 20)
    else:
        voltage_impact = random.uniform(-10, 10)
        power_impact = random.uniform(-15, 15)
    detection_ms = int((time.time() - start_time) * 1000) + random.randint(50, 500)
    SimulationRun.objects.create(
        scenario=scenario, run_by=request.user,
        status='completed', completed_at=timezone.now(),
        voltage_impact=voltage_impact, power_impact=power_impact,
        detection_time_ms=detection_ms,
        results={'scenario': scenario.name, 'attack_type': scenario.attack_type,
                 'voltage_impact': voltage_impact, 'power_impact': power_impact}
    )
    messages.success(request, f'Simulation "{scenario.name}" completed.')
    return redirect('simulation:results')

@login_required
def results(request):
    runs = SimulationRun.objects.filter(run_by=request.user).order_by('-started_at')[:20]
    return render(request, 'simulation/results.html', {'runs': runs})
