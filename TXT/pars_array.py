def parsing_array(data):
    # Fungsi untuk memparsing data Array
    if ',' in data:
        array = data.split(',')
    elif '\n' in data:
        array = data.split('\n')
    else:
        array = [data] 
        
    array = [item.strip() for item in array]
    return array
