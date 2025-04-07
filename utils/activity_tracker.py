import time
import threading
from pynput import keyboard, mouse

class ActivityTracker:
    def __init__(self, timeout=300, callback=None):
        self.timeout = timeout
        self.callback = callback
        self.last_activity_time = time.time()
        self.timer_thread = None
        self.active = False

        self.keyboard_listener = keyboard.Listener(on_press=self.reset_timer)
        self.mouse_listener = mouse.Listener(on_click=self.reset_timer, on_move=self.reset_timer,on_scroll=self.reset_timer)

    
    def start_tracking(self):
        if not self.active:
            self.active = True
            self.last_activity_time = time.time()
            self.timer_thread = threading.Thread(target=self.monitor_inactivity, daemon=True)
            self.timer_thread.start()

            self.keyboard_listener.start()
            self.mouse_listener.start()
            print("[ActivityTracker] Tracking started...")

    def stop_tracking(self):
        self.active = False
        self.keyboard_listener.stop()
        self.mouse_listener.stop()
        print("[ActivityTracker] Tracking stopped.")

    def reset_timer(self, *args):
        self.last_activity_time = time.time()
    
    def monitor_inactivity(self):
        while self.active:
            if time.time() - self.last_activity_time > self.timeout:
                if self.callback:
                    self.callback()
                self.active = False
                break
            time.sleep(1)