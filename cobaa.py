import tkinter as tk
from tkinter import messagebox
import sqlite3

# Koneksi ke database SQLite
conn = sqlite3.connect('makanan.db')
c = conn.cursor()

# Membuat tabel makanan jika belum ada
c.execute('''
CREATE TABLE IF NOT EXISTS makanan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_makanan TEXT,
    kategori TEXT,
    warna TEXT
)
''')
conn.commit()

data_makanan = {}
selected_id = None  # Untuk menyimpan id data yang sedang diedit

# Fungsi untuk menyimpan atau mengubah data
def simpan_data():
    if all(data_makanan.values()):
        if selected_id:  # Jika sedang dalam mode edit
            c.execute("UPDATE makanan SET nama_makanan=?, kategori=?, warna=? WHERE id=?",
                      (data_makanan['nama'], data_makanan['kategori'], data_makanan['warna'], selected_id))
            messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        else:
            c.execute("INSERT INTO makanan (nama_makanan, kategori, warna) VALUES (?, ?, ?)",
                      (data_makanan['nama'], data_makanan['kategori'], data_makanan['warna']))
            messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")
        conn.commit()
        clear_data()
        tampilkan_data()
        switch_page(halaman_awal)
    else:
        messagebox.showwarning("Input Error", "Lengkapi semua data")

# Fungsi untuk menampilkan data di Listbox
def tampilkan_data():
    listbox.delete(0, tk.END)
    for row in c.execute("SELECT * FROM makanan"):
        listbox.insert(tk.END, f"{row[0]} - {row[1]} ({row[2]}, {row[3]})")

# Fungsi untuk menghapus data
def hapus_data():
    try:
        selected = listbox.curselection()[0]
        item_id = listbox.get(selected).split(' - ')[0]  # Ambil ID dari data yang dipilih
        c.execute("DELETE FROM makanan WHERE id=?", (item_id,))
        conn.commit()
        tampilkan_data()
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
    except IndexError:
        messagebox.showwarning("Selection Error", "Pilih data yang ingin dihapus")

# Fungsi untuk mengedit data
def edit_data():
    global selected_id
    try:
        selected = listbox.curselection()[0]
        selected_id = listbox.get(selected).split(' - ')[0]  # Ambil ID dari data yang dipilih

        # Mendapatkan data dari database berdasarkan ID
        c.execute("SELECT * FROM makanan WHERE id=?", (selected_id,))
        row = c.fetchone()

        # Mengisi input field dengan data yang dipilih
        entry_nama.delete(0, tk.END)
        entry_nama.insert(0, row[1])
        entry_kategori.delete(0, tk.END)
        entry_kategori.insert(0, row[2])
        entry_warna.delete(0, tk.END)
        entry_warna.insert(0, row[3])

        # Beralih ke halaman input untuk mengedit data
        switch_page(halaman_nama)
    except IndexError:
        messagebox.showwarning("Selection Error", "Pilih data yang ingin diedit")

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
    global data_makanan, selected_id
    data_makanan = {}
    selected_id = None  # Reset ID yang dipilih setelah proses edit selesai

def reset_data():
        c.execute("delete from makanan")
        conn.commit()
        tampilkan_data() #refresh listbox setelah penghapusan
        messagebox.showinfo("reset", "semua data telah dihapus")

# Setup GUI
root = tk.Tk()
root.title("Data Makanan")

# Warna ungu yang digunakan
ungu = "#76608A"

# Membuat frame untuk setiap halaman dan menerapkan warna ungu
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

# --- Halaman Awal ---
tk.Label(halaman_awal, text="Masukkan Detail Makanan", font=("Arial", 16), bg=ungu, fg="white").pack(pady=10)
tk.Button(halaman_awal, text="Masukkan Nama Makanan", command=lambda: switch_page(halaman_nama), bg="white").pack(pady=10)

# --- Halaman Nama ---
tk.Label(halaman_nama, text="Masukkan Nama Makanan", font=("Arial", 16), bg=ungu, fg="white").pack(pady=10)
entry_nama = tk.Entry(halaman_nama)
entry_nama.pack(pady=10)
tk.Button(halaman_nama, text="Lanjut", command=lambda: simpan_input('nama', entry_nama, halaman_kategori), bg="white").pack(pady=10)

# --- Halaman Kategori ---
tk.Label(halaman_kategori, text="Masukkan Kategori Makanan", font=("Arial", 16), bg=ungu, fg="white").pack(pady=10)
entry_kategori = tk.Entry(halaman_kategori)
entry_kategori.pack(pady=10)
tk.Button(halaman_kategori, text="Lanjut", command=lambda: simpan_input('kategori', entry_kategori, halaman_warna), bg="white").pack(pady=10)

# --- Halaman Warna ---
tk.Label(halaman_warna, text="Masukkan Warna Makanan", font=("Arial", 16), bg=ungu, fg="white").pack(pady=10)
entry_warna = tk.Entry(halaman_warna)
entry_warna.pack(pady=10)
tk.Button(halaman_warna, text="Lanjut", command=lambda: simpan_input('warna', entry_warna, halaman_tampilkan_data), bg="white").pack(pady=10)

# --- Halaman Tampilkan Data ---
tk.Label(halaman_tampilkan_data, text="Data Makanan", font=("Arial", 16), bg=ungu, fg="white").pack(pady=10)
tk.Button(halaman_tampilkan_data, text="Simpan Data", command=simpan_data, bg="white").pack(pady=10)
listbox = tk.Listbox(halaman_tampilkan_data, width=50)
listbox.pack(pady=10)
tk.Button(halaman_tampilkan_data, text="Hapus Data", command=hapus_data, bg="white").pack(pady=10)
tk.Button(halaman_tampilkan_data, text="Edit Data", command=edit_data, bg="white").pack(pady=10)

# Menampilkan halaman awal saat aplikasi pertama kali dijalankan
switch_page(halaman_awal)
tampilkan_data()

root.mainloop()

# Tutup koneksi ke database saat aplikasi ditutup
conn.close()
