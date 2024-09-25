def baca_file(lokasi_file):
    try:
        with open(lokasi_file, 'r')as  file:
            data = file.read().strip()
        return data

def identifikasi_format(data):
    if ',' in data or '\n' in data:
        return 'array'
    elif '=>' in data or ':' in data:
        return 'dictionary'
    return None
