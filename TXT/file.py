import tkinter as tk
from tkinter import messagebox
import sqlite3

# Koneksi ke database
conn = sqlite3.connect('makanan.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS makanan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_makanan TEXT, kategori TEXT, warna TEXT
)
''')
conn.commit()

data_makanan = {}

# Fungsi tambah data
def tambah_data():
    if all(data_makanan.values()):
        c.execute("INSERT INTO makanan (nama_makanan, kategori, warna) VALUES (?, ?, ?)",
                  (data_makanan['nama'], data_makanan['kategori'], data_makanan['warna']))
        conn.commit()
        messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")
        clear_data()
        tampilkan_data()
        switch_page(halaman_awal)
    else:
        messagebox.showwarning("Input Error", "Lengkapi semua data")

# Fungsi tampilkan dan hapus data
def tampilkan_data():
    listbox.delete(0, tk.END)
    for row in c.execute("SELECT * FROM makanan"):
        listbox.insert(tk.END, f"{row[0]} - {row[1]} ({row[2]}, {row[3]})")

def hapus_data():
    try:
        selected = listbox.curselection()[0]
        c.execute("DELETE FROM makanan WHERE id=?", (listbox.get(selected).split()[0],))
        conn.commit()
        tampilkan_data()
    except IndexError:
        messagebox.showwarning("Selection Error", "Pilih data yang ingin dihapus")

# Navigasi halaman
def switch_page(page):
    page.tkraise()

# Simpan input sementara
def simpan_input(key, entry, next_page):
    data_makanan[key] = entry.get()
    if data_makanan[key]:
        switch_page(next_page)
    else:
        messagebox.showwarning("Input Error", f"{key.capitalize()} tidak boleh kosong")

def clear_data():
    global data_makanan
    data_makanan = {}

# Setup GUI
root = tk.Tk()
root.title("Data Makanan")

# Membuat frame untuk setiap halaman
halaman_awal = tk.Frame(root)
halaman_awal.grid(row=0, column=0, sticky='news')

halaman_nama = tk.Frame(root)
halaman_nama.grid(row=0, column=0, sticky='news')

halaman_kategori = tk.Frame(root)
halaman_kategori.grid(row=0, column=0, sticky='news')

halaman_warna = tk.Frame(root)
halaman_warna.grid(row=0, column=0, sticky='news')

halaman_tampilkan_data = tk.Frame(root)
halaman_tampilkan_data.grid(row=0, column=0, sticky='news')

# --- Halaman Awal ---
tk.Label(halaman_awal, text="Masukkan Detail Makanan", font=("Arial", 16)).pack(pady=10)
tk.Button(halaman_awal, text="Masukkan Nama Makanan", command=lambda: switch_page(halaman_nama)).pack(pady=10)

# --- Halaman Nama ---
tk.Label(halaman_nama, text="Masukkan Nama Makanan", font=("Arial", 16)).pack(pady=10)
entry_nama = tk.Entry(halaman_nama)
entry_nama.pack(pady=10)
tk.Button(halaman_nama, text="Lanjut", command=lambda: simpan_input('nama', entry_nama, halaman_kategori)).pack(pady=10)

# --- Halaman Kategori ---
tk.Label(halaman_kategori, text="Masukkan Kategori Makanan", font=("Arial", 16)).pack(pady=10)
entry_kategori = tk.Entry(halaman_kategori)
entry_kategori.pack(pady=10)
tk.Button(halaman_kategori, text="Lanjut", command=lambda: simpan_input('kategori', entry_kategori, halaman_warna)).pack(pady=10)

# --- Halaman Warna ---
tk.Label(halaman_warna, text="Masukkan Warna Makanan", font=("Arial", 16)).pack(pady=10)
entry_warna = tk.Entry(halaman_warna)
entry_warna.pack(pady=10)
tk.Button(halaman_warna, text="Lanjut", command=lambda: simpan_input('warna', entry_warna, halaman_tampilkan_data)).pack(pady=10)

# --- Halaman Tampilkan Data ---
tk.Label(halaman_tampilkan_data, text="Data Makanan", font=("Arial", 16)).pack(pady=10)
tk.Button(halaman_tampilkan_data, text="Simpan Data", command=tambah_data).pack(pady=10)
listbox = tk.Listbox(halaman_tampilkan_data, width=50)
listbox.pack(pady=10)
tk.Button(halaman_tampilkan_data, text="Hapus Data", command=hapus_data).pack(pady=10)

# Menampilkan halaman awal saat aplikasi pertama kali dijalankan
switch_page(halaman_awal)
tampilkan_data()

root.mainloop()
conn.close()
