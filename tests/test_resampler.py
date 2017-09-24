from unittest import TestCase
from technical_analysis.resampler import resample


class TestResampler(TestCase):
    def test_resample(self):
        samples = [
        { # this first sample should not be considered
                "high": 45,
                "low": 44,
                "volumefrom": 45,
                "volumeto": 55,
                "close": 44
        },{
            "high": 4,
            "low": 3,
            "volumefrom": 2,
            "volumeto": 3,
            "close": 3.5
        },{
            "high": 5,
            "low": 4,
            "volumefrom": 3,
            "volumeto": 4,
            "close": 4.5
        },{
            "high": 6,
            "low": 5,
            "volumefrom": 5,
            "volumeto": 6,
            "close": 5.5
        },{
            "high": 5,
            "low": 4,
            "volumefrom": 6,
            "volumeto": 5,
            "close": 4
        }]

        result = resample(samples, 2)
        result_0 = result[0]
        result_1 = result[1]

        self.assertEqual(5, result_0["high"])
        self.assertEqual(3, result_0["low"])
        self.assertEqual(2, result_0["volumefrom"])
        self.assertEqual(4, result_0["volumeto"])
        self.assertEqual(4.5, result_0["close"])

        self.assertEqual(6, result_1["high"])
        self.assertEqual(4, result_1["low"])
        self.assertEqual(5, result_1["volumefrom"])
        self.assertEqual(5, result_1["volumeto"])
        self.assertEqual(4, result_1["close"])
