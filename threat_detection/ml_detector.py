import joblib
import numpy as np
import os
from django.conf import settings

MODEL_PATH = os.path.join(settings.ML_MODELS_DIR, 'hvdc_rf_model.pkl')
SCALER_PATH = os.path.join(settings.ML_MODELS_DIR, 'scaler.pkl')

def load_model():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler

def predict_threat(features: dict):
    """
    features = {
      'dc_voltage': float, 'dc_current': float,
      'ac_voltage_rectifier': float, 'ac_voltage_inverter': float,
      'active_power': float, 'reactive_power': float,
      'firing_angle_rectifier': float, 'extinction_angle_inverter': float,
      'network_packet_rate': int, 'communication_latency': float
    }
    """
    try:
        model, scaler = load_model()
        feature_order = [
            'dc_voltage','dc_current','ac_voltage_rectifier',
            'ac_voltage_inverter','active_power','reactive_power',
            'firing_angle_rectifier','extinction_angle_inverter',
            'network_packet_rate','communication_latency'
        ]
        X = np.array([[features[k] for k in feature_order]])
        X_scaled = scaler.transform(X)
        pred = model.predict(X_scaled)[0]
        proba = model.predict_proba(X_scaled)[0]
        confidence = float(max(proba))
        label_map = {0:'normal',1:'dos',2:'fdi',3:'cmd_manip',4:'replay'}
        return {'attack_type': label_map.get(pred, 'unknown'),
                'confidence': confidence,
                'probabilities': {label_map[i]: float(p) for i, p in enumerate(proba)}}
    except Exception as e:
        return {'attack_type': 'unknown', 'confidence': 0.0, 'error': str(e)}
