
def parse_callback_data(data, expected_parts=2):
    return data.split("_", expected_parts - 1)
