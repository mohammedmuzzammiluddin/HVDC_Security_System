from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import ThreatLog, AIModel
from .ml_detector import predict_threat
from monitoring.models import HVDCReading

@login_required
def threat_dashboard(request):
    threats = ThreatLog.objects.order_by('-detected_at')[:100]
    stats = {
        'total': ThreatLog.objects.count(),
        'dos': ThreatLog.objects.filter(attack_type='dos').count(),
        'fdi': ThreatLog.objects.filter(attack_type='fdi').count(),
        'cmd': ThreatLog.objects.filter(attack_type='cmd_manip').count(),
        'critical': ThreatLog.objects.filter(severity='critical').count(),
    }
    return render(request, 'threat_detection/dashboard.html',
                  {'threats': threats, 'stats': stats})

@login_required
def run_detection(request):
    reading = HVDCReading.objects.order_by('-timestamp').first()
    if not reading:
        messages.error(request, 'No sensor data found.')
        return redirect('threat_detection:dashboard')
    features = {
        'dc_voltage': reading.dc_voltage, 'dc_current': reading.dc_current,
        'ac_voltage_rectifier': reading.ac_voltage_rectifier,
        'ac_voltage_inverter': reading.ac_voltage_inverter,
        'active_power': reading.active_power,
        'reactive_power': reading.reactive_power,
        'firing_angle_rectifier': reading.firing_angle_rectifier,
        'extinction_angle_inverter': reading.extinction_angle_inverter,
        'network_packet_rate': reading.network_packet_rate,
        'communication_latency': reading.communication_latency,
    }
    result = predict_threat(features)
    severity = 'low' if result['confidence'] < 0.6 else 'medium' if result['confidence'] < 0.8 else 'high'
    if result['attack_type'] != 'normal':
        severity = 'critical' if result['confidence'] > 0.9 else severity
    ThreatLog.objects.create(
        attack_type=result['attack_type'], severity=severity,
        confidence_score=result['confidence'],
        dc_voltage=reading.dc_voltage, dc_current=reading.dc_current,
        active_power=reading.active_power,
        network_packet_rate=reading.network_packet_rate,
        communication_latency=reading.communication_latency,
        description=f'AI detected: {result["attack_type"]} (conf={result["confidence"]:.2f})'
    )
    messages.success(request, f'Detection complete: {result["attack_type"]} detected.')
    return redirect('threat_detection:dashboard')
