import subprocess
import os
import time
import signal

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
testproject_dir = os.path.join(current_dir, "testproject")
screenshots_dir = os.path.join(testproject_dir, "screenshots")

# Ensure the screenshots directory exists
os.makedirs(testproject_dir, exist_ok=True)

# Run migrations
subprocess.run(["./manage.py", "migrate"], cwd=testproject_dir, check=True)

# Start the Django development server
server_process = subprocess.Popen(
    ["./manage.py", "runserver", "8001"],
    cwd=testproject_dir,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

time.sleep(1)

try:
    # Take a screenshot using shot-scraper
    subprocess.run([
        "shot-scraper",
        "multi",
        "shots.yml",
    ], check=True)
finally:
    # Terminate the server process
    server_process.send_signal(signal.SIGTERM)
    server_process.wait()

print("Screenshot taken and server terminated.")
