import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json

# Fungsi untuk memuat data
def muat_data():
    global makanan_data, kategori_data, warna_data
    try:
        with open('Data_Makanan.json', 'r') as f:
            makanan_data = json.load(f)
    except FileNotFoundError:
        makanan_data = []
    
    try:
        with open('Data_Kategori.json', 'r') as f:
            kategori_data = json.load(f)
    except FileNotFoundError:
        kategori_data = {1: "Buah", 2: "Sayuran", 3: "Daging"}
    
    try:
        with open('Data_Warna.json', 'r') as f:
            warna_data = json.load(f)
    except FileNotFoundError:
        warna_data = {1: "Merah", 2: "Hijau", 3: "Kuning"}

# Fungsi untuk menyimpan data
def simpan_data():
    with open('Data_Makanan.json', 'w') as f:
        json.dump(makanan_data, f)
    with open('Data_Kategori.json', 'w') as f:
        json.dump(kategori_data, f)
    with open('Data_Warna.json', 'w') as f:
        json.dump(warna_data, f)

# Inisialisasi jendela aplikasi utama
root = tk.Tk()
root.title("Data Makanan & Transaksi")
root.geometry("600x600")
root.configure(bg="#A48ACF")

makanan_data = []
transaksi_data = []
kategori_data = {1: "Buah", 2: "Sayuran", 3: "Daging"}
warna_data = {1: "Merah", 2: "Hijau", 3: "Kuning"}

data_makanan = {'nama': '', 'kategori': '', 'warna': ''}

muat_data()  # Memuat data saat program dijalankan

# Fungsi untuk menyimpan makanan ke database
def simpan_ke_database():
    try:
        nama = data_makanan['nama']
        kategori = int(data_makanan['kategori'])
        warna = int(data_makanan['warna'])
        
        makanan_data.append({'nama': nama, 'kategori': kategori, 'warna': warna})
        tampilkan_riwayat_makanan()
        
        data_makanan.update({'nama': '', 'kategori': '', 'warna': ''})
        simpan_data()  # Menyimpan data ke file setelah menambahkan item baru
        messagebox.showinfo("Berhasil", "Data makanan berhasil disimpan!")
    
    except ValueError:
        messagebox.showerror("Error Input", "Kategori dan Warna harus berupa angka!")

# Menampilkan riwayat makanan
def tampilkan_riwayat_makanan():
    riwayat_makanan_text.config(state=tk.NORMAL)  # Mengaktifkan text untuk diperbarui
    riwayat_makanan_text.delete(1.0, tk.END)  # Menghapus data sebelumnya
    for idx, makanan in enumerate(makanan_data, start=1):
        riwayat_makanan_text.insert(tk.END, f"{idx}. Nama: {makanan['nama']}, Kategori: {kategori_data.get(makanan['kategori'], 'N/A')}, Warna: {warna_data.get(makanan['warna'], 'N/A')}\n")
    riwayat_makanan_text.config(state=tk.DISABLED)  # Menonaktifkan text untuk pengeditan

# Menampilkan riwayat transaksi
def tampilkan_riwayat_transaksi():
    riwayat_transaksi_text.config(state=tk.NORMAL)
    riwayat_transaksi_text.delete(1.0, tk.END)  # Menghapus data sebelumnya
    for idx, transaksi in enumerate(transaksi_data, start=1):
        riwayat_transaksi_text.insert(tk.END, f"{idx}. Tanggal: {transaksi['tanggal']}, Nama: {transaksi['nama']}, Harga: Rp {transaksi['harga']}\n")
    riwayat_transaksi_text.config(state=tk.DISABLED)

# Menambahkan data makanan
def tambah_data():
    def simpan_input():
        data_makanan['nama'] = entry_nama.get()
        data_makanan['kategori'] = entry_kategori.get()
        data_makanan['warna'] = entry_warna.get()
        simpan_ke_database()
        window.destroy()
    
    window = tk.Toplevel(root)
    window.title("Tambah Data")
    window.geometry("300x250")
    window.configure(bg="#76608A")
    
    tk.Label(window, text="Nama", bg="#76608A", fg="white").pack(pady=5)
    entry_nama = tk.Entry(window)
    entry_nama.pack(pady=5)
    
    tk.Label(window, text="Kategori (1: Buah, 2: Sayuran, 3: Daging)", bg="#76608A", fg="white").pack(pady=5)
    entry_kategori = tk.Entry(window)
    entry_kategori.pack(pady=5)
    
    tk.Label(window, text="Warna (1: Merah, 2: Hijau, 3: Kuning)", bg="#76608A", fg="white").pack(pady=5)
    entry_warna = tk.Entry(window)
    entry_warna.pack(pady=5)
    
    tk.Button(window, text="Simpan", command=simpan_input).pack(pady=10)

