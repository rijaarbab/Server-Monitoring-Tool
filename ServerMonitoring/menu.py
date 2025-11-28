import time
import subprocess
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from ServerMonitoring import dashboard

console = Console()
stress_process = None

def show_menu():
    console.clear()
    console.print(Panel.fit("Server Monitoring System"))
    console.print()
    
    menu = Table(title="Main Menu", show_header=False)
    menu.add_column("Option", width=10)
    menu.add_column("Description", width=50)
    
    menu.add_row("1", "Live Dashboard")
    menu.add_row("2", "Run CPU Stress Test")
    menu.add_row("3", "View Alert History")
    menu.add_row("0", "Exit")
    
    console.print(menu)
    console.print()

def run_stress_test():
    global stress_process
    
    console.clear()
    console.print(Panel.fit("CPU Stress Test"))
    console.print()
    
    console.print("\nStarting CPU stress test...")
    
    try:
        stress_process = subprocess.Popen(['stress-ng','--cpu', '0'])
        
        time.sleep(2)
        console.print("Stress test running!")
        console.print("\Starting Dashbord\n")
        time.sleep(2)
        
        dashboard.run_live_dashboard()
        
        try:
            stress_process.terminate()
            stress_process.wait()
        except:
            pass
        console.print("\nStress test stopped")
            
    except:
        console.print("\nSomething went wrong")

def stop_stress_if_running():
    global stress_process
    try:
        if stress_process:
            stress_process.terminate()
            stress_process.wait()
    except:
        pass

def view_alert_history():
    console.clear()
    console.print(Panel.fit("Alert History"))
    console.print()
    
    try:
        with open("alert_history.log", "r") as f:
            lines = f.readlines()
        
        if lines:
            console.print(f"Showing last 10 of {len(lines)} alerts:\n")
            for line in lines[-10:]:
                console.print(line.strip())
        else:
            console.print("No alerts in history")
            
    except:
        console.print("No alert history file found")
