def tambah_data(nama_file):
    data_dict = {}
    max_id = 0

    # Membaca file dan mencari ID yang tersedia
    try:
        with open(nama_file, 'r') as file:
            lines = file.readlines()
            for line in lines[1:]:  # Mulai dari baris kedua (setelah header)
                if ':' in line:
                    id, value = line.strip().split(':', 1)
                    id = int(id)
                    data_dict[id] = value
                    max_id = max(max_id, id)
    except FileNotFoundError:
        print(f"File {nama_file} tidak ditemukan. Akan dibuat file baru.")

    # Meminta input dari pengguna
    value = input("Masukkan nama data: ")

    # Mencari ID kosong pertama atau menggunakan ID baru
    new_id = next((i for i in range(1, max_id + 2) if i not in data_dict), max_id + 1)

    # Menambahkan data baru ke dictionary
    data_dict[new_id] = value

    # Menulis kembali seluruh data ke file
    with open(nama_file, 'w') as file:
        file.write("ID_DATA\n")  # Tulis header
        for id, val in sorted(data_dict.items()):
            file.write(f"{id}:{val}\n")

    print(f"Data '{new_id}:{value}' berhasil ditambahkan ke {nama_file}")
    print("Operasi selesai.")  # Tambahan penutup di dalam fungsi
    return f"{new_id}:{value}"
