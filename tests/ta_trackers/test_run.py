from unittest import TestCase
from unittest.mock import patch
from ta_trackers.rsi import run


class TestRSI(TestCase):
    @patch("technical_analysis.stochrsi.historical_api.get_historical_hour")
    def test_run(self, mock_get_historical_hour):
        mock_get_historical_hour.return_value = [{'close': float(value)} for value in range(101)]
        result = run(*["QTUM"])

        self.assertEqual((100.0, "rsi_QTUM"), result)

    @patch("technical_analysis.stochrsi.historical_api.get_historical_hour")
    def test_run_with_aggregate(self, mock_get_historical_hour):
        mock_get_historical_hour.return_value = [{'close': float(value)} for value in range(101)]
        run(*["QTUM", 42])

        mock_get_historical_hour.assert_called_with('QTUM', 'BTC', limit=200, aggregate=42)