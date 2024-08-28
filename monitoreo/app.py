from flask import Flask, jsonify, render_template
import docker
import psutil

app = Flask(_name_)

app.jinja_env.filters['filesizeformat'] = lambda value: f"{value / (1024 * 1024):.2f} MB"

# Crear cliente de Docker
client = docker.from_env()

def calculate_cpu_usage(stats):
    cpu_stats = stats['cpu_stats']
    precpu_stats = stats['precpu_stats']
    
    cpu_delta = cpu_stats['cpu_usage']['total_usage'] - precpu_stats['cpu_usage']['total_usage']
    system_cpu_delta = cpu_stats['system_cpu_usage'] - precpu_stats['system_cpu_usage']
    
    if system_cpu_delta > 0:
        cpu_usage = (cpu_delta / system_cpu_delta) * 100 * len(cpu_stats['cpu_usage']['percpu_usage'])
    else:
        cpu_usage = 0

    return cpu_usage

@app.route('/')
def index():
    try:
        # Obtener información del host
        host_info = {
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'memory_used': psutil.virtual_memory().used,
            'disk_total': psutil.disk_usage('/').total,
            'disk_used': psutil.disk_usage('/').used
        }

        # Obtener información del contenedor
        containers_info = []
        for container in client.containers.list():
            container_stats = container.stats(stream=False)
            containers_info.append({
                'id': container.short_id,
                'name': container.name,
                'status': container.status,
                'image': container.image.tags,
                'cpu_usage': calculate_cpu_usage(container_stats),
                'memory_usage': container_stats['memory_stats']['usage']
            })

        return render_template('index.html', host_info=host_info, containers_info=containers_info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5000)