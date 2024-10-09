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

# Fungsi untuk menyimpan data sementara sebelum ditambahkan ke database
data_makanan = {"nama": "", "kategori": "", "warna": ""}

# Fungsi untuk tambah data ke database
def tambah_data():
    if all(data_makanan.values()):
        c.execute("INSERT INTO makanan (nama_makanan, kategori, warna) VALUES (?, ?, ?)",
                  (data_makanan['nama'], data_makanan['kategori'], data_makanan['warna']))
        conn.commit()
        messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")
        clear_data()
        tampilkan_data()
        ganti_halaman(halaman_awal)
    else:
        messagebox.showwarning("Input Error", "Lengkapi semua data")

# Fungsi untuk menampilkan data di Listbox
def tampilkan_data():
    listbox.delete(0, tk.END)
    c.execute("SELECT * FROM makanan")
    rows = c.fetchall()
    for row in rows:
        listbox.insert(tk.END, f"{row[0]} - {row[1]} ({row[2]}, {row[3]})")

# Fungsi untuk menghapus data
def hapus_data():
    try:
        selected_item = listbox.curselection()[0]
        data = listbox.get(selected_item)
        item_id = data.split(' ')[0]  # Ambil ID dari data
        c.execute("DELETE FROM makanan WHERE id=?", (item_id,))
        conn.commit()
        tampilkan_data()
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
    except IndexError:
        messagebox.showwarning("Selection Error", "Pilih data yang ingin dihapus")

# Fungsi untuk mengubah halaman
def ganti_halaman(halaman):
    halaman.tkraise()

# Fungsi untuk mengosongkan data sementara
def clear_data():
    global data_makanan
    data_makanan = {"nama": "", "kategori": "", "warna": ""}

# Fungsi untuk menyimpan input sementara
def simpan_nama():
    data_makanan["nama"] = entry_nama.get()
    if data_makanan["nama"]:
        ganti_halaman(halaman_kategori)
    else:
        messagebox.showwarning("Input Error", "Nama makanan tidak boleh kosong")

def simpan_kategori():
    data_makanan["kategori"] = entry_kategori.get()
    if data_makanan["kategori"]:
        ganti_halaman(halaman_warna)
    else:
        messagebox.showwarning("Input Error", "Kategori tidak boleh kosong")

def simpan_warna():
    data_makanan["warna"] = entry_warna.get()
    if data_makanan["warna"]:
        ganti_halaman(halaman_tampilkan_data)
    else:
        messagebox.showwarning("Input Error", "Warna tidak boleh kosong")

# GUI dengan tkinter
root = tk.Tk()
root.title("Data Makanan")

# Frame Halaman Utama
halaman_awal = tk.Frame(root)
halaman_awal.grid(row=0, column=0, sticky='news')

# Frame Halaman Nama
halaman_nama = tk.Frame(root)
halaman_nama.grid(row=0, column=0, sticky='news')

# Frame Halaman Kategori
halaman_kategori = tk.Frame(root)
halaman_kategori.grid(row=0, column=0, sticky='news')

# Frame Halaman Warna
halaman_warna = tk.Frame(root)
halaman_warna.grid(row=0, column=0, sticky='news')

# Frame Halaman Tampilkan Data
halaman_tampilkan_data = tk.Frame(root)
halaman_tampilkan_data.grid(row=0, column=0, sticky='news')

# --- Halaman Awal ---
label_awal = tk.Label(halaman_awal, text="Masukkan Detail Makanan", font=("Arial", 16))
label_awal.pack(pady=10)

btn_mulai = tk.Button(halaman_awal, text="Masukkan Nama Makanan", command=lambda: ganti_halaman(halaman_nama))
btn_mulai.pack(pady=10)

# --- Halaman Nama ---
label_nama = tk.Label(halaman_nama, text="Masukkan Nama Makanan", font=("Arial", 16))
label_nama.pack(pady=10)

entry_nama = tk.Entry(halaman_nama)
entry_nama.pack(pady=10)

btn_lanjut_nama = tk.Button(halaman_nama, text="Lanjut", command=simpan_nama)
btn_lanjut_nama.pack(pady=10)

# --- Halaman Kategori ---
label_kategori = tk.Label(halaman_kategori, text="Masukkan Kategori Makanan", font=("Arial", 16))
label_kategori.pack(pady=10)

entry_kategori = tk.Entry(halaman_kategori)
entry_kategori.pack(pady=10)

btn_lanjut_kategori = tk.Button(halaman_kategori, text="Lanjut", command=simpan_kategori)
btn_lanjut_kategori.pack(pady=10)

# --- Halaman Warna ---
label_warna = tk.Label(halaman_warna, text="Masukkan Warna Makanan", font=("Arial", 16))
label_warna.pack(pady=10)

entry_warna = tk.Entry(halaman_warna)
entry_warna.pack(pady=10)

btn_lanjut_warna = tk.Button(halaman_warna, text="Lanjut", command=simpan_warna)
btn_lanjut_warna.pack(pady=10)

# --- Halaman Tampilkan Data ---
label_tampilkan = tk.Label(halaman_tampilkan_data, text="Data Makanan", font=("Arial", 16))
label_tampilkan.pack(pady=10)

btn_simpan = tk.Button(halaman_tampilkan_data, text="Simpan Data", command=tambah_data)
btn_simpan.pack(pady=10)

listbox = tk.Listbox(halaman_tampilkan_data, width=50)
listbox.pack(pady=10)

btn_hapus = tk.Button(halaman_tampilkan_data, text="Hapus Data", command=hapus_data)
btn_hapus.pack(pady=10)

tampilkan_data()

# Menampilkan halaman awal saat aplikasi pertama kali dijalankan
ganti_halaman(halaman_awal)

root.mainloop()

# Tutup koneksi ke database saat aplikasi ditutup
conn.close()
