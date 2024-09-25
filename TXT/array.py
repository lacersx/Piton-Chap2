try:
    with open('data.txt', 'r') as file:
        # Membaca semua baris dan memisahkan berdasarkan koma
        array_data = [item.strip() for line in file for item in line.split(',')]
    
    # Menampilkan data yang dibaca
    if array_data:
        print("Data yang dibaca dari file:")
        print(array_data)

except FileNotFoundError:
    print(f"File '{data.txt}' tidak ditemukan.")
