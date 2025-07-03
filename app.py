from flask import Flask, render_template, jsonify
import psutil
import json
from datetime import datetime

app = Flask(__name__)

def get_system_data():
    cpu = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']),
                       key=lambda p: p.info['cpu_percent'], reverse=True)[:10]

    data = {
        'timestamp': datetime.now().isoformat(),
        'cpu': cpu,
        'memory': memory.percent,
        'disk': disk.percent,
        'net_sent': net.bytes_sent,
        'net_recv': net.bytes_recv,
        'top_processes': [
            {'pid': p.info['pid'], 'name': p.info['name'], 'cpu': p.info['cpu_percent']}
            for p in processes
        ]
    }
    with open('resource_log.json', 'a') as f:
        json.dump(data, f)
        f.write('\n')

    with open('alerts.log', 'a') as alert_file:
        if cpu > 2:
            alert_file.write(f"[ALERT] High CPU usage: {cpu}% at {data['timestamp']}\n")
        if memory.percent > 80:
            alert_file.write(f"[ALERT] High Memory usage: {memory.percent}% at {data['timestamp']}\n")
        if disk.percent > 90:
            alert_file.write(f"[ALERT] High Disk usage: {disk.percent}% at {data['timestamp']}\n")

    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/data')
def data():
    return jsonify(get_system_data())

if __name__ == '__main__':
    app.run(debug=True)
