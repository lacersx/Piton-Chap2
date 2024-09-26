#full code dibawah
def baca_file(lokasi_file):
    try:
        with open(lokasi_file, 'r')as  file:
            data = file.read().strip()
        return data
    except FileNotFoundError:
        print(f"File'{lokasi_file}'tidak ditemukan. Silahkan masukan file yang benar")
    return None

def identifikasi_format(data):
    if ',' in data or '\n' in data:
        return 'array'
    elif '=>' in data or ':' in data:
        return 'dictionary'
    return None

def parsing_dictionary(data):
    dictionary = {}
    if '=>' in data:
        pairs = data.split(',')
        for pair in pairs:
            key, value = pair.split('=>')
            dictionary[key.strip()] = value.strip()
    elif ':' in data:
        pairs = data.split(';')
        for pair in pairs:
            key, value = pair.split(':')
            dictionary[key.strip()] = value.strip()
    return dictionary
