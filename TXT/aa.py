import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Initialize main application window
root = tk.Tk()
root.title("Data Makanan & Transaksi")
root.geometry("500x500")
root.configure(bg="#A48ACF")

makanan_data = []

class Baca:
    def baca_file(lokasi_file):
        try:
            with open(lokasi_file, 'r') as file:
                data = file.read().strip()
            return data
        except FileNotFoundError:
            print(f"File {lokasi_file} tidak ditemukan.")
            return None

def simpan_ke_database():
    try:
        nama = data_makanan['nama']
        kategori = int(data_makanan['kategori'])
        warna = int(data_makanan['warna'])

        # Tambahkan data baru ke list makanan_data
        makanan_data.append({'nama': nama, 'kategori': kategori, 'warna': warna})
        
        # Perbarui tampilan di Listbox
        tampilkan_data()

        # Reset data_makanan untuk input baru
        data_makanan.clear()
        data_makanan.update({'nama': '', 'kategori': '', 'warna': ''})

        messagebox.showinfo("Berhasil", "Data makanan berhasil disimpan!")
    
    except ValueError:
        messagebox.showerror("Input Error", "Kategori dan Warna harus berupa angka!")

#Fungsi untuk menampilkan data
def tampilkan_data():
    listbox.delete(0, tk.END)
    for idx, makanan in enumerate(makanan_data, start=1):
        listbox.insert(tk.END, f"{idx}. {makanan['nama']} (Kategori: {kategori_data[makanan['kategori']]}, Warna: {warna_data[makanan['warna']]})")

# Fungsi untuk menampilkan transaksi
def tampilkan_transaksi():
    transaksi_listbox.delete(0, tk.END)
    for idx, transaksi in enumerate(transaksi_data, start=1):
        transaksi_listbox.insert(tk.END, f"{idx}. {transaksi['tanggal']} - {transaksi['nama']} - Rp {transaksi['harga']}")

# Function placeholders for button actions
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


def hapus_data_makanan():
    selected_makanan = listbox.curselection()
    selected_transaksi = transaksi_listbox.curselection()

    if selected_makanan:
        try:
            selected = listbox.curselection()[0]
            del makanan_data[selected]
            tampilkan_data()
        except IndexError:
            messagebox.showwarning("Pilih Data", "Pilih data yang ingin dihapus!")
    
    elif selected_transaksi:
        try:
            selected = selected_transaksi[0]
            del transaksi_data[selected]
            tampilkan_transaksi()
        except IndexError:
            messagebox.showwarning("Pilih Data", "Pilih data transaksi yang ingin dihapus!")
    
    else:
        messagebox.showwarning("Pilih Data", "Tidak ada data yang dipilih untuk dihapus!")

def edit_data_makanan():
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
        window.configure(bg="#76608A")
        
        label_nama = tk.Label(window, text="Edit Nama", font=("Arial", 12), bg="#76608A", fg="white")
        label_nama.pack(pady=10)
        entry_nama = tk.Entry(window, font=("Arial", 12))
        entry_nama.insert(0, makanan_terpilih['nama'])
        entry_nama.pack(pady=10)

        label_kategori = tk.Label(window, text="Edit Kategori", font=("Arial", 12), bg="#76608A", fg="white")
        label_kategori.pack(pady=10)
        entry_kategori = tk.Entry(window, font=("Arial", 12))
        entry_kategori.insert(0, makanan_terpilih['kategori'])
        entry_kategori.pack(pady=10)

        label_warna = tk.Label(window, text="Edit Warna", font=("Arial", 12), bg="#76608A", fg="white")
        label_warna.pack(pady=10)
        entry_warna = tk.Entry(window, font=("Arial", 12))
        entry_warna.insert(0, makanan_terpilih['warna'])
        entry_warna.pack(pady=10)

        simpan_button = tk.Button(window, text="Simpan", command=lanjut_edit, bg="white")
        simpan_button.pack(pady=10)

    except IndexError:
        messagebox.showwarning("Pilih Data", "Pilih data yang ingin diedit!")


def hapus_data_lain():
    pass

