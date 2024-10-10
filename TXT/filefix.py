import tkinter as tk
from tkinter import messagebox
import sqlite3

# Koneksi ke database
conn = sqlite3.connect('makanan.db')
c = conn.cursor()

# Buat tabel jika belum ada
c.execute('''CREATE TABLE IF NOT EXISTS makanan (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                nama TEXT, 
                kategori TEXT, 
                warna TEXT)''')

# Variabel global untuk menyimpan input dari tiap window
data_makanan = {'nama': '', 'kategori': '', 'warna': ''}

# Fungsi untuk menambah data ke dalam database setelah semua input diterima
def tambah_data_ke_db():
    nama = data_makanan['nama']
    kategori = data_makanan['kategori']
    warna = data_makanan['warna']
    
    if nama and kategori and warna:
        c.execute("INSERT INTO makanan (nama, kategori, warna) VALUES (?, ?, ?)", (nama, kategori, warna))
        conn.commit()
        tampilkan_data()
        data_makanan['nama'] = ''
        data_makanan['kategori'] = ''
        data_makanan['warna'] = ''
    else:
        messagebox.showwarning("Input Error", "Semua field harus diisi!")

# Fungsi untuk menghapus data
def hapus_data():
    try:
        selected = listbox.curselection()[0]
        makanan_id = listbox.get(selected).split()[0]  # ambil ID
        c.execute("DELETE FROM makanan WHERE id=?", (makanan_id,))
        conn.commit()
        tampilkan_data()
    except IndexError:
        messagebox.showwarning("Pilih Data", "Pilih data yang ingin dihapus!")

# Fungsi untuk menampilkan data di listbox
def tampilkan_data():
    listbox.delete(0, tk.END)
    for row in c.execute("SELECT * FROM makanan"):
        listbox.insert(tk.END, f"{row[0]} - {row[1]} ({row[2]}, {row[3]})")

# Fungsi untuk membuka window input kategori
def input_kategori_window():
    window = tk.Toplevel(root)
    window.title("Input Kategori Makanan")
    window.geometry("300x200")
    window.configure(bg="#76608A")  # Warna latar belakang sama
    
    label = tk.Label(window, text="Masukkan Kategori", font=("Arial", 12), bg="#76608A", fg="white")
    label.pack(pady=10)
    
    entry = tk.Entry(window, font=("Arial", 12))
    entry.pack(pady=10)
    
    def lanjutkan():
        kategori = entry.get()
        if kategori:
            data_makanan['kategori'] = kategori
            window.destroy()
            input_warna_window()  # Lanjut ke input warna
        else:
            messagebox.showwarning("Input Error", "Kategori harus diisi!")
    
    button = tk.Button(window, text="Lanjut", command=lanjutkan, bg="white")
    button.pack(pady=10)

# Fungsi untuk membuka window input warna
def input_warna_window():
    window = tk.Toplevel(root)
    window.title("Input Warna Makanan")
    window.geometry("300x200")
    window.configure(bg="#76608A")  # Warna latar belakang sama
    
    label = tk.Label(window, text="Masukkan Warna", font=("Arial", 12), bg="#76608A", fg="white")
    label.pack(pady=10)
    
    entry = tk.Entry(window, font=("Arial", 12))
    entry.pack(pady=10)
    
    def lanjutkan():
        warna = entry.get()
        if warna:
            data_makanan['warna'] = warna
            window.destroy()
            tambah_data_ke_db()  # Simpan data dan kembali ke tampilan utama
        else:
            messagebox.showwarning("Input Error", "Warna harus diisi!")
    
    button = tk.Button(window, text="Selesai", command=lanjutkan, bg="white")
    button.pack(pady=10)

# Fungsi untuk membuka window input nama
def input_nama_window():
    window = tk.Toplevel(root)
    window.title("Input Nama Makanan")
    window.geometry("300x200")
    window.configure(bg="#76608A")  # Warna latar belakang sama
    
    label = tk.Label(window, text="Masukkan Nama Makanan", font=("Arial", 12), bg="#76608A", fg="white")
    label.pack(pady=10)
    
    entry = tk.Entry(window, font=("Arial", 12))
    entry.pack(pady=10)
    
    def lanjutkan():
        nama = entry.get()
        if nama:
            data_makanan['nama'] = nama
            window.destroy()
            input_kategori_window()  # Lanjut ke input kategori
        else:
            messagebox.showwarning("Input Error", "Nama harus diisi!")
    
    button = tk.Button(window, text="Lanjut", command=lanjutkan, bg="white")
    button.pack(pady=10)

# Membuat GUI utama
root = tk.Tk()
root.title("Data Makanan")
root.geometry("600x500")
root.configure(bg="#76608A")

# Frame untuk form input
frame_form = tk.Frame(root, bg="#76608A")
frame_form.pack(padx=20, pady=10)

# Frame untuk listbox
frame_list = tk.Frame(root, bg="#76608A")
frame_list.pack(padx=20, pady=10)

# Tombol untuk membuka input nama
button_tambah = tk.Button(frame_form, text="Tambah Makanan", command=input_nama_window, width=15, bg="white")
button_tambah.grid(row=0, column=0, pady=10)

# Tombol untuk menghapus data
button_hapus = tk.Button(frame_form, text="Hapus", command=hapus_data, width=15, bg="white")
button_hapus.grid(row=0, column=1, pady=10)

# Listbox untuk menampilkan data makanan
label_list = tk.Label(frame_list, text="Data Makanan", font=("Arial", 14, "bold"), bg="#76608A", fg="white")
label_list.pack(pady=5)
listbox = tk.Listbox(frame_list, font=("Arial", 12), width=50, height=10)
listbox.pack(pady=5)

# Menampilkan data saat aplikasi dibuka
tampilkan_data()

root.mainloop()

# Tutup koneksi database saat aplikasi ditutup
conn.close()