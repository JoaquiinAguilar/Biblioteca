import os
import django
import time
from django.core.management import call_command

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cubicle_project.settings')
django.setup()

def run_release_cubicles_periodically(interval_seconds=60):
    print(f"Starting cubicle release scheduler. Running every {interval_seconds} seconds.")
    while True:
        try:
            print(f"[{time.ctime()}] Running release_expired_cubicles command...")
            call_command('release_expired_cubicles')
        except Exception as e:
            print(f"[{time.ctime()}] Error running command: {e}")
        time.sleep(interval_seconds)

if __name__ == "__main__":
    run_release_cubicles_periodically()
