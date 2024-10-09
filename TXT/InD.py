import os

class Baca:
    def baca_file(lokasi_file):
        try:
            with open(lokasi_file, 'r') as file:
                data = file.read().strip()
            return data
        except FileNotFoundError:
            print(f"File {lokasi_file} tidak ditemukan.")
            return None

class Up:
    def tambah_data(nama_file):
        try:
            with open(nama_file, 'r') as file:
                lines = file.readlines()
                last_id = max(int(line.split(':')[0]) for line in lines[1:] if ':' in line)
        except FileNotFoundError:   
            last_id = 0

        value = input("Masukkan nama data: ")
        new_id = last_id + 1

        with open(nama_file, 'a') as file:
            if not lines[-1].endswith('\n'):
                file.write('\n')
            file.write(f"{new_id}:{value}\n")
        print(f"Data '{new_id}:{value}' berhasil ditambahkan ke {nama_file}")

# Fungsi untuk mendapatkan ID terakhir dari file
    def baca_id_terakhir(nama_file):
        if not os.path.exists(nama_file):
            return 0
        with open(nama_file, 'r') as file:
            lines = file.readlines()
            if len(lines) > 1:
                last_line = lines[-1].strip()
                if ':' in last_line:
                    return int(last_line.split(':')[0])
        return 0
    
    def parsing_dictionary(data):
        dict_result = {}
        lines = data.splitlines()

        for line in lines[1:]:  # Lewati header
            parts = line.split(':')

            # Jika panjangnya 2, itu adalah format untuk Warna atau Kategori
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                dict_result[key] = value
            # Jika panjangnya 4, itu adalah format untuk Makanan
            elif len(parts) == 4:
                key = parts[0].strip()
                value = tuple(parts[1:])  # Buat tuple dari elemen sisanya
                dict_result[key] = value
            else:
                print(f"Data tidak valid pada baris: {line}")  # Debugging output
    
        return dict_result

class Del:
    def hapus_data(nama_file):
        if not os.path.exists(nama_file):
            print(f"File {nama_file} tidak ditemukan.")
            return

        data = Baca.baca_file(nama_file)
        if data is None:
            print(f"Gagal membaca file {nama_file}.")
            return

        data_dict = Up.parsing_dictionary(data)

        jenis_data = "item"
        if "Kategori" in nama_file.lower():
            jenis_data = "Kategori"
        elif "Warna" in nama_file.lower():
            jenis_data = "Warna"
        elif "Makanan" in nama_file.lower():
            jenis_data = "Makanan"

        print(f"Data {jenis_data} yang tersedia:")
        for id_item, info_item in data_dict.items():
            print(f"ID: {id_item}, {jenis_data.capitalize()}: {info_item}")

        id_hapus = input(f"Masukkan ID {jenis_data} yang akan dihapus: ")

        if id_hapus not in data_dict:
            print(f"ID {id_hapus} tidak ditemukan.")
            return

        del data_dict[id_hapus]

        print(f"Data {jenis_data} dengan ID {id_hapus} berhasil dihapus.")

class Makanan:
    def Data_Makanan():
        file_output = 'Data_Makanan.txt'
    
        Warna_data = Baca.baca_file('Data_Warna.txt')
        if Warna_data is None:
            print("File data Warna tidak ditemukan.")
            return
        Warna_dict = Up.parsing_dictionary(Warna_data)  # Parsing warna

        Kategori_data = Baca.baca_file('Data_Kategori.txt')
        if Kategori_data is None:
            print("File data Kategori tidak ditemukan.")
            return
        Kategori_dict = Up.parsing_dictionary(Kategori_data)  # Parsing kategori

        id_terakhir = Up.baca_id_terakhir(file_output)

        while True:
            try:
                id_Kategori = input("Masukkan nomor Kategori: ")
                if id_Kategori not in Kategori_dict:
                    print("Nomor Kategori tidak valid. Silakan coba lagi.")
                    continue
            
                id_Warna = input("Masukkan nomor Warna: ")
                if id_Warna not in Warna_dict:
                    print("Nomor Warna tidak valid. Silakan coba lagi.")
                    continue
            
                # Dapatkan nama makanan dari input
                nama_makanan = input("Masukkan nama makanan: ")

                # Hitung ID makanan berikutnya
                id_makanan = id_terakhir + 1
            
                # Simpan hasil ke file dengan format yang benar
                mode = 'a' if os.path.exists(file_output) else 'w'
                with open(file_output, mode) as file:
                    if mode == 'w':
                        file.write("ID_DATA\n")  # Menulis header jika file baru
                    file.write(f"{id_makanan}:{nama_makanan}:{id_Kategori}:{id_Warna}\n")
            
                print(f"Data makanan berhasil disimpan dengan ID: {id_makanan}")
                break  # Keluar dari loop jika berhasil
            
            except ValueError:
                print("Input tidak valid. Harap masukkan angka.")
