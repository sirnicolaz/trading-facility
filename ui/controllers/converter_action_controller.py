import npyscreen
import re
from controllers.conversion_manager import convert
from ui.helpers.command_line_parsing import parse_conversion_command


class ConvertedActionController(npyscreen.ActionControllerSimple):
    def __init__(self, *args, **kwargs):
        super(ConvertedActionController, self).__init__(*args, **kwargs)

        self.add_action(ident=".*=", function=self.convert, live=True)

    def convert(self, command_line, control_widget_proxy, live=True):
        try:
            value, from_currency, to_currency = parse_conversion_command(command_line)
            result = convert(value, from_currency, to_currency)
            control_widget_proxy.value = re.sub(r"\s*=.*",  " -> %.10f" % result, command_line)
        except ValueError:
            control_widget_proxy.value = re.sub(r"\s*=.*", " -> bad input", command_line)