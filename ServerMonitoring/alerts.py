import yaml
from datetime import datetime


cpu_warning = 70
cpu_critical = 90
mem_warning = 75
mem_critical = 90
disk_warning = 80
disk_critical = 95

def load_thresholds():
    global cpu_warning, cpu_critical
    global mem_warning, mem_critical
    global disk_warning, disk_critical
    
    try:
        with open("configs/config.yaml", 'r') as f:
            config = yaml.safe_load(f)
            thresholds = config['thresholds']
            
            cpu_warning = thresholds['cpu']['warning']
            cpu_critical = thresholds['cpu']['critical']
            mem_warning = thresholds['memory']['warning']
            mem_critical = thresholds['memory']['critical']
            disk_warning = thresholds['disk']['warning']
            disk_critical = thresholds['disk']['critical']
    except:
        pass  # No File, use defualt values
    
def check_alerts(metrics):
    load_thresholds()
    
    alerts_list = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Check CPU
    cpu = metrics['cpu_percent']
    if cpu >= cpu_critical:
        alerts_list.append({
            'time': timestamp,
            'level': 'CRITICAL',
            'type': 'CPU',
            'message': f'CPU usage critical: {cpu}%'
        })
    elif cpu >= cpu_warning:
        alerts_list.append({
            'time': timestamp,
            'level': 'WARNING',
            'type': 'CPU',
            'message': f'CPU usage high: {cpu}%'
        })
    
    # Check Memory
    memory = metrics['mem_percent']
    if memory >= mem_critical:
        alerts_list.append({
            'time': timestamp,
            'level': 'CRITICAL',
            'type': 'MEMORY',
            'message': f'Memory usage critical: {memory}%'
        })
    elif memory >= mem_warning:
        alerts_list.append({
            'time': timestamp,
            'level': 'WARNING',
            'type': 'MEMORY',
            'message': f'Memory usage high: {memory}%'
        })
    
    # Check Disk
    disk = metrics['disk_percent']
    if disk > 0:
        if disk >= disk_critical:
            alerts_list.append({
                'time': timestamp,
                'level': 'CRITICAL',
                'type': 'DISK',
                'message': f'Disk usage critical: {disk}%'
            })
        elif disk >= disk_warning:
            alerts_list.append({
                'time': timestamp,
                'level': 'WARNING',
                'type': 'DISK',
                'message': f'Disk usage high: {disk}%'
            })
    
    return alerts_list

def save_alert(alert):
    try:
        with open("alert_history.log", 'a') as f:
            line = f"[{alert['time']}] {alert['level']} - {alert['type']}: {alert['message']}\n"
            f.write(line)
    except:
        print("Could not save alerts")
