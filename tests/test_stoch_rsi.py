import random
from unittest import TestCase
from unittest.mock import patch

from technical_analysis.stochrsi import stoch_rsi, is_overbought, is_overssold


class TestStochRsi(TestCase):
    @patch("monitoring.stochrsi_strategy.historical_api.get_historical_hour")
    def test_stoch_rsi(self, mock_get_historical_hour):
        mock_get_historical_hour.return_value = [{'close': random.uniform(0.5, 1.9)} for _ in range(101)]
        market = "BTC-QTUM"

        result = stoch_rsi(market)

        self.assertEqual(101, len(result[0]))
        self.assertEqual(101, len(result[1]))

    @patch("monitoring.stochrsi_strategy.historical_api.get_historical_hour")
    def test_stoch_rsi_currencies(self, mock_get_historical_hour):
        mock_get_historical_hour.return_value = [{'close': 0.1} for i in range(0,101)]
        market = "BTC-QTUM"

        stoch_rsi(market)
        mock_get_historical_hour.assert_called_with("QTUM", "BTC")

    def test_is_oversold(self):
        values = [[50, 40, 20], [70, 80, 19]]

        result = is_overssold(values)

        self.assertTrue(result)

    def test_is_not_oversold(self):
        values = [[50, 15, 40], [70, 10, 19]]

        result = is_overssold(values)

        self.assertFalse(result)

    def test_is_not_overbought(self):
        values = [[50,40,20],[70,80,19]]

        result = is_overbought(values)

        self.assertFalse(result)

    def test_is_overbought(self):
        values = [[50,40,90],[70,80,80]]

        result = is_overbought(values)

        self.assertTrue(result)
