import time
import threading

def timer(hours, minutes, seconds):
    total_seconds = hours * 3600 + minutes * 60 + seconds
    time.sleep(total_seconds)
    print("Done")

# Example usage: Set the timer for 1 hour, 30 minutes, and 45 seconds
timer_thread = threading.Thread(target=timer, args=(0, 0, 6))
timer_thread.start()

print("timer has started")
time.sleep(2)
print("a")
