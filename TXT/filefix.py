import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

# Koneksi ke database
conn = sqlite3.connect('makanan.db')
c = conn.cursor()

# Drop the tables if they exist and create them again
c.execute('''DROP TABLE IF EXISTS makanan''')
c.execute('''DROP TABLE IF EXISTS kategori''')
c.execute('''DROP TABLE IF EXISTS warna''')

c.execute('''CREATE TABLE IF NOT EXISTS makanan (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                nama TEXT, 
                kategori TEXT, 
                warna TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS kategori (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                nama TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS warna (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                nama TEXT)''')

# Inisialisasi data kategori
kategori_data = [
    (1, 'Protein'),
    (2, 'Mineral'),
    (3, 'Snack'),
    (4, 'Karbohidrat'),
    (5, 'Segar')
]

# Inisialisasi data warna
warna_data = [
    (1, 'Kuning'),
    (2, 'Hijau'),
    (3, 'Merah'),
    (4, 'Biru')
]

# Inisialisasi data makanan
makanan_data = [
    (1, 'Chiki Pedas', 'Snack', 'Hijau'),
    (2, 'Sayuran', 'Mineral', 'Hijau'),
    (3, 'Kentang', 'Protein', 'Merah'),
    (4, 'Mie', 'Snack', 'Hijau')
]

# Masukkan data kategori dan warna ke database
c.executemany("INSERT INTO kategori (id, nama) VALUES (?, ?)", kategori_data)
c.executemany("INSERT INTO warna (id, nama) VALUES (?, ?)", warna_data)

# Masukkan data makanan ke database
c.executemany("INSERT INTO makanan (id, nama, kategori, warna) VALUES (?, ?, ?, ?)", makanan_data)

conn.commit()

data_makanan = {'nama': '', 'kategori': '', 'warna': ''}
selected_id = None

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
    def parsing_dictionary(data):
        dict_result = {}
        lines = data.splitlines()

        for line in lines[1:]:
            parts = line.split(':')
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                dict_result[key] = value
            elif len(parts) == 4:
                key = parts[0].strip()
                value = tuple(parts[1:])
                dict_result[key] = value
            else:
                print(f"Data tidak valid pada baris: {line}")
    
        return dict_result

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

        print("Data yang tersedia:")
        for id_item, info_item in data_dict.items():
            print(f"ID: {id_item}, Info: {info_item}")

        id_hapus = input("Masukkan ID yang akan dihapus: ")

        if id_hapus not in data_dict:
            print(f"ID {id_hapus} tidak ditemukan.")
            return

        del data_dict[id_hapus]
        print(f"Data dengan ID {id_hapus} berhasil dihapus.")

# Fungsi utama: tambah, edit, hapus, dan tampilkan data
def simpan_data():
    global data_makanan
    if all(data_makanan.values()):
        if selected_id:
            c.execute("UPDATE makanan SET nama=?, kategori=?, warna=? WHERE id=?", 
                      (data_makanan['nama'], data_makanan['kategori'], data_makanan['warna'], selected_id))
        else:
            c.execute("INSERT INTO makanan (nama, kategori, warna) VALUES (?, ?, ?)", 
                      (data_makanan['nama'], data_makanan['kategori'], data_makanan['warna']))
        conn.commit()
        clear_data()
        tampilkan_data()
    else:
        messagebox.showwarning("Input Error", "Lengkapi semua data!")

def hapus_data():
    try:
        selected = listbox.curselection()[0]
        c.execute("DELETE FROM makanan WHERE id=?", (listbox.get(selected).split()[0],))
        conn.commit()
        tampilkan_data()
    except IndexError:
        messagebox.showwarning("Pilih Data", "Pilih data yang ingin dihapus!")

def edit_data():
    global selected_id
    try:
        selected = listbox.curselection()[0]
        selected_id = listbox.get(selected).split()[0]
        c.execute("SELECT * FROM makanan WHERE id=?", (selected_id,))
        row = c.fetchone()
        entry_nama.delete(0, tk.END)
        entry_kategori.delete(0, tk.END)
        entry_warna.delete(0, tk.END)
        entry_nama.insert(0, row[1])
        entry_kategori.insert(0, row[2])
        entry_warna.insert(0, row[3])
        switch_page(halaman_nama)
    except IndexError:
        messagebox.showwarning("Pilih Data", "Pilih data yang ingin diedit!")

