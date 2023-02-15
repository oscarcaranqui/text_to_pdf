import re

def extract_information(message: str) -> list:
    dictionary = {}
    pool_motor, result = [], []
    flag = False
    ip = message.split('\n')[0]
    sector_pool_motor = message.split('\n')[4:]
    sector, ip_gw = str(), str()

    for item in sector_pool_motor:
        match = re.match(r'\s*(\w+)\s+(\w+)\s+(\d+)\s*', item)
        if match:
            sector = match.group(1)
            piscina = match.group(2)
            motor = match.group(3)
            pool_motor.append([piscina, int(motor)])
            flag = True

    if flag:
        for key, value in pool_motor:
            if key in dictionary:
                dictionary[key].append(value)
            else:
                dictionary[key] = [value]

        match = re.match(r"\bIP: (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2})\b", ip)

        if match:
            ip_gw = match.group(1)
            return [True, dict(sorted(dictionary.items())), ip_gw, sector]
        else:
            return [False]


    else:
        result = [False]

    return result