# Mengedit data makanan
def edit_data():
    def simpan_edit():
        index = int(entry_index.get()) - 1
        if 0 <= index < len(makanan_data):
            field = edit_option.get()
            if field == "Nama":
                makanan_data[index]['nama'] = entry_value.get()
            elif field == "Kategori":
                makanan_data[index]['kategori'] = int(entry_value.get())
            elif field == "Warna":
                makanan_data[index]['warna'] = int(entry_value.get())
            tampilkan_riwayat_makanan()
            window.destroy()
        else:
            messagebox.showerror("Error", "Index tidak valid!")
    
    window = tk.Toplevel(root)
    window.title("Edit Data")
    window.geometry("300x300")
    window.configure(bg="#76608A")
    
    tk.Label(window, text="Index Data yang akan diedit", bg="#76608A", fg="white").pack(pady=5)
    entry_index = tk.Entry(window)
    entry_index.pack(pady=5)
    
    tk.Label(window, text="Pilih kolom yang akan diedit", bg="#76608A", fg="white").pack(pady=5)
    edit_option = tk.StringVar(value="Nama")
    tk.OptionMenu(window, edit_option, "Nama", "Kategori", "Warna").pack(pady=5)
    
    tk.Label(window, text="Nilai Baru", bg="#76608A", fg="white").pack(pady=5)
    entry_value = tk.Entry(window)
    entry_value.pack(pady=5)
    
    tk.Button(window, text="Simpan Edit", command=simpan_edit).pack(pady=10)

# Menghapus data makanan
def hapus_data_makanan():
    def hapus_terpilih():
        nama_makanan = makanan_var.get()
        for makanan in makanan_data:
            if makanan['nama'] == nama_makanan:
                makanan_data.remove(makanan)
                tampilkan_riwayat_makanan()
                window.destroy()
                simpan_data()  # Menyimpan data ke file setelah menghapus item
                messagebox.showinfo("Hapus Data", f"Data makanan '{nama_makanan}' telah dihapus!")
                return
        messagebox.showwarning("Hapus Data", "Makanan tidak ditemukan!")

    if not makanan_data:
        messagebox.showwarning("Hapus Data", "Tidak ada data makanan untuk dihapus!")
        return

    window = tk.Toplevel(root)
    window.title("Hapus Data")
    window.geometry("300x200")
    window.configure(bg="#76608A")
    
    tk.Label(window, text="Pilih Makanan untuk Dihapus", bg="#76608A", fg="white").pack(pady=5)
    makanan_var = tk.StringVar(value=makanan_data[0]['nama'] if makanan_data else "")
    tk.OptionMenu(window, makanan_var, *[m['nama'] for m in makanan_data]).pack(pady=5)
    
    tk.Button(window, text="Hapus Makanan", command=hapus_terpilih).pack(pady=10)

# Menambahkan transaksi
def tambah_transaksi():
    def simpan_transaksi():
        transaksi_data.append({
            'tanggal': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'nama': makanan_var.get(),
            'harga': entry_harga.get()
        })
        tampilkan_riwayat_transaksi()
        window.destroy()
    
    window = tk.Toplevel(root)
    window.title("Tambah Transaksi")
    window.geometry("300x250")
    window.configure(bg="#76608A")
    
    tk.Label(window, text="Pilih Makanan", bg="#76608A", fg="white").pack(pady=5)
    makanan_var = tk.StringVar(value=makanan_data[0]['nama'] if makanan_data else "")
    tk.OptionMenu(window, makanan_var, *[m['nama'] for m in makanan_data]).pack(pady=5)
    
    tk.Label(window, text="Harga", bg="#76608A", fg="white").pack(pady=5)
    entry_harga = tk.Entry(window)
    entry_harga.pack(pady=5)
    
    tk.Button(window, text="Simpan Transaksi", command=simpan_transaksi).pack(pady=10)

# Membuat tombol untuk menambah, mengedit, dan menghapus data
tambah_button = tk.Button(root, text="Tambah Data Makanan", command=tambah_data)
tambah_button.pack(pady=10)

edit_button = tk.Button(root, text="Edit Data Makanan", command=edit_data)
edit_button.pack(pady=10)

hapus_button = tk.Button(root, text="Hapus Data Makanan", command=hapus_data_makanan)
hapus_button.pack(pady=10)

transaksi_button = tk.Button(root, text="Tambah Transaksi", command=tambah_transaksi)
transaksi_button.pack(pady=10)

# Menampilkan riwayat makanan
riwayat_makanan_text = tk.Text(root, width=60, height=10, state=tk.DISABLED)
riwayat_makanan_text.pack(pady=20)

# Menampilkan riwayat transaksi
riwayat_transaksi_text = tk.Text(root, width=60, height=10, state=tk.DISABLED)
riwayat_transaksi_text.pack(pady=20)

# Menampilkan riwayat makanan dan transaksi saat aplikasi dijalankan
tampilkan_riwayat_makanan()
tampilkan_riwayat_transaksi()

root.mainloop()  