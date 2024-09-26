def parsing_array(data):
    # Fungsi untuk memparsing data Array
    if ',' in data:
        array = data.split(',')
    else:
        array = data.split('\n')
    
    return array
