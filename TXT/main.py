from InD import baca_file, parsing_dictionary, Data_Makanan
from up import tambah_data
from pars_array import hapus_data

def main():
    # Muat data dari file saat aplikasi dimulai
    while True:
        print("\n==== Menu Utama ====")
        print("1. Lihat Data")
        print("2. Tambah warna dan Kategori")
        print("3. Hapus Data")
        print("4. Buat Data Makanan")
        print("5. Keluar Aplikasi")
        pilihan = input("Pilih opsi (1/2/3/4/5): ")

        if pilihan == '1':
            print("1. Lihat Data Warna")
            print("2. Lihat Data Kategori")
            print("3. Lihat Data Makanan")
            pilihan = input("Pilihan : ")

            if pilihan == '1':
                isi = baca_file(lokasi_file="Data_Warna.txt")
                if isi is not None and isi.strip():
                    data_dict = parsing_dictionary(isi)
                    print("\nData yang dibaca adalah Dictionary:")
                    for key, value in data_dict.items():
                        print(f"{key}: {value}")
                else:
                    print("File tidak ditemukan atau kosong.")

            elif pilihan == '2':
                isi = baca_file(lokasi_file="Data_Kategori.txt")
                if isi is not None and isi.strip():
                    data_dict = parsing_dictionary(isi)
                    print("\nData yang dibaca adalah Dictionary:")
                    for key, value in data_dict.items():
                        print(f"{key}: {value}")
                else:
                    print("File tidak ditemukan atau kosong.")

            elif pilihan == '3':  # Kode untuk melihat data makanan
                isi = baca_file(lokasi_file="Data_Makanan.txt")
                if isi is not None and isi.strip():
                    data_dict = parsing_dictionary(isi)
                    print("\nData yang dibaca adalah Dictionary:")
                    for key, value in data_dict.items():
                        # Mengeluarkan tuple sebagai string dengan format yang diinginkan
                        print(f"{key}: {', '.join(value)}")
                else:
                    print("File tidak ditemukan atau kosong.")

        
        elif pilihan == '2':
            print("Pilih File yang ingin di tambah : ")
            print("1. Data Warna")
            print("2. Data Kategori")
            pilihan = input("Pilihan : ")
            if pilihan == '1':
                tambah_data(nama_file="Data_Warna.txt")
                 
            elif pilihan == '2':
                tambah_data(nama_file="Data_Kategori.txt")   

        elif pilihan == '3':
            print("Pilih File yang ingin di hapus : ")
            print("1. Data Warna")
            print("2. Data Kategori")
            print("3. Data Makanan")
            pilihan = input("Pilihan : ")
            if pilihan == '1':
                hapus_data(nama_file="Data_Warna.txt")
                 
            elif pilihan == '2':
                hapus_data(nama_file="Data_Kategori.txt")

            elif pilihan == '3':
                hapus_data(nama_file="Data_Makanan.txt")

        elif pilihan == '4':
            print("Data Makanan: ")  
            Data_Makanan()

        elif pilihan == '5':
            print("Terima kasih telah menggunakan aplikasi!") 
            break

        else:
            print("Pilihan tidak valid, silakan coba lagi.")



if __name__ == "__main__":
    main()