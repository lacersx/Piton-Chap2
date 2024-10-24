import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Data Kategori dan Warna
kategori_data = {
    1: 'Protein',
    2: 'Mineral',
    3: 'Snack',
    4: 'Karbohidrat',
    5: 'Segar'
}

warna_data = {
    1: 'Kuning',
    2: 'Hijau',
    3: 'Merah',
    4: 'Biru'
}

makanan_data = []  # List untuk menyimpan data makanan
transaksi_data = []  # List untuk menyimpan data transaksi

# Fungsi untuk membaca data makanan dari file txt
def baca_data_dari_file(nama_file='Data_Makanan.txt'):
    try:
        with open(nama_file, 'r') as file:
            for line in file:
                # Pisahkan data berdasarkan koma
                nama, kategori, warna = line.strip().split(',')
                # Simpan ke dalam list makanan_data
                makanan_data.append({
                    'nama': nama,
                    'kategori': int(kategori),
                    'warna': int(warna)
                })
    except FileNotFoundError:
        messagebox.showwarning("File Tidak Ditemukan", f"File '{nama_file}' tidak ditemukan!")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# Fungsi untuk menampilkan data
def tampilkan_data():
    listbox.delete(0, tk.END)
    for idx, makanan in enumerate(makanan_data, start=1):
        listbox.insert(
            tk.END, 
            f"{idx}. {makanan['nama']} (Kategori: {kategori_data[makanan['kategori']]}, Warna: {warna_data[makanan['warna']]})"
        )

# Fungsi untuk menyimpan data ke list (database)
def simpan_ke_database():
    try:
        nama = Data_Makanan['nama']
        kategori = int(Data_Makanan['kategori'])
        warna = int(Data_Makanan['warna'])

        # Tambahkan data baru ke list makanan_data
        makanan_data.append({'nama': nama, 'kategori': kategori, 'warna': warna})
        
        # Perbarui tampilan di Listbox
        tampilkan_data()

        # Reset Data_Makanan untuk input baru
        Data_Makanan.clear()
        Data_Makanan.update({'nama': '', 'kategori': '', 'warna': ''})

        messagebox.showinfo("Berhasil", "Data makanan berhasil disimpan!")
    
    except ValueError:
        messagebox.showerror("Input Error", "Kategori dan Warna harus berupa angka!")

# Fungsi untuk membuka jendela input kategori
def buka_kategori_window():
    window = tk.Toplevel(root)
    window.title("Kategori Makanan")
    window.geometry("300x200")
    window.configure(bg="#4B306A")
    
    label = tk.Label(window, text="Masukkan Kategori (1-5)", font=("Arial", 12), bg="#4B306A", fg="white")
    label.pack(pady=10)
    
    entry_kategori = tk.Entry(window, font=("Arial", 12))
    entry_kategori.pack(pady=10)

    def lanjut_warna():
        kategori = entry_kategori.get()
        if kategori.isdigit() and 1 <= int(kategori) <= 5:
            Data_Makanan['kategori'] = kategori
            window.destroy()
            buka_warna_window()
        else:
            messagebox.showwarning("Input Error", "Kategori harus berupa angka antara 1 hingga 5!")

    lanjut_button = tk.Button(window, text="Lanjut", command=lanjut_warna, bg="white")
    lanjut_button.pack(pady=10)

# Fungsi untuk membuka jendela input warna
def buka_warna_window():
    window = tk.Toplevel(root)
    window.title("Warna Makanan")
    window.geometry("300x200")
    window.configure(bg="#4B306A")
    
    label = tk.Label(window, text="Masukkan Warna (1-4)", font=("Arial", 12), bg="#4B306A", fg="white")
    label.pack(pady=10)
    
    entry_warna = tk.Entry(window, font=("Arial", 12))
    entry_warna.pack(pady=10)

    def simpan_data():
        warna = entry_warna.get()
        if warna.isdigit() and 1 <= int(warna) <= 4:
            Data_Makanan['warna'] = warna
            window.destroy()
            simpan_ke_database()
        else:
            messagebox.showwarning("Input Error", "Warna harus berupa angka antara 1 hingga 4!")

    simpan_button = tk.Button(window, text="Selesai", command=simpan_data, bg="white")
    simpan_button.pack(pady=10)


# Fungsi untuk membuka jendela detail makanan
def buka_detail_makanan():
    window = tk.Toplevel(root)
    window.title("Data Makanan")
    window.geometry("300x200")
    window.configure(bg="#4B306A")
    
    label = tk.Label(window, text="Masukkan Nama Makanan", font=("Arial", 12), bg="#4B306A", fg="white")
    label.pack(pady=10)
    
    entry_nama = tk.Entry(window, font=("Arial", 12))
    entry_nama.pack(pady=10)

    def lanjut_kategori():
        nama_makanan = entry_nama.get()
        if nama_makanan:
            Data_Makanan['nama'] = nama_makanan
            window.destroy()
            buka_kategori_window()
        else:
            messagebox.showwarning("Input Error", "Nama Makanan Harus Diisi!")
    
    lanjut_button = tk.Button(window, text="Lanjut", command=lanjut_kategori, bg="white")
    lanjut_button.pack(pady=10)

# Variabel global untuk menyimpan input sementara
Data_Makanan = {'nama': '', 'kategori': '', 'warna': ''}

# Membuat GUI utama
root = tk.Tk()
root.title("Data Makanan & Transaksi")
root.geometry("500x600")
root.configure(bg="#4B306A")

# Tombol untuk membuka input nama makanan
button_tambah = tk.Button(root, text="Tambah Makanan", command=buka_detail_makanan, width=20, bg="white")
button_tambah.pack(pady=10)

# Listbox untuk menampilkan data makanan
listbox = tk.Listbox(root, font=("Arial", 12), width=50, height=10)
listbox.pack(pady=10)

# Tombol untuk menutup aplikasi
button_tutup = tk.Button(root, text="Tutup Aplikasi", command=root.quit, width=20, bg="white")
button_tutup.pack(pady=10)

# Baca data dari file dan tampilkan di listbox
baca_data_dari_file()
tampilkan_data()

root.mainloop()
