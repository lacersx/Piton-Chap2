def main():
    lokasi_file = input("Masukkan nama file: ")

    # Baca file
    data = baca_file(lokasi_file)
    if data is None:
        return

    # Identifikasi format
    format_file = identifikasi_format(data)
    
    if format_file == 'array':
        array = parsing_array(data)
        print("Isi file sebagai Array:", array)
    elif format_file == 'dictionary':
        dictionary = parsing_dictionary(data)
        print("Isi file sebagai Dictionary:", dictionary)
    else:
        print("Format file tidak dikenali.")

if __name__ == "__main__":
    main()
