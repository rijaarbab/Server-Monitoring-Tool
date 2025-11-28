import psutil
import platform
import time

def get_metrics():
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_cores = psutil.cpu_count()
    
    # Memory
    mem = psutil.virtual_memory()
    mem_percent = mem.percent
    mem_total = mem.total / (1024*1024*1024)  # For GB Conversion
    mem_available = mem.available / (1024*1024*1024) # For GB  Conversion
    
    # Disk
    disk_percent = 0
    disk_free = 0
    try:
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_free = disk.free / (1024*1024*1024)  # For GB Conversion
    except:
        pass
    
    # Network
    net = psutil.net_io_counters()
    net_sent = net.bytes_sent / (1024*1024)  # For MB Conversion
    net_recv = net.bytes_recv / (1024*1024)  # For MB Conversion
    
    # System Info
    boot_time = psutil.boot_time()
    uptime = (time.time() - boot_time) / 3600
    
    return {
        'cpu_percent': cpu_percent,
        'cpu_cores': cpu_cores,
        'mem_percent': mem_percent,
        'mem_total': mem_total,
        'mem_available': mem_available,
        'disk_percent': disk_percent,
        'disk_free': disk_free,
        'net_sent': net_sent,
        'net_recv': net_recv,
        'hostname': platform.node(),
        'os': platform.system(),
        'uptime': uptime
    }
