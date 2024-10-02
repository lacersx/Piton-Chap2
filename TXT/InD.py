def baca_file(lokasi_file):
    try:
        with open(lokasi_file, 'r')as  file:
            data = file.read().strip()
        return data
    except FileNotFoundError:
        return None

def identifikasi_format(data):
    if ':' in data:
        return 'dictionary'
    return None

def parsing_dictionary(data):
    dictionary = {}
    if ':' in data:
        pairs = data.split('\n')
        for pair in pairs:
            key, value = pair.split(':')
            dictionary[key.strip()] = value.strip()
    return dictionary
