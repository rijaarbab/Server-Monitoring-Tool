import time
import yaml
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from ServerMonitoring import metrics
from ServerMonitoring import alerts
from ServerMonitoring import notifications

console = Console()

#thresholds
cpu_warning = 70
cpu_critical = 90
mem_warning = 75
mem_critical = 90
disk_warning = 80
disk_critical = 95

#alert snooze time in seconds
alert_interval = 300  

def load_config():
    global cpu_warning, cpu_critical
    global mem_warning, mem_critical
    global disk_warning, disk_critical
    global alert_interval
    
    try:
        with open("configs/config.yaml", 'r') as f:
            config = yaml.safe_load(f)
            
            cpu_warning = config['thresholds']['cpu']['warning']
            cpu_critical = config['thresholds']['cpu']['critical']
            mem_warning = config['thresholds']['memory']['warning']
            mem_critical = config['thresholds']['memory']['critical']
            disk_warning = config['thresholds']['disk']['warning']
            disk_critical = config['thresholds']['disk']['critical']
            alert_interval = config['alert_settings']['min_alert_interval_minutes'] * 60
    except:
        pass 


def get_color_and_status(value, warning, critical):
    if value < warning:
        return "green", "Normal"
    elif value < critical:
        return "yellow", "Warning"
    else:
        return "red", "Critical"

def show_dashboard(data):
    
    cpu_percent = data['cpu_percent']
    cpu_cores = data['cpu_cores']
    mem_percent = data['mem_percent']
    mem_total = data['mem_total']
    mem_available = data['mem_available']
    disk_percent = data['disk_percent']
    disk_free = data['disk_free']
    net_sent = data['net_sent']
    net_recv = data['net_recv']
    hostname = data['hostname']
    os_name = data['os']
    uptime = data['uptime']
    
    # Getting System info
    info = f"Host: {hostname} | OS: {os_name} | CPU Cores: {cpu_cores} | RAM: {mem_total:.1f} GB | Uptime: {uptime:.1f}h"
    console.print(Panel(info, title="System Information"))
    console.print()
    
    # Creating dashboard table
    table = Table(title="Server Monitoring Dashboard", show_header=True)
    table.add_column("Metric", width=20)
    table.add_column("Value", width=20)
    table.add_column("Status", width=20)
    
    # CPU Stats
    cpu_color, cpu_status = get_color_and_status(cpu_percent, cpu_warning, cpu_critical )
    table.add_row("CPU Usage", f"[{cpu_color}]{cpu_percent}%[/{cpu_color}]", f"[{cpu_color}]{cpu_status}[/{cpu_color}]")
    
    # Memory Stats
    mem_color, mem_status = get_color_and_status(mem_percent, mem_warning, mem_critical)
    table.add_row("Memory Usage", f"[{mem_color}]{mem_percent}%[/{mem_color}]", f"[{mem_color}]{mem_status}[/{mem_color}]")
    
    # Disk Stats
    if disk_percent > 0:
        disk_color, disk_status = get_color_and_status(disk_percent, disk_warning, disk_critical)
        table.add_row("Disk Usage", f"[{disk_color}]{disk_percent}%[/{disk_color}]", f"[{disk_color}]{disk_status}[/{disk_color}]")
    
    table.add_row("--------------------", "--------------------", "--------------------", style="dim")
    table.add_row("Available Memory", f"{mem_available:.1f} GB", "Info")
    table.add_row("Free Disk Space", f"{disk_free:.1f} GB", "Info")
    table.add_row("Network Sent", f"{net_sent:.1f} MB", "Info")
    table.add_row("Network Received", f"{net_recv:.1f} MB", "Info")
    
    console.print(table)

def run_live_dashboard():
    console.clear()
    
    load_config()
    
    alert_sent_count = 0
    last_alert_time = 0
    
    try:
        while True:
            
            data = metrics.get_metrics()
            
            console.clear()
            console.print(f"\nServer Monitoring Active - Alerts Sent: {alert_sent_count}\n")
            
            show_dashboard(data)
            console.print()
            
            #Check alert snooze time
            current_time = time.time()
            if current_time - last_alert_time > alert_interval:
                alert_list = alerts.check_alerts(data)
                
                if alert_list:
                    for alert in alert_list:
                        alerts.save_alert(alert)
                        notifications.send_notifications(alert, data)
                    console.print("Alert Sent")
                    alert_sent_count = alert_sent_count + len(alert_list)
                
                last_alert_time = current_time
            
            console.print("Press Ctrl+C to stop server monitoring")
            time.sleep(2)
    
    except KeyboardInterrupt:
        console.print("\nMonitoring stopped")
        console.print(f"Total alerts: {alert_sent_count}\n")
