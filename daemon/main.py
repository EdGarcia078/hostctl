import time
import os
from daemon.config_loader import load_config
from daemon.process_runner import run_detached

docker_processes = []
cloudflared_process = None


def start_docker_projects(projects):
    global docker_processes

    for path in projects:
        print(f"[hostctl] Starting Docker in {path}")

        p = run_detached(
            ["docker", "compose", "up", "-d"],
            cwd=path
        )

        docker_processes.append(p)


def start_cloudflare(tunnel_id):
    global cloudflared_process

    print("[hostctl] Starting Cloudflare Tunnel")

    cloudflared_process = run_detached(
        ["cloudflared", "tunnel", "run", tunnel_id]
    )


def main():
    config = load_config()

    countdown = config.get("countdown", 0)
    docker_projects = config.get("docker_projects", [])
    tunnel_id = config.get("cloudflare_tunnel")

    print(f"[hostctl] Countdown: {countdown}s")

    # simple countdown
    for i in range(countdown, 0, -1):
        print(f"[hostctl] Starting in {i}s...")
        time.sleep(1)

    print("[hostctl] Starting services...")

    start_docker_projects(docker_projects)
    start_cloudflare(tunnel_id)

    time.sleep(2)

    if cloudflared_process.poll() is not None:
        print("[hostctl] Cloudflare FAILED to start")
    else:
        print(f"[hostctl] Cloudflare RUNNING PID={cloudflared_process.pid}")

    # mantener vivo el daemon
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
