# Meminta nama file dari pengguna
nama_file = input("Masukkan nama file (misalnya data.txt): ")

try:
    with open(nama_file, 'r') as file:
        # Membaca semua baris dan memisahkan berdasarkan koma
        array_data = [item.strip() for line in file for item in line.split(',')]
    
    # Menampilkan data yang dibaca
    if array_data:
        print("Data yang dibaca dari file:")
        print(array_data)

except FileNotFoundError:
    print(f"File '{nama_file}' tidak ditemukan.") 
