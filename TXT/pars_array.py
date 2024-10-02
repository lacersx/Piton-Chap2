def hapus_data(nama_file):
    if not os.path.exists(nama_file):
        print(f"File {nama_file} tidak ditemukan.")
        return

    data = baca_file(nama_file)
    if data is None:
        print(f"Gagal membaca file {nama_file}.")
        return

    data_dict = parse_dictionary(data)

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

    tulis_kembali_data(nama_file, data_dict, jenis_data)

    print(f"Data {jenis_data} dengan ID {id_hapus} berhasil dihapus.")
