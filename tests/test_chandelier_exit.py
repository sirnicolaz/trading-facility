from unittest import TestCase
from technical_analysis import chandelier_exit
from tests.resources.zeceur import ZECEUR_HISTORY


class TestChandelierExit(TestCase):
    def test_get_long_chandelier_exit(self):

        result = chandelier_exit.get_long_chandelier_exit(ZECEUR_HISTORY)

        self.assertEqual(165.20688574976617, result)


    def test_get_long_chandelier_exit_custom_period(self):

        result = chandelier_exit.get_long_chandelier_exit(ZECEUR_HISTORY, period=30)

        self.assertEqual(165.77224134040961, result)


    def test_get_long_chandelier_exit_custom_coefficient(self):

        result = chandelier_exit.get_long_chandelier_exit(ZECEUR_HISTORY, coefficient=5)

        self.assertEqual(152.0114762496103, result)
