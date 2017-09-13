import re


def parse_conversion_command(command):
    regex = re.compile("(.*\d) (\w*) to (\w*)")
    match = regex.match(command)

    if match is None:
        raise ValueError("Unrecognized command")

    groups = match.group
    value = float(groups(1))
    from_currency = groups(2)
    to_currency = groups(3)

    return value, from_currency, to_currency