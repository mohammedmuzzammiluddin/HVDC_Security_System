"""
HVDC CyberSec Dataset Generator
Run: python datasets/generate_dataset.py
Generates: datasets/hvdc_cyber_dataset.csv
"""
import numpy as np
import pandas as pd
import random

np.random.seed(42)
random.seed(42)
N = 5000  # Total samples

def normal_operation(n):
    return pd.DataFrame({
        'dc_voltage': np.random.normal(500, 5, n),
        'dc_current': np.random.normal(2.0, 0.1, n),
        'ac_voltage_rectifier': np.random.normal(220, 3, n),
        'ac_voltage_inverter': np.random.normal(215, 3, n),
        'active_power': np.random.normal(1000, 20, n),
        'reactive_power': np.random.normal(50, 10, n),
        'firing_angle_rectifier': np.random.normal(15, 1, n),
        'extinction_angle_inverter': np.random.normal(18, 1, n),
        'network_packet_rate': np.random.randint(100, 300, n),
        'communication_latency': np.random.normal(5, 0.5, n),
        'label': 0  # 0 = normal
    })

def dos_attack(n):
    return pd.DataFrame({
        'dc_voltage': np.random.normal(490, 15, n),
        'dc_current': np.random.normal(1.8, 0.3, n),
        'ac_voltage_rectifier': np.random.normal(210, 10, n),
        'ac_voltage_inverter': np.random.normal(205, 10, n),
        'active_power': np.random.normal(950, 50, n),
        'reactive_power': np.random.normal(60, 15, n),
        'firing_angle_rectifier': np.random.normal(15, 2, n),
        'extinction_angle_inverter': np.random.normal(18, 2, n),
        'network_packet_rate': np.random.randint(5000, 50000, n),
        'communication_latency': np.random.normal(200, 50, n),
        'label': 1  # 1 = DoS
    })

def fdi_attack(n):
    return pd.DataFrame({
        'dc_voltage': np.random.normal(520, 20, n),   # falsely elevated
        'dc_current': np.random.normal(2.5, 0.4, n),
        'ac_voltage_rectifier': np.random.normal(235, 15, n),
        'ac_voltage_inverter': np.random.normal(230, 15, n),
        'active_power': np.random.normal(1100, 80, n),
        'reactive_power': np.random.normal(80, 20, n),
        'firing_angle_rectifier': np.random.normal(20, 5, n),
        'extinction_angle_inverter': np.random.normal(22, 5, n),
        'network_packet_rate': np.random.randint(150, 400, n),  # similar to normal
        'communication_latency': np.random.normal(6, 1, n),
        'label': 2  # 2 = FDI
    })

def cmd_manip_attack(n):
    return pd.DataFrame({
        'dc_voltage': np.random.normal(480, 30, n),
        'dc_current': np.random.normal(3.0, 0.8, n),  # high current
        'ac_voltage_rectifier': np.random.normal(200, 20, n),
        'ac_voltage_inverter': np.random.normal(195, 20, n),
        'active_power': np.random.normal(850, 100, n),
        'reactive_power': np.random.normal(120, 30, n),
        'firing_angle_rectifier': np.random.normal(30, 8, n),  # abnormal angle
        'extinction_angle_inverter': np.random.normal(35, 8, n),
        'network_packet_rate': np.random.randint(200, 600, n),
        'communication_latency': np.random.normal(15, 5, n),
        'label': 3  # 3 = Command Manipulation
    })

def replay_attack(n):
    return pd.DataFrame({
        'dc_voltage': np.random.normal(500, 5, n),   # similar to normal
        'dc_current': np.random.normal(2.0, 0.1, n),
        'ac_voltage_rectifier': np.random.normal(220, 3, n),
        'ac_voltage_inverter': np.random.normal(215, 3, n),
        'active_power': np.random.normal(1000, 20, n),
        'reactive_power': np.random.normal(50, 10, n),
        'firing_angle_rectifier': np.random.normal(15, 1, n),
        'extinction_angle_inverter': np.random.normal(18, 1, n),
        'network_packet_rate': np.random.randint(280, 450, n),  # slightly elevated
        'communication_latency': np.random.normal(8, 2, n),
        'label': 4  # 4 = Replay Attack
    })

# Generate samples per class
n_each = N // 5
df = pd.concat([
    normal_operation(n_each),
    dos_attack(n_each),
    fdi_attack(n_each),
    cmd_manip_attack(n_each),
    replay_attack(n_each),
], ignore_index=True)

# Shuffle dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save to CSV
df.to_csv('datasets/hvdc_cyber_dataset.csv', index=False)

print(f'Dataset generated: {len(df)} samples')
print('Label distribution:')
label_map = {0:'Normal',1:'DoS',2:'FDI',3:'Cmd Manip',4:'Replay'}
for k, v in df['label'].value_counts().sort_index().items():
    print(f'  {label_map[k]}: {v}')
print('Saved to: datasets/hvdc_cyber_dataset.csv')
