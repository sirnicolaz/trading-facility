from unittest import TestCase
from unittest.mock import patch

from technical_analysis.macd import get_macd, is_trend_down
from tests.resources.qtumbtc import QTUM_SAMPLE, QTUM_MACD


class TestMacd(TestCase):
    @patch("technical_analysis.macd.historical_api")
    def test_get_macd(self, mock_historical_api):
        mock_data = QTUM_SAMPLE
        mock_historical_api.get_historical_hour.return_value = mock_data

        values = get_macd("BTC-QTUM", 4)

        expected_function_length = 201
        self.assertEqual(3, len(values))
        self.assertEqual(expected_function_length, len(values[0]))
        self.assertEqual(expected_function_length, len(values[1]))
        self.assertEqual(expected_function_length, len(values[2]))

    def test_is_trend_down(self):
        mock_data = QTUM_MACD

        result = is_trend_down(mock_data[0], mock_data[1])

        self.assertTrue(result)