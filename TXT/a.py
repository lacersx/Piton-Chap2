import tkinter as tk
from tkinter import messagebox

# Fungsi untuk membaca data dari file txt dengan format tertentu
def load_data(filename):
    data = {}
    try:
        with open(filename, "r") as file:
            header = file.readline().strip()  # Mengabaikan header
            for line in file:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    key, value = parts
                    data[int(key)] = value
                else:
                    messagebox.showwarning("Format Error", f"Format data di file {filename} tidak sesuai.")
    except FileNotFoundError:
        messagebox.showerror("Error", f"File {filename} tidak ditemukan.")
    except ValueError:
        messagebox.showerror("Error", f"Data di file {filename} mengandung ID yang tidak valid.")
    return data

# Membaca data kategori dan warna
kategori_data = load_data("Data_Kategori.txt")
warna_data = load_data("Data_Warna.txt")

# Mengecek apakah data berhasil dimuat
if kategori_data:
    print("Data Kategori berhasil dimuat:", kategori_data)
else:
    print("Data Kategori tidak ditemukan atau format salah.")

if warna_data:
    print("Data Warna berhasil dimuat:", warna_data)
else:
    print("Data Warna tidak ditemukan atau format salah.")

# GUI sederhana untuk menampilkan dropdown kategori dan warna
root = tk.Tk()
root.title("Dropdown Data dari File")

tk.Label(root, text="Pilih Kategori:").pack()
dropdown_kategori = tk.StringVar(root)
dropdown_kategori.set("Pilih Kategori")
kategori_menu = tk.OptionMenu(root, dropdown_kategori, *kategori_data.values())
kategori_menu.pack()

tk.Label(root, text="Pilih Warna:").pack()
dropdown_warna = tk.StringVar(root)
dropdown_warna.set("Pilih Warna")
warna_menu = tk.OptionMenu(root, dropdown_warna, *warna_data.values())
warna_menu.pack()

# Fungsi untuk menampilkan pilihan yang dipilih
def tampilkan_pilihan():
    kategori_nama = dropdown_kategori.get()
    warna_nama = dropdown_warna.get()
    messagebox.showinfo("Pilihan Anda", f"Kategori: {kategori_nama}\nWarna: {warna_nama}")

tombol_simpan = tk.Button(root, text="Tampilkan Pilihan", command=tampilkan_pilihan)
tombol_simpan.pack()

root.mainloop()
