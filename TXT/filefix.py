import tkinter as tk
from tkinter import messagebox

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

makanan_data = [
    {'nama': 'Chiki Pedas', 'kategori': 3, 'warna': 2},
    {'nama': 'Sayuran', 'kategori': 2, 'warna': 2},
    {'nama': 'Kentang', 'kategori': 1, 'warna': 3},
    {'nama': 'Mie', 'kategori': 3, 'warna': 2},
]

# Fungsi untuk membuka jendela detail makanan
def buka_detail_makanan():
    window = tk.Toplevel(root)
    window.title("Data Makanan")
    window.geometry("300x200")
    window.configure(bg="#4B306A")  # Warna latar belakang sama
    
    label = tk.Label(window, text="Masukkan Nama Makanan", font=("Arial", 12), bg="#4B306A", fg="white")
    label.pack(pady=10)
    
    entry_nama = tk.Entry(window, font=("Arial", 12))
    entry_nama.pack(pady=10)

    def lanjut_kategori():
        nama_makanan = entry_nama.get()
        if nama_makanan:
            data_makanan['nama'] = nama_makanan
            window.destroy()
            buka_kategori_window()
        else:
            messagebox.showwarning("Input Error", "Nama Makanan Harus Diisi!")
    
    lanjut_button = tk.Button(window, text="Lanjut", command=lanjut_kategori, bg="white")
    lanjut_button.pack(pady=10)

# Fungsi untuk membuka jendela input kategori
def buka_kategori_window():
    window = tk.Toplevel(root)
    window.title("Kategori Makanan")
    window.geometry("300x200")
    window.configure(bg="#4B306A")  # Warna latar belakang sama
    
    label = tk.Label(window, text="Masukkan Kategori Makanan", font=("Arial", 12), bg="#4B306A", fg="white")
    label.pack(pady=10)
    
    entry_kategori = tk.Entry(window, font=("Arial", 12))
    entry_kategori.pack(pady=10)

    def lanjut_warna():
        kategori = entry_kategori.get()
        if kategori:
            data_makanan['kategori'] = kategori
            window.destroy()
            buka_warna_window()
        else:
            messagebox.showwarning("Input Error", "Kategori Harus Diisi!")
    
    lanjut_button = tk.Button(window, text="Lanjut", command=lanjut_warna, bg="white")
    lanjut_button.pack(pady=10)

# Fungsi untuk membuka jendela input warna
def buka_warna_window():
    window = tk.Toplevel(root)
    window.title("Warna Makanan")
    window.geometry("300x200")
    window.configure(bg="#4B306A")  # Warna latar belakang sama
    
    label = tk.Label(window, text="Masukkan Warna Makanan", font=("Arial", 12), bg="#4B306A", fg="white")
    label.pack(pady=10)
    
    entry_warna = tk.Entry(window, font=("Arial", 12))
    entry_warna.pack(pady=10)

    def simpan_data():
        warna = entry_warna.get()
        if warna:
            data_makanan['warna'] = warna
            window.destroy()
            simpan_ke_database()
        else:
            messagebox.showwarning("Input Error", "Warna Harus Diisi!")
    
    simpan_button = tk.Button(window, text="Selesai", command=simpan_data, bg="white")
    simpan_button.pack(pady=10)

# Fungsi untuk menyimpan data ke list (database)
def simpan_ke_database():
    nama = data_makanan['nama']
    kategori = data_makanan['kategori']
    warna = data_makanan['warna']
    
    makanan_data.append({'nama': nama, 'kategori': int(kategori), 'warna': int(warna)})
    tampilkan_data()

# Fungsi untuk menampilkan data
def tampilkan_data():
    listbox.delete(0, tk.END)
    for idx, makanan in enumerate(makanan_data, start=1):
        listbox.insert(tk.END, f"{idx}. {makanan['nama']} (Kategori: {kategori_data[makanan['kategori']]}, Warna: {warna_data[makanan['warna']]})")

# Fungsi untuk menghapus data yang dipilih
def hapus_data():
    try:
        selected = listbox.curselection()[0]
        del makanan_data[selected]
        tampilkan_data()
    except IndexError:
        messagebox.showwarning("Pilih Data", "Pilih data yang ingin dihapus!")

# Fungsi untuk mengedit data yang dipilih
def edit_data():
    try:
        selected = listbox.curselection()[0]
        makanan_terpilih = makanan_data[selected]

        def lanjut_edit():
            nama_makanan = entry_nama.get()
            kategori = entry_kategori.get()
            warna = entry_warna.get()

            if nama_makanan and kategori and warna:
                makanan_terpilih['nama'] = nama_makanan
                makanan_terpilih['kategori'] = int(kategori)
                makanan_terpilih['warna'] = int(warna)
                window.destroy()
                tampilkan_data()
            else:
                messagebox.showwarning("Input Error", "Semua field harus diisi!")

        window = tk.Toplevel(root)
        window.title("Edit Makanan")
        window.geometry("300x200")
        window.configure(bg="#4B306A")
        
        label_nama = tk.Label(window, text="Edit Nama", font=("Arial", 12), bg="#4B306A", fg="white")
        label_nama.pack(pady=10)
        entry_nama = tk.Entry(window, font=("Arial", 12))
        entry_nama.insert(0, makanan_terpilih['nama'])
        entry_nama.pack(pady=10)

        label_kategori = tk.Label(window, text="Edit Kategori", font=("Arial", 12), bg="#4B306A", fg="white")
        label_kategori.pack(pady=10)
        entry_kategori = tk.Entry(window, font=("Arial", 12))
        entry_kategori.insert(0, makanan_terpilih['kategori'])
        entry_kategori.pack(pady=10)

        label_warna = tk.Label(window, text="Edit Warna", font=("Arial", 12), bg="#4B306A", fg="white")
        label_warna.pack(pady=10)
        entry_warna = tk.Entry(window, font=("Arial", 12))
        entry_warna.insert(0, makanan_terpilih['warna'])
        entry_warna.pack(pady=10)

        simpan_button = tk.Button(window, text="Simpan", command=lanjut_edit, bg="white")
        simpan_button.pack(pady=10)

    except IndexError:
        messagebox.showwarning("Pilih Data", "Pilih data yang ingin diedit!")

# Variabel global untuk menyimpan input sementara
data_makanan = {'nama': '', 'kategori': '', 'warna': ''}

# Membuat GUI utama
root = tk.Tk()
root.title("Data Makanan")
root.geometry("400x500")
root.configure(bg="#4B306A")

# Tombol untuk membuka input nama makanan
button_tambah = tk.Button(root, text="Tambah Makanan", command=buka_detail_makanan, width=20, bg="white")
button_tambah.pack(pady=10)

# Listbox untuk menampilkan data makanan
listbox = tk.Listbox(root, font=("Arial", 12), width=50, height=10)
listbox.pack(pady=10)

# Tombol untuk menghapus data
button_hapus = tk.Button(root, text="Hapus Data", command=hapus_data, width=20, bg="white")
button_hapus.pack(pady=10)

# Tombol untuk mengedit data
button_edit = tk.Button(root, text="Edit Data", command=edit_data, width=20, bg="white")
button_edit.pack(pady=10)

# Tombol untuk menutup aplikasi
button_tutup = tk.Button(root, text="Tutup Aplikasi", command=root.quit, width=20, bg="white")
button_tutup.pack(pady=10)

# Tampilkan data makanan yang ada
tampilkan_data()

root.mainloop()