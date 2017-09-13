from unittest import TestCase
from ui.helpers.command_line_parsing import parse_conversion_command


class TestCommandLineParsing(TestCase):
    def test_parse_conversion_command_value(self):
        test_string = "3.45 btc to eur ="

        result, _, _ = parse_conversion_command(test_string)

        self.assertEqual(3.45, result)

    def test_parse_conversion_command_from_currency(self):
        test_string = "3.45 btc to eur ="

        _, result, _ = parse_conversion_command(test_string)

        self.assertEqual("btc", result)

    def test_parse_conversion_command_to_currency(self):
        test_string = "3.45 btc to eur ="

        _, _, result = parse_conversion_command(test_string)

        self.assertEqual("eur", result)

    def test_parse_conversion_command_bad_string(self):
        test_string = "dio cane ="

        with self.assertRaises(ValueError):
            parse_conversion_command(test_string)

