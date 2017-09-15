def percentage_gain(new_value, old_value):
    if old_value == 0:
        return 0

    return (new_value * 100.0 / old_value) - 100.0