def edit_data_lain():
    pass

def tambah_transaksi():
    window = tk.Toplevel(root)
    window.title("Tambah Transaksi")
    window.geometry("300x250")
    window.configure(bg="#76608A")

    label_nama = tk.Label(window, text="Pilih Makanan", font=("Arial", 12), bg="#76608A", fg="white")
    label_nama.pack(pady=10)

    makanan_var = tk.StringVar(window)
    makanan_var.set(makanan_data[0]['nama'])  # Default pilihan pertama

    makanan_option = tk.OptionMenu(window, makanan_var, *[m['nama'] for m in makanan_data])
    makanan_option.pack(pady=10)

    label_harga = tk.Label(window, text="Masukkan Harga", font=("Arial", 12), bg="#76608A", fg="white")
    label_harga.pack(pady=10)

    entry_harga = tk.Entry(window, font=("Arial", 12))
    entry_harga.pack(pady=10)

    def simpan_transaksi():
        makanan = makanan_var.get()
        harga = entry_harga.get()

        if harga:
            transaksi_data.append({
                'tanggal': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'nama': makanan,
                'harga': harga
            })
            window.destroy()
            tampilkan_transaksi()
        else:
            messagebox.showwarning("Input Error", "Harga Harus Diisi!")

    simpan_button = tk.Button(window, text="Simpan Transaksi", command=simpan_transaksi, bg="white")
    simpan_button.pack(pady=10)

# Variabel global untuk menyimpan input sementara
data_makanan = {'nama': '', 'kategori': '', 'warna': ''}


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

def keluar_aplikasi():
    root.quit()

# Main Frame setup for better structure
frame_main = tk.Frame(root, bg="#A48ACF")
frame_main.pack(expand=True, fill="both")

# Add "Tambah Data" button at the top center
button_tambah = tk.Button(frame_main, text="Tambah Data", command=tambah_data, width=20)
button_tambah.grid(row=0, column=1, pady=(20, 10))

# Display area for 'data_makanan'
label_makanan = tk.Label(frame_main, text="Tampilan Data Makanan", bg="white", width=40, height=10)
label_makanan.grid(row=1, column=1, pady=10, padx=10)

# Listbox untuk menampilkan data makanan
listbox = tk.Listbox(root, font=("Arial", 12), width=50, height=10)
listbox.pack(pady=10)

# Row with multiple buttons under 'data_makanan'
button_hapus_makanan = tk.Button(frame_main, text="Hapus Data Makanan", command=hapus_data_makanan, width=18)
button_edit_makanan = tk.Button(frame_main, text="Edit Data Makanan", command=edit_data_makanan, width=18)
button_tambah_transaksi = tk.Button(frame_main, text="Tambah Transaksi", command=tambah_transaksi, width=18)
button_hapus_lain = tk.Button(frame_main, text="Hapus Data Lain", command=hapus_data_lain, width=18)
button_edit_lain = tk.Button(frame_main, text="Edit Data Lain", command=edit_data_lain, width=18)

button_hapus_makanan.grid(row=2, column=0, padx=5, pady=5)
button_edit_makanan.grid(row=2, column=1, padx=5, pady=5)
button_tambah_transaksi.grid(row=2, column=2, padx=5, pady=5)
button_hapus_lain.grid(row=3, column=0, padx=5, pady=5)
button_edit_lain.grid(row=3, column=2, padx=5, pady=5)

# Display area for 'data_transaksi'
label_transaksi = tk.Label(frame_main, text="Tampilan Data Transaksi", bg="white", width=40, height=10)
label_transaksi.grid(row=4, column=1, pady=10, padx=10)

# Bottom row with "Simpan Data" and "Keluar Aplikasi" buttons
button_simpan = tk.Button(frame_main, text="Simpan Data", command=simpan_data, width=18)
button_keluar = tk.Button(frame_main, text="Keluar Aplikasi", command=keluar_aplikasi, width=18)

button_simpan.grid(row=5, column=0, pady=10, padx=5)
button_keluar.grid(row=5, column=2, pady=10, padx=5)

root.mainloop()
