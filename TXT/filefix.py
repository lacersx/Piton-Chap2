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
selected_id = None  # Variabel untuk menyimpan ID makanan yang dipilih saat mengedit

# Fungsi untuk menambah data ke dalam database setelah semua input diterima
def tambah_data_ke_db():
    nama = data_makanan['nama']
    kategori = data_makanan['kategori']
    warna = data_makanan['warna']
    
    if nama and kategori and warna:
        if selected_id:  # Jika sedang mengedit, update data
            c.execute("UPDATE makanan SET nama=?, kategori=?, warna=? WHERE id=?", 
                      (nama, kategori, warna, selected_id))
        else:  # Jika menambah data baru
            c.execute("INSERT INTO makanan (nama, kategori, warna) VALUES (?, ?, ?)", 
                      (nama, kategori, warna))
        conn.commit()
        tampilkan_data()
        data_makanan['nama'] = ''
        data_makanan['kategori'] = ''
        data_makanan['warna'] = ''
        reset_selected_id()
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

# Fungsi untuk mengedit data yang dipilih
def edit_data():
    global selected_id
    try:
        selected = listbox.curselection()[0]
        makanan_data = listbox.get(selected).split()
        selected_id = makanan_data[0]  # Ambil ID
        
        # Ambil data dari database berdasarkan ID yang dipilih
        c.execute("SELECT * FROM makanan WHERE id=?", (selected_id,))
        makanan = c.fetchone()
        
        # Simpan data ke dalam variabel global dan buka window edit
        data_makanan['nama'] = makanan[1]
        data_makanan['kategori'] = makanan[2]
        data_makanan['warna'] = makanan[3]
        
        # Buka window untuk mengedit nama
        input_nama_window(is_edit=True)
        
    except IndexError:
        messagebox.showwarning("Pilih Data", "Pilih data yang ingin diedit!")

# Fungsi untuk membuka window input kategori
def input_kategori_window(is_edit=False):
    window = tk.Toplevel(root)
    window.title("Input Kategori Makanan")
    window.geometry("300x200")
    window.configure(bg="#76608A")  # Warna latar belakang sama
    
    label = tk.Label(window, text="Masukkan Kategori", font=("Arial", 12), bg="#76608A", fg="white")
    label.pack(pady=10)
    
    entry = tk.Entry(window, font=("Arial", 12))
    entry.insert(0, data_makanan['kategori'])  # Isi dengan data sebelumnya jika sedang mengedit
    entry.pack(pady=10)
    
    def lanjutkan():
        kategori = entry.get()
        if kategori:
            data_makanan['kategori'] = kategori
            window.destroy()
            input_warna_window(is_edit)  # Lanjut ke input warna
        else:
            messagebox.showwarning("Input Error", "Kategori harus diisi!")
    
    button = tk.Button(window, text="Lanjut", command=lanjutkan, bg="white")
    button.pack(pady=10)

# Fungsi untuk membuka window input warna
def input_warna_window(is_edit=False):
    window = tk.Toplevel(root)
    window.title("Input Warna Makanan")
    window.geometry("300x200")
    window.configure(bg="#76608A")  # Warna latar belakang sama
    
    label = tk.Label(window, text="Masukkan Warna", font=("Arial", 12), bg="#76608A", fg="white")
    label.pack(pady=10)
    
    entry = tk.Entry(window, font=("Arial", 12))
    entry.insert(0, data_makanan['warna'])  # Isi dengan data sebelumnya jika sedang mengedit
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
def input_nama_window(is_edit=False):
    window = tk.Toplevel(root)
    window.title("Input Nama Makanan")
    window.geometry("300x200")
    window.configure(bg="#76608A")  # Warna latar belakang sama
    
    label = tk.Label(window, text="Masukkan Nama Makanan", font=("Arial", 12), bg="#76608A", fg="white")
    label.pack(pady=10)
    
    entry = tk.Entry(window, font=("Arial", 12))
    entry.insert(0, data_makanan['nama'])  # Isi dengan data sebelumnya jika sedang mengedit
    entry.pack(pady=10)
    
    def lanjutkan():
        nama = entry.get()
        if nama:
            data_makanan['nama'] = nama
            window.destroy()
            input_kategori_window(is_edit)  # Lanjut ke input kategori
        else:
            messagebox.showwarning("Input Error", "Nama harus diisi!")
    
    button = tk.Button(window, text="Lanjut", command=lanjutkan, bg="white")
    button.pack(pady=10)

# Fungsi untuk mereset ID yang dipilih saat selesai edit
def reset_selected_id():
    global selected_id
    selected_id = None

# Fungsi untuk menutup aplikasi
def tutup_aplikasi():
    conn.close()  # Tutup koneksi database sebelum menutup aplikasi
    root.quit()  # Tutup aplikasi

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

# Tombol untuk mengedit data
button_edit = tk.Button(frame_form, text="Edit", command=edit_data, width=15, bg="white")
button_edit.grid(row=0, column=2, pady=10)

# Tombol untuk menutup aplikasi
button_tutup = tk.Button(frame_form, text="Tutup Aplikasi", command=tutup_aplikasi, width=15, bg="white")
button_tutup.grid(row=0, column=3, pady=10)

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