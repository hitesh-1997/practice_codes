import unittest
from unittest.mock import patch
from barber_shop import BarberShop

class TestBarberShop(unittest.TestCase):

    def setUp(self):
        self.shop = BarberShop()

    @patch('barber_shop.time.sleep', return_value=None)
    def test_cut_hair_barber(self, patched_time_sleep):
        # Simulate barber cutting hair without real sleep to speed up test
        with patch('barber_shop.threading.Thread.start') as mock_thread_start:
            barber_thread = threading.Thread(target=self.shop.cut_hair_barber, daemon=True)
            barber_thread.start()
            mock_thread_start.assert_called_once()

        # Simulate customer getting a haircut
        self.shop._barber.release() # This simulates a customer sitting in the barber chair by releasing the semaphore
        self.shop._current_customer_seated = 5

        with patch('barber_shop.print') as mock_print:
            # Allow some time for the barber to "cut hair"
            patched_time_sleep.assert_not_called()  # Ensure that the sleep is patched correctly

            # Assert that the print function has been called with the correct message
            self.assertTrue(any("Cutting Hair for customer: 5" in call_args[0][0] for call_args in mock_print.call_args_list))

            # Lastly, check if the chair semaphore is released after a haircut, allowing the next customer to sit
            self.assertTrue(self.shop._chair._value == 1)  # Semaphore released, value should be 1


if __name__ == '__main__':
    unittest.main()
