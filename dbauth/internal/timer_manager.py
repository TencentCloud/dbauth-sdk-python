import logging
import threading

from dbauth.internal.constants import Constants


class TimerManager:
    """TimerManager is a utility class that provides methods for managing timer tasks."""

    def __init__(self):
        self.timer_map = {}
        self.lock = threading.Lock()
        self.log = logging.getLogger(__name__)

    def save_timer(self, key, delay, task):
        """Saves a timer task that runs after a specified interval."""
        if not key:
            self.log.warning("Key is empty, skipping timer creation.")
            return

        if delay <= 0 or delay > Constants.MAX_DELAY:
            self.log.warning(f"Invalid delay: {delay}, skipping timer creation.")
            return

        with self.lock:
            timer = threading.Timer(delay / 1000, task)
            timer.daemon = True  # Set the timer thread as a daemon
            timer.start()

            # If a timer with the same key exists, cancel it and remove it from the map
            if key in self.timer_map:
                self.timer_map[key].cancel()
                del self.timer_map[key]

            self.timer_map[key] = timer

    def cancel_timer(self, key):
        with self.lock:
            if key in self.timer_map:
                self.timer_map[key].cancel()
                del self.timer_map[key]
                self.log.info(f"Timer cancelled for key: {key}")
            else:
                self.log.warning(f"No timer found for key: {key}")

    def shutdown(self):
        with self.lock:
            for timer in self.timer_map.values():
                timer.cancel()
            self.timer_map.clear()
        self.log.info("TimerManager shutdown complete.")
