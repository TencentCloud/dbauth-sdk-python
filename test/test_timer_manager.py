import threading
import unittest
from unittest.mock import MagicMock

from dbauth.internal.timer_manager import TimerManager


class TestTimerManager(unittest.TestCase):

    def setUp(self):
        self.timer_manager = TimerManager()

    def tearDown(self):
        self.timer_manager.shutdown()

    def test_saves_timer_with_valid_key_and_delay(self):
        mock_task = MagicMock()
        self.timer_manager.save_timer("test_key", 1000, mock_task)
        self.assertIn("test_key", self.timer_manager.timer_map)

    def test_does_not_save_timer_with_empty_key(self):
        mock_task = MagicMock()
        self.timer_manager.save_timer("", 1000, mock_task)
        self.assertNotIn("", self.timer_manager.timer_map)

    def test_does_not_save_timer_with_none_key(self):
        mock_task = MagicMock()
        self.timer_manager.save_timer(None, 1000, mock_task)
        self.assertNotIn("", self.timer_manager.timer_map)

    def test_does_not_save_timer_with_invalid_delay_min(self):
        mock_task = MagicMock()
        self.timer_manager.save_timer("test_key", -1, mock_task)
        self.assertNotIn("test_key", self.timer_manager.timer_map)

    def test_does_not_save_timer_with_invalid_delay_max(self):
        mock_task = MagicMock()
        self.timer_manager.save_timer("test_key", 24 * 60 * 60 * 1000 + 1, mock_task)
        self.assertNotIn("test_key", self.timer_manager.timer_map)

    def test_cancels_existing_timer(self):
        mock_task = MagicMock()
        self.timer_manager.save_timer("test_key", 1000, mock_task)
        self.timer_manager.cancel_timer("test_key")
        self.assertNotIn("test_key", self.timer_manager.timer_map)

    def test_does_not_cancel_nonexistent_timer(self):
        with self.assertLogs(self.timer_manager.log, level='WARNING') as log:
            self.timer_manager.cancel_timer("nonexistent_key")
            self.assertIn("No timer found for key: nonexistent_key", log.output[0])

    def test_executes_task_after_delay(self):
        mock_task = MagicMock()
        event = threading.Event()

        def task_wrapper():
            mock_task()
            event.set()

        self.timer_manager.save_timer("test_key", 1000, task_wrapper)
        # repeat the task
        self.timer_manager.save_timer("test_key", 1000, task_wrapper)
        event.wait(2)  # Wait for the task to complete
        mock_task.assert_called_once()

    def test_timer_manager(self):
        counter = 0
        event = threading.Event()

        def increment_counter():
            nonlocal counter
            counter += 1
            if counter == 2:
                event.set()
            self.timer_manager.save_timer("key", 1000, increment_counter)

        self.timer_manager.save_timer("key", 1000, increment_counter)
        event.wait(3)  # Wait for the task to complete
        self.assertEqual(2, counter)


if __name__ == '__main__':
    unittest.main()
