import tkinter as tk
from tkinter import messagebox

# Data makanan dan transaksi yang akan diisi saat aplikasi berjalan
makanan_data = []
transaksi_data = []
kategori_data = {}
warna_data = {}

# Fungsi untuk membaca data kategori dan warna dari file txt
def load_data(filename):
    data = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                key, value = line.strip().split(',')
                data[int(key)] = value
    except FileNotFoundError:
        messagebox.showerror("Error", f"File {filename} tidak ditemukan.")
    return data

# Fungsi untuk menyimpan data makanan dan transaksi ke file txt
def save_data(filename, data_list):
    with open(filename, "w") as file:
        for data in data_list:
            file.write(",".join(map(str, data.values())) + "\n")

# Fungsi untuk menampilkan data makanan
def tampilkan_data_makanan():
    listbox_makanan.delete(0, tk.END)
    for idx, makanan in enumerate(makanan_data, start=1):
        nama = makanan['nama']
        kategori = kategori_data.get(makanan['kategori'], "Unknown")
        warna = warna_data.get(makanan['warna'], "Unknown")
        listbox_makanan.insert(tk.END, f"{idx}. {nama} (Kategori: {kategori}, Warna: {warna})")

# Fungsi untuk menambah data makanan
def tambah_data_makanan():
    nama = entry_nama.get()
    kategori = int(dropdown_kategori.get())
    warna = int(dropdown_warna.get())
    
    if nama:
        makanan_data.append({'nama': nama, 'kategori': kategori, 'warna': warna})
        tampilkan_data_makanan()
        save_data("makanan_data.txt", makanan_data)
    else:
        messagebox.showwarning("Input Error", "Nama makanan harus diisi!")

# Fungsi untuk menghapus data makanan
def hapus_data_makanan():
    selected = listbox_makanan.curselection()
    if selected:
        makanan_data.pop(selected[0])
        tampilkan_data_makanan()
        save_data("makanan_data.txt", makanan_data)
    else:
        messagebox.showwarning("Pilih Data", "Pilih data yang ingin dihapus.")

# Fungsi untuk menambah transaksi
def tambah_transaksi():
    # Implementasi untuk menambah transaksi berdasarkan pilihan makanan dan harga
    pass

# Memuat data kategori dan warna dari file txt
kategori_data = load_data("kategori_data.txt")
warna_data = load_data("warna_data.txt")

# Membuat GUI
root = tk.Tk()
root.title("Aplikasi Data Makanan & Transaksi")
root.geometry("600x400")

# Tampilan Utama - Listbox untuk menampilkan data makanan
listbox_makanan = tk.Listbox(root, width=50, height=10)
listbox_makanan.pack(pady=10)

# Field input untuk nama makanan
tk.Label(root, text="Nama Makanan:").pack()
entry_nama = tk.Entry(root)
entry_nama.pack()

# Dropdown untuk kategori
tk.Label(root, text="Kategori:").pack()
dropdown_kategori = tk.StringVar(root)
dropdown_kategori.set("Pilih Kategori")
kategori_menu = tk.OptionMenu(root, dropdown_kategori, *kategori_data.keys())
kategori_menu.pack()

# Dropdown untuk warna
tk.Label(root, text="Warna:").pack()
dropdown_warna = tk.StringVar(root)
dropdown_warna.set("Pilih Warna")
warna_menu = tk.OptionMenu(root, dropdown_warna, *warna_data.keys())
warna_menu.pack()

# Tombol untuk menambah makanan
button_tambah = tk.Button(root, text="Tambah Makanan", command=tambah_data_makanan)
button_tambah.pack(pady=5)

# Tombol untuk menghapus makanan
button_hapus = tk.Button(root, text="Hapus Makanan", command=hapus_data_makanan)
button_hapus.pack(pady=5)

# Menampilkan data makanan saat aplikasi dimulai
tampilkan_data_makanan()

root.mainloop()
