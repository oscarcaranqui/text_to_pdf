import re


def extract_information(message: str) -> dict:
    dictionary = {}
    pool_motor = []
    sector_pool_motor = message.split('\n')[4:]

    for item in sector_pool_motor:
        match = re.match(r'\s*(\w+)\s+(\w+)\s+(\d+)\s*', item)

        if match:
            piscina = match.group(2)
            motor = match.group(3)
            pool_motor.append([piscina, int(motor)])

    for key, value in pool_motor:
        if key in dictionary:
            dictionary[key].append(value)
        else:
            dictionary[key] = [value]

    result = dict(sorted(dictionary.items()))
    return result