def tampilkan_data():
    listbox.delete(0, tk.END)
    for row in c.execute("SELECT * FROM makanan"):
        listbox.insert(tk.END, f"{row[0]} - {row[1]} ({row[2]}, {row[3]})")

def simpan_input(key, entry, next_page):
    global data_makanan
    input_value = entry.get()
    if input_value:  # Check if input is not empty
        data_makanan[key] = input_value
        switch_page(next_page)
    else:
        messagebox.showwarning("Input Error", f"{key.capitalize()} tidak boleh kosong!")

def clear_data():
    global data_makanan, selected_id
    data_makanan = {'nama': '', 'kategori': '', 'warna': ''}  # Reset to initial state
    selected_id = None
    entry_nama.delete(0, tk.END)
    entry_kategori.delete(0, tk.END)
    entry_warna.delete(0, tk.END)

# Setup GUI
root = tk.Tk()
root.title("Data Makanan")
ungu = "#76608A"
putih = "#FFFFFF"

# Halaman
halaman_awal = tk.Frame(root, bg=ungu)
halaman_awal.grid(row=0, column=0, sticky='news')
halaman_nama = tk.Frame(root, bg=ungu)
halaman_nama.grid(row=0, column=0, sticky='news')
halaman_kategori = tk.Frame(root, bg=ungu)
halaman_kategori.grid(row=0, column=0, sticky='news')
halaman_warna = tk.Frame(root, bg=ungu)
halaman_warna.grid(row=0, column=0, sticky='news')
halaman_tampilkan_data = tk.Frame(root, bg=ungu)
halaman_tampilkan_data.grid(row=0, column=0, sticky='news')

# Elemen UI dengan tampilan yang lebih menarik
tk.Label(halaman_awal, text="Masukkan Detail Makanan", font=("Arial", 18, "bold"), bg=ungu, fg=putih).pack(pady=10)
tk.Button(halaman_awal, text="Masukkan Nama Makanan", command=lambda: switch_page(halaman_nama), bg=putih, width=30).pack(pady=10)

tk.Label(halaman_nama, text="Masukkan Nama Makanan", font=("Arial", 16), bg=ungu, fg=putih).pack(pady=10)
entry_nama = tk.Entry(halaman_nama, font=("Arial", 14), width=30)
entry_nama.pack(pady=10)
tk.Button(halaman_nama, text="Lanjut", command=lambda: simpan_input('nama', entry_nama, halaman_kategori), bg=putih, width=30).pack(pady=10)

tk.Label(halaman_kategori, text="Masukkan Kategori Makanan", font=("Arial", 16), bg=ungu, fg=putih).pack(pady=10)
entry_kategori = tk.Entry(halaman_kategori, font=("Arial", 14), width=30)
entry_kategori.pack(pady=10)
tk.Button(halaman_kategori, text="Lanjut", command=lambda: simpan_input('kategori', entry_kategori, halaman_warna), bg=putih, width=30).pack(pady=10)

tk.Label(halaman_warna, text="Masukkan Warna Makanan", font=("Arial", 16), bg=ungu, fg=putih).pack(pady=10)
entry_warna = tk.Entry(halaman_warna, font=("Arial", 14), width=30)
entry_warna.pack(pady=10)
tk.Button(halaman_warna, text="Lanjut", command=lambda: simpan_input('warna', entry_warna, halaman_tampilkan_data), bg=putih, width=30).pack(pady=10)

tk.Label(halaman_tampilkan_data, text="Data Makanan", font=("Arial", 18, "bold"), bg=ungu, fg=putih).pack(pady=10)
tk.Button(halaman_tampilkan_data, text="Simpan Data", command=simpan_data, bg=putih, width=30).pack(pady=10)
tk.Button(halaman_tampilkan_data, text="Tambah Data Baru", command=lambda: switch_page(halaman_nama), bg=putih, width=30).pack(pady=10)
tk.Button(halaman_tampilkan_data, text="Hapus Data", command=hapus_data, bg=putih, width=30).pack(pady=10)
tk.Button(halaman_tampilkan_data, text="Edit Data", command=edit_data, bg=putih, width=30).pack(pady=10)

listbox = tk.Listbox(halaman_tampilkan_data, font=("Arial", 14), width=50)
listbox.pack(pady=10)

def switch_page(page):
    page.tkraise()

tampilkan_data()  # Menampilkan data saat aplikasi pertama kali dijalankan
switch_page(halaman_awal)  # Mulai di halaman awal

root.mainloop()

# Tutup koneksi database saat aplikasi ditutup
conn.close()
