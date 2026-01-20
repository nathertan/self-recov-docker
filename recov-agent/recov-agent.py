import docker
import time
import requests

client = docker.from_env()
container_name = "my-victim"
# Ensure this matches your ip addr show docker0 (usually 172.17.0.1)
WHATSAPP_BOT_URL = "http://172.17.0.1:3000/alert"

print("Recovery Agent started... Monitoring begins.", flush=True)

def send_alert(msg):
    try:
        print(f"-> Attempting to contact Bot at {WHATSAPP_BOT_URL}...", flush=True)
        payload = {"message": msg}
        # 5 second timeout to ensure we don't give up too fast
        requests.post(WHATSAPP_BOT_URL, json=payload, timeout=5)
        print(f"-> Alert sent to WhatsApp: {msg}", flush=True)
    except Exception as e:
        print(f"-> FAILED TO SEND ALERT. Reason: {e}", flush=True)

while True:
    try:
        # Check if victim is alive
        response = requests.get('http://victim-service:5000', timeout=2)
    except:
        # If we are here, the victim is dead
        print("Status: DOWN! Initiating recovery...", flush=True)
        try:
            # 1. Restart
            container = client.containers.get(container_name)
            container.restart()
            print("RESTART SUCCESSFUL.", flush=True)
            
            # 2. Alert
            send_alert(f"The container {container_name} crashed and was restarted.")
            
            # Wait for boot
            time.sleep(5) 
        except Exception as e:
            print(f"Error during recovery: {e}", flush=True)

    time.sleep(2)