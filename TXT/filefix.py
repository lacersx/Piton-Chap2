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

# Fungsi untuk menambah data ke dalam database
def tambah_data():
    nama = entry_nama.get()
    kategori = entry_kategori.get()
    warna = entry_warna.get()
    
    if nama and kategori and warna:
        c.execute("INSERT INTO makanan (nama, kategori, warna) VALUES (?, ?, ?)", (nama, kategori, warna))
        conn.commit()
        tampilkan_data()
        clear_entries()
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

# Fungsi untuk mengedit data
def edit_data():
    try:
        selected = listbox.curselection()[0]
        makanan_id = listbox.get(selected).split()[0]  # ambil ID
        nama = entry_nama.get()
        kategori = entry_kategori.get()
        warna = entry_warna.get()
        
        if nama and kategori and warna:
            c.execute("UPDATE makanan SET nama=?, kategori=?, warna=? WHERE id=?", (nama, kategori, warna, makanan_id))
            conn.commit()
            tampilkan_data()
            clear_entries()
        else:
            messagebox.showwarning("Input Error", "Semua field harus diisi!")
    except IndexError:
        messagebox.showwarning("Pilih Data", "Pilih data yang ingin diedit!")

# Fungsi untuk menampilkan data di listbox
def tampilkan_data():
    listbox.delete(0, tk.END)
    for row in c.execute("SELECT * FROM makanan"):
        listbox.insert(tk.END, f"{row[0]} - {row[1]} ({row[2]}, {row[3]})")

# Fungsi untuk membersihkan input
def clear_entries():
    entry_nama.delete(0, tk.END)
    entry_kategori.delete(0, tk.END)
    entry_warna.delete(0, tk.END)

# Membuat GUI
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

# Label dan Entry untuk input data makanan
label_nama = tk.Label(frame_form, text="Nama Makanan", font=("Arial", 12), bg="#76608A", fg="white")
label_nama.grid(row=0, column=0, sticky="w", pady=5)
entry_nama = tk.Entry(frame_form, font=("Arial", 12))
entry_nama.grid(row=0, column=1, pady=5)

label_kategori = tk.Label(frame_form, text="Kategori", font=("Arial", 12), bg="#76608A", fg="white")
label_kategori.grid(row=1, column=0, sticky="w", pady=5)
entry_kategori = tk.Entry(frame_form, font=("Arial", 12))
entry_kategori.grid(row=1, column=1, pady=5)

label_warna = tk.Label(frame_form, text="Warna", font=("Arial", 12), bg="#76608A", fg="white")
label_warna.grid(row=2, column=0, sticky="w", pady=5)
entry_warna = tk.Entry(frame_form, font=("Arial", 12))
entry_warna.grid(row=2, column=1, pady=5)

# Tombol untuk aksi
button_tambah = tk.Button(frame_form, text="Tambah", command=tambah_data, width=15, bg="white")
button_tambah.grid(row=3, column=0, pady=10)

button_edit = tk.Button(frame_form, text="Edit", command=edit_data, width=15, bg="white")
button_edit.grid(row=3, column=1, pady=10)

button_hapus = tk.Button(frame_form, text="Hapus", command=hapus_data, width=15, bg="white")
button_hapus.grid(row=4, column=0, pady=10)

button_simpan = tk.Button(frame_form, text="Simpan", command=lambda: clear_entries(), width=15, bg="white")
button_simpan.grid(row=4, column=1, pady=10)

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