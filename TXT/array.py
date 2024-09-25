# Membuat list kosong untuk menyimpan nama daerah
daerah = []

# Meminta input daerah dari pengguna
for _ in range(int(input("Berapa banyak daerah? "))):
    daerah.append(input("Masukkan nama daerah: "))

# Menampilkan daftar daerah
print("\nDaftar daerah:", daerah)

# Menampilkan pilihan untuk menambah atau menghapus daerah
while True:
    print("\nPilih opsi:")
    print("1. Tambah daerah")
    print("2. Hapus daerah")
    print("3. Keluar")
    pilihan = input("Masukkan pilihan (1/2/3): ")

    if pilihan == "1":
        daerah.append(input("Masukkan nama daerah baru: "))
        print("Daftar setelah penambahan:", daerah)

    elif pilihan == "2":
        hapus = input("Masukkan nama daerah yang ingin dihapus: ")
        if hapus in daerah:
            daerah.remove(hapus)
            print("Daftar setelah penghapusan:", daerah)
        else:
            print(f"Nama daerah {hapus} tidak ditemukan.")
    
    elif pilihan == "3":
        print("Keluar dari program.")
        break

    else:
        print("Pilihan tidak valid, coba lagi.")
