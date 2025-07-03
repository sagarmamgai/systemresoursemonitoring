function updateData() {
    fetch('/data')
        .then(res => res.json())
        .then(data => {
            document.getElementById('cpu').textContent = `CPU Usage: ${data.cpu}%`;
            document.getElementById('memory').textContent = `Memory Usage: ${data.memory}%`;
            document.getElementById('disk').textContent = `Disk Usage: ${data.disk}%`;
            document.getElementById('net').textContent = `Net: ${data.net_sent} Sent / ${data.net_recv} Recv`;

            const processList = document.getElementById('processes');
            processList.innerHTML = '';
            data.top_processes.forEach(proc => {
                const li = document.createElement('li');
                li.textContent = `${proc.name} (PID: ${proc.pid}) - CPU: ${proc.cpu}%`;
                processList.appendChild(li);
            });
        });
}
setInterval(updateData, 2000);
updateData();
