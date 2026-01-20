# Auto-Recovery Infrastructure Prototype

This project demonstrates a fault-tolerant container architecture designed to detect application failures and automatically recover service without human intervention. It replicates the core "Liveness Probe" and "Restart Policy" logic found in orchestrators like Kubernetes, but built from scratch using Python and Docker for containerization.

## 🏗 Architecture

The system consists of two isolated containers networked via Docker Compose:

1.  **The Victim (`victim-service`)**:
    - A Flask-based web application designed with a "Kill Switch" endpoint (`/crash`).
    - Simulates a critical production failure (Process ID 1 Hard Exit).
2.  **The Recovery Agent (`recov-agent`)**:
    - A "Sidecar" Python service that polls the application's HTTP health every 2 seconds.
    - Upon detecting a failure (timeout or connection refusal), it utilizes the **Docker Socket (`/var/run/docker.sock`)** to issue a restart command to the specific container.

## 🚀 How to Run

### Prerequisites

- Docker & Docker Compose

### Quick Start

1.  Clone the repository:

    ```bash
    git clone https://github.com/nathertan/self-recov-docker
    cd self-recov-docker
    ```

2.  Launch the stack:

    ```bash
    docker compose up --build
    ```

3.  **Simulate a Crash:**
    Open your browser and navigate to:
    `http://localhost:5000/crash`

4.  **Observe Recovery:**
    Watch the terminal logs. You will see the `recov-agent` detect the downtime and restart the `victim-service` immediately.

## 📂 Project Structure

```text
.
├── docker-compose.yaml      # Orchestrates the network and volume mounting
├── victim/                  # The Web Application
│   ├── app.py               # Flask app with os._exit(1) capability
│   └── Dockerfile           # Python envir onment setup
└── recov-agent/             # The Watchdog Service
    ├── recov-agent.py       # Logic for health checking & Docker API calls
    └── Dockerfile           # Python + Docker SDK setup
```
