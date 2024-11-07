import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Sample data structures
foods = []
categories = ["Protein", "Mineral", "Snack", "Karbohidrat", "Segar"]
colors = ["Kuning", "Hijau", "Merah", "Biru"]
transaction_history = []  # To store the transaction history

# Main Application
class FoodApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Data Management")
        self.root.geometry("800x600")

        # Section for Food List
        self.food_list_frame = tk.Frame(root, bg="#bdb2ff", bd=2, relief="groove")
        self.food_list_frame.place(x=20, y=20, width=300, height=500)
        
        tk.Label(self.food_list_frame, text="Tampilan Data Makanan", bg="#bdb2ff", font=("Arial", 12, "bold")).pack()
        self.food_listbox = tk.Listbox(self.food_list_frame)
        self.food_listbox.pack(fill="both", expand=True)
        
        # Button Panel for Food List
        tk.Button(self.food_list_frame, text="Tambah Data Makanan", command=self.add_food).pack(pady=5)
        tk.Button(self.food_list_frame, text="Edit Data Makanan", command=self.edit_food).pack(pady=5)
        tk.Button(self.food_list_frame, text="Hapus Data Makanan", command=self.delete_food).pack(pady=5)

        # Section for Adding Food
        self.add_food_frame = tk.Frame(root, bg="#bdb2ff", bd=2, relief="groove")
        self.add_food_frame.place(x=350, y=20, width=400, height=300)
        
        tk.Label(self.add_food_frame, text="Tambah Data Makanan", bg="#bdb2ff", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(self.add_food_frame, text="Nama Makanan:").pack()
        self.food_name_entry = tk.Entry(self.add_food_frame)
        self.food_name_entry.pack()

        tk.Label(self.add_food_frame, text="Warna:").pack()
        self.food_color_var = tk.StringVar(value="Select Color")
        self.food_color_menu = tk.OptionMenu(self.add_food_frame, self.food_color_var, *colors)
        self.food_color_menu.pack()

        tk.Label(self.add_food_frame, text="Kategori:").pack()
        self.food_category_var = tk.StringVar(value="Select Category")
        self.food_category_menu = tk.OptionMenu(self.add_food_frame, self.food_category_var, *categories)
        self.food_category_menu.pack()

        tk.Label(self.add_food_frame, text="Harga:").pack()
        self.food_price_entry = tk.Entry(self.add_food_frame)
        self.food_price_entry.pack()

        # Save Button for Adding Food
        tk.Button(self.add_food_frame, text="Simpan", command=self.save_food).pack(pady=10)

        # Section for Adding Category
        self.add_category_frame = tk.Frame(root, bg="#bdb2ff", bd=2, relief="groove")
        self.add_category_frame.place(x=350, y=330, width=400, height=120)
        
        tk.Label(self.add_category_frame, text="Tambah Kategori", bg="#bdb2ff", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(self.add_category_frame, text="Masukan Kategori Baru:").pack()
        self.new_category_entry = tk.Entry(self.add_category_frame)
        self.new_category_entry.pack()
        
        tk.Button(self.add_category_frame, text="Simpan", command=self.save_category).pack(pady=10)

        # Section for Adding Color
        self.add_color_frame = tk.Frame(root, bg="#bdb2ff", bd=2, relief="groove")
        self.add_color_frame.place(x=350, y=460, width=400, height=120)
        
        tk.Label(self.add_color_frame, text="Tambah Warna", bg="#bdb2ff", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(self.add_color_frame, text="Masukan Warna Baru:").pack()
        self.new_color_entry = tk.Entry(self.add_color_frame)
        self.new_color_entry.pack()
        
        tk.Button(self.add_color_frame, text="Simpan", command=self.save_color).pack(pady=10)

        # Section for Transaction History
        self.history_frame = tk.Frame(root, bg="#bdb2ff", bd=2, relief="groove")
        self.history_frame.place(x=350, y=550, width=400, height=200)
        
        tk.Label(self.history_frame, text="Riwayat Transaksi", bg="#bdb2ff", font=("Arial", 12, "bold")).pack(pady=10)
        self.transaction_listbox = tk.Listbox(self.history_frame)
        self.transaction_listbox.pack(fill="both", expand=True)

        # Dropdown to select category for transaction
        tk.Label(self.history_frame, text="Pilih Kategori Transaksi:").pack(pady=5)
        self.transaction_category_var = tk.StringVar(value="Select Category")
        self.transaction_category_menu = tk.OptionMenu(self.history_frame, self.transaction_category_var, *categories)
        self.transaction_category_menu.pack(pady=5)

        # Entry for food price
        tk.Label(self.history_frame, text="Harga Makanan:").pack(pady=5)
        self.transaction_food_price_entry = tk.Entry(self.history_frame)
        self.transaction_food_price_entry.pack(pady=5)
        
        # Button to Add Transaction
        tk.Button(self.history_frame, text="Tambah Transaksi", command=self.add_transaction).pack(pady=5)

    def update_listbox(self):
        # Update listbox with current food items
        self.food_listbox.delete(0, tk.END)
        for food in foods:
            self.food_listbox.insert(tk.END, f"{food['name']} - {food['color']} - {food['category']} - Harga: {food['price']}")

    def update_transaction_history(self):
        # Update the transaction history listbox
        self.transaction_listbox.delete(0, tk.END)
        for transaction in transaction_history:
            self.transaction_listbox.insert(tk.END, transaction)

    def add_food(self):
        # Clear inputs and prepare for adding new food
        self.food_name_entry.delete(0, tk.END)
        self.food_color_var.set("Select Color")
        self.food_category_var.set("Select Category")
        self.food_price_entry.delete(0, tk.END)
        self.root.title("Tambah Data Makanan")

    def save_food(self):
        # Save new food entry
        name = self.food_name_entry.get()
        color = self.food_color_var.get()
        category = self.food_category_var.get()
        price = self.food_price_entry.get()
        if name and color != "Select Color" and category != "Select Category" and price:
            try:
                price = float(price)
                foods.append({"name": name, "color": color, "category": category, "price": price})
                self.update_listbox()

                # Record transaction
                transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                transaction_history.append(f"{transaction_time} - Tambah: {name} - {color} - {category} - Harga: {price}")
                self.update_transaction_history()

                messagebox.showinfo("Success", "Data makanan berhasil disimpan.")
            except ValueError:
                messagebox.showwarning("Input Error", "Harga harus berupa angka.")
        else:
            messagebox.showwarning("Input Error", "Semua kolom harus diisi.")

    def edit_food(self):
        # Edit selected food entry
        selected = self.food_listbox.curselection()
        if selected:
            index = selected[0]
            food = foods[index]
            self.food_name_entry.delete(0, tk.END)
            self.food_name_entry.insert(0, food['name'])
            self.food_color_var.set(food['color'])
            self.food_category_var.set(food['category'])
            self.food_price_entry.delete(0, tk.END)
            self.food_price_entry.insert(0, food['price'])
            foods.pop(index)
            self.root.title("Edit Data Makanan")
        else:
            messagebox.showwarning("Selection Error", "Pilih makanan untuk diedit.")
        self.update_listbox()

    def delete_food(self):
        # Delete selected food entry
        selected = self.food_listbox.curselection()
        if selected:
            index = selected[0]
            food = foods.pop(index)
            self.update_listbox()

            # Record transaction
            transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            transaction_history.append(f"{transaction_time} - Hapus: {food['name']} - {food['color']} - {food['category']} - Harga: {food['price']}")
            self.update_transaction_history()

            messagebox.showinfo("Deleted", "Data makanan berhasil dihapus.")
        else:
            messagebox.showwarning("Selection Error", "Pilih makanan untuk dihapus.")

    def save_category(self):
        # Save new category
        category = self.new_category_entry.get()
        if category:
            categories.append(category)
            self.update_option_menu(self.food_category_menu, self.food_category_var, categories, "Select Category")
            self.new_category_entry.delete(0, tk.END)

            # Record transaction
            transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            transaction_history.append(f"{transaction_time} - Tambah Kategori: {category}")
            self.update_transaction_history()

            messagebox.showinfo("Success", "Kategori berhasil disimpan.")
        else:
            messagebox.showwarning("Input Error", "Kategori tidak boleh kosong.")

    def save_color(self):
        # Save new color
        color = self.new_color_entry.get()
        if color:
            colors.append(color)
            self.update_option_menu(self.food_color_menu, self.food_color_var, colors, "Select Color")
            self.new_color_entry.delete(0, tk.END)

            # Record transaction
            transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            transaction_history.append(f"{transaction_time} - Tambah Warna: {color}")
            self.update_transaction_history()

            messagebox.showinfo("Success", "Warna berhasil disimpan.")
        else:
            messagebox.showwarning("Input Error", "Warna tidak boleh kosong.")

    def update_option_menu(self, menu, var, options, default):
        # Update an OptionMenu widget with new options
        menu["menu"].delete(0, "end")
        var.set(default)
        for option in options:
            menu["menu"].add_command(label=option, command=lambda value=option: var.set(value))

    def add_transaction(self):
        # Record a transaction with selected category and price
        selected_category = self.transaction_category_var.get()
        food_price = self.transaction_food_price_entry.get()
        if selected_category != "Select Category" and food_price:
            try:
                food_price = float(food_price)
                transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                transaction_history.append(f"{transaction_time} - Transaksi dengan kategori: {selected_category} - Harga: {food_price}")
                self.update_transaction_history()
                messagebox.showinfo("Success", f"Transaksi dengan kategori '{selected_category}' dan harga {food_price} berhasil ditambahkan.")
            except ValueError:
                messagebox.showwarning("Input Error", "Harga harus berupa angka.")
        else:
            messagebox.showwarning("Selection Error", "Pilih kategori transaksi dan masukkan harga.")

# Run the application
root = tk.Tk()
app = FoodApp(root)
root.mainloop()
