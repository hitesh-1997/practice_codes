import unittest
from unittest.mock import patch
from barber_shop import BarberShop

class TestBarberShop(unittest.TestCase):

    def setUp(self):
        self.shop = BarberShop()

    @patch('barber_shop.time.sleep', return_value=None)
    def test_cut_hair_barber(self, mocked_time_sleep):
        # Simulate the barber cutting hair without actually waiting
        with patch('threading.Semaphore.acquire'), patch('threading.Semaphore.release'):
            # Mock print to check the output later
            with patch('builtins.print') as mocked_print:
                # Assuming we simulate that a customer with ID 1 is seated
                self.shop._current_customer_seated = 1
                # We should also simulate that the _barber semaphore
                # has been released by a previous action
                self.shop._barber.release()
                # Run the barber function in a separate thread to allow our test to continue
                barber_thread = threading.Thread(target=self.shop.cut_hair_barber, daemon=True)
                barber_thread.start()
                # Give some time for the thread to run
                threading.Event().wait(0.1)
                # Check if the print output contains the expected output of cutting hair for customer 1
                mocked_print.assert_called_with("Cutting Hair for customer: 1")
                # To ensure our daemon thread does not block the test, we simulate stopping the while loop
                self.shop._barber.acquire(blocking=False)  # This simulates stopping the loop by not having an acquired barber semaphore

if __name__ == '__main__':
    unittest.main()
