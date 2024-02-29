import unittest
from unittest.mock import patch
from deferred_callback import DeferredCallback
import time

class TestDeferredCallback(unittest.TestCase):

    def setUp(self):
        self.dc = DeferredCallback()

    @patch('time.time', side_effect=[1, 2, 3])  # Mocking time.time() to return deterministic values.
    def test_execute_callback(self, mock_time):
        # Adding callbacks with specific IDs and timeouts such that
        # they should be executed immediately when execute_callback is called.
        self.dc.add_callback('Task1', 1)  # This should time out at time 2
        self.dc.add_callback('Task2', 5)  # This should not time out at time 2
        
        # Mocking print to verify execution behavior.
        with patch('builtins.print') as mock_print:
            def execute_and_stop():
                self.dc.execute_callback()
                self.dc.cv.acquire()
                self.dc.cv.notify()  # To stop the while loop in execute_callback.
                self.dc.cv.release()

            t = threading.Thread(target=execute_and_stop)
            t.start()
            t.join()

            # Verifying that Task1 gets executed and Task2 does not within the mocked time frame.
            mock_print.assert_any_call("Executing task: Task1, time diff: 1", flush=True)
            self.assertNotIn(call("Executing task: Task2, time diff: -2", flush=True), mock_print.mock_calls)

if __name__ == '__main__':
    unittest.main()
