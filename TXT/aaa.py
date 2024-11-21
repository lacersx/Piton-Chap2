import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from tkcalendar import Calendar

class Baca:
    @staticmethod
    def baca_file_kategori(lokasi_file):
        try:
            with open(lokasi_file, 'r') as file:
                lines = file.read().strip().splitlines()
                category_data = {}

                for line in lines[1:]:  # Skip header line
                    if ':' in line and line.strip():
                        try:
                            id_category, category = line.split(':', 1)
                            id_category = int(id_category.strip())
                            category = category.strip()
                            category_data[id_category] = category
                        except ValueError as e:
                            print(f"Error processing line '{line}': {e}")
                return category_data
        except FileNotFoundError:
            print(f"File {lokasi_file} tidak ditemukan.")
            return {}

    @staticmethod
    def baca_file_warna(lokasi_file):
        try:
            with open(lokasi_file, 'r') as file:
                lines = file.read().strip().splitlines()
                color_data = {}

                for line in lines[1:]:  # Skip header line
                    if ':' in line and line.strip():
                        try:
                            id_color, color = line.split(':', 1)
                            id_color = int(id_color.strip())
                            color = color.strip()
                            color_data[id_color] = color
                        except ValueError as e:
                            print(f"Error processing line '{line}': {e}")
                return color_data
        except FileNotFoundError:
            print(f"File {lokasi_file} tidak ditemukan.")
            return {}

    @staticmethod
    def baca_file_makanan(lokasi_file):
        try:
            with open(lokasi_file, 'r') as file:
                lines = file.read().strip().splitlines()
                food_data = []
                for line in lines[1:]:  # Skip header line
                    if ':' in line:
                        try:
                            parts = line.split(':')
                            if len(parts) >= 4:
                                id_food = int(parts[0])
                                name = parts[1].strip()
                                category_id = int(parts[2].strip())
                                color_id = int(parts[3].strip())
                                food_data.append({
                                    "id": id_food,
                                    "name": name,
                                    "category_id": category_id,
                                    "color_id": color_id
                                })
                        except (ValueError, IndexError) as e:
                            print(f"Error processing line '{line}': {e}")
                return food_data
        except FileNotFoundError:
            print(f"File {lokasi_file} tidak ditemukan.")
            return []

    def baca_file_transaksi(lokasi_file):
            try:
                with open(lokasi_file, 'r') as file:
                    lines = file.read().strip().splitlines()
                    transaction_data = []
                
                    for line in lines[1:]:  # Skip header line
                        if ':' in line and line.strip():
                            try:
                                # Split line into components
                                parts = line.split(':')
                                if len(parts) >= 5:
                                    transaction_data.append({
                                        'timestamp': parts[0].strip(),
                                        'food_name': parts[1].strip(),
                                        'quantity': int(parts[2].strip()),
                                        'category': parts[3].strip(),
                                        'color': parts[4].strip()
                                    })
                            except (ValueError, IndexError) as e:
                                print(f"Error processing transaction line '{line}': {e}")
                    return transaction_data
            except FileNotFoundError:
                print(f"File {lokasi_file} tidak ditemukan.")
                return []

    @staticmethod
    def simpan_file_kategori(lokasi_file, categories):
        try:
            with open(lokasi_file, 'w') as file:
                file.write("ID:Kategori\n")  # Header
                for id_category, category in categories.items():
                    file.write(f"{id_category}:{category}\n")
            return True
        except Exception as e:
            print(f"Error saving category file: {e}")
            return False

    @staticmethod
    def simpan_file_warna(lokasi_file, colors):
        try:
            with open(lokasi_file, 'w') as file:
                file.write("ID:Warna\n")  # Header
                for id_color, color in colors.items():
                    file.write(f"{id_color}:{color}\n")
            return True
        except Exception as e:
            print(f"Error saving color file: {e}")
            return False

    @staticmethod
    def simpan_file_makanan(lokasi_file, foods):
        try:
            with open(lokasi_file, 'w') as file:
                file.write("ID:Nama:KategoriID:WarnaID\n")  # Header
                for food in foods:
                    file.write(f"{food['id']}:{food['name']}:{food['category_id']}:{food['color_id']}\n")
            return True
        except Exception as e:
            print(f"Error saving food file: {e}")
            return False

    def simpan_file_transaksi(lokasi_file, transactions):
        try:
            with open(lokasi_file, 'w') as file:
                file.write("Timestamp:FoodName:Quantity:Category:Color\n")  # Header
                for transaction in transactions:
                    file.write(f"{transaction['timestamp']}:{transaction['food_name']}:"
                             f"{transaction['quantity']}:{transaction['category']}:"
                             f"{transaction['color']}\n")
            return True
        except Exception as e:
            print(f"Error saving transaction file: {e}")
            return False

class FoodApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Data Management")
        self.root.geometry("800x600")

        # Initialize data structures
        self.colors = {}     # Will be populated from file
        self.foods = []      # Will be populated from file
        self.categories = {} # Will be populated from file
        self.transaction_history = []
        
        # Initialize category window and listboxes as None
        self.category_window = None
        self.add_category_listbox = None
        self.delete_category_listbox = None
        
        # Load data from files
        self.load_data()
        
        # Setup UI
        self.setup_ui()
        self.update_listbox()

    def load_data(self):
        # Load categories
        self.categories = Baca.baca_file_kategori("Data_Kategori.txt")
        if not self.categories:
            messagebox.showwarning("Warning", "File kategori tidak ditemukan atau kosong. Silakan tambahkan kategori terlebih dahulu.")
        
        # Load colors
        self.colors = Baca.baca_file_warna("Data_Warna.txt")
        if not self.colors:
            messagebox.showwarning("Warning", "File warna tidak ditemukan atau kosong. Silakan tambahkan warna terlebih dahulu.")
        
        # Load foods
        self.foods = Baca.baca_file_makanan("Data_Makanan.txt")
        if not self.foods:
            messagebox.showwarning("Warning", "File makanan tidak ditemukan atau kosong.")

        self.transaction_history = Baca.baca_file_transaksi("Data_Transaksi.txt")
        if not self.transaction_history:
            messagebox.showwarning("Warning", "File makanan tidak ditemukan atau kosong.")


    def setup_ui(self):
        # Food List Frame
        self.food_list_frame = tk.Frame(self.root, bg="#bdb2ff", bd=2, relief="groove")
        self.food_list_frame.place(x=20, y=20, width=300, height=500)
        
        tk.Label(self.food_list_frame, text="Data Makanan", bg="#bdb2ff", font=("Arial", 12, "bold")).pack()
        self.food_listbox = tk.Listbox(self.food_list_frame)
        self.food_listbox.pack(fill="both", expand=True)
        
        # Control buttons
        tk.Button(self.food_list_frame, text="Tambah Data Makanan", command=self.add_food).pack(pady=5)
        tk.Button(self.food_list_frame, text="Edit Data Makanan", command=self.edit_food).pack(pady=5)
        tk.Button(self.food_list_frame, text="Hapus Data Makanan", command=self.delete_food).pack(pady=5)

        # Menu buttons
        tk.Button(self.food_list_frame, text="Menu Kategori", command=self.show_category_menu).pack(pady=5)
        tk.Button(self.food_list_frame, text="Menu Warna", command=self.show_color_frame).pack(pady=5)
        tk.Button(self.food_list_frame, text="Menu Transaksi", command=self.show_transaction_menu).pack(pady=5)

        # Add Food Frame
        self.add_food_frame = tk.Frame(self.root, bg="#bdb2ff", bd=2, relief="groove")
        self.add_food_frame.place(x=350, y=20, width=400, height=250)
        
        tk.Label(self.add_food_frame, text="Tambah Data Makanan", bg="#bdb2ff", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Food input fields
        tk.Label(self.add_food_frame, text="Nama Makanan:").pack()
        self.food_name_entry = tk.Entry(self.add_food_frame)
        self.food_name_entry.pack(pady=1)

        # Category input fields
        tk.Label(self.add_food_frame, text="Kategori :").pack(pady=1)

        # Category dropdown
        self.food_category_var = tk.StringVar()
        self.food_category_menu = tk.OptionMenu(self.add_food_frame, self.food_category_var, "")
        self.update_category_menu()
        self.food_category_menu.pack()

        # Color input fields
        tk.Label(self.add_food_frame, text="Warna :").pack(pady=1)

        # Color dropdown
        self.food_color_var = tk.StringVar()
        self.food_color_menu = tk.OptionMenu(self.add_food_frame, self.food_color_var, "")
        self.update_color_menu()
        self.food_color_menu.pack()

        tk.Button(self.add_food_frame, text="Simpan Makanan", command=self.save_food).pack(pady=10)

    def update_category_menu(self):
        menu = self.food_category_menu["menu"]
        menu.delete(0, "end")
        for category in self.categories.values():
            menu.add_command(label=category, command=lambda x=category: self.food_category_var.set(x))
        if self.categories:
            self.food_category_var.set(list(self.categories.values())[0])

    def update_color_menu(self):
        menu = self.food_color_menu["menu"]
        menu.delete(0, "end")
        for color in self.colors.values():
            menu.add_command(label=color, command=lambda x=color: self.food_color_var.set(x))
        if self.colors:
            self.food_color_var.set(list(self.colors.values())[0])

    # Category management
    def show_category_menu(self):
        # If window exists, bring it to front instead of creating new one
        if self.category_window is not None:
            self.category_window.lift()
            self.category_window.focus_force()
            return

        self.category_window = tk.Toplevel(self.root)
        self.category_window.title("Menu Kategori")
        self.category_window.geometry("500x400")

        # Handle window close event
        self.category_window.protocol("WM_DELETE_WINDOW", self.on_category_window_close)

        # Create notebook for tabs
        notebook = ttk.Notebook(self.category_window)
        notebook.pack(expand=True, fill="both", padx=10, pady=5)

        # Create frames for tabs
        add_frame = ttk.Frame(notebook)
        delete_frame = ttk.Frame(notebook)

        # Setup Add Category Tab
        tk.Label(add_frame, text="Tambah Kategori Baru", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Category input
        tk.Label(add_frame, text="Nama Kategori:").pack(pady=5)
        self.new_category_entry = tk.Entry(add_frame)
        self.new_category_entry.pack(pady=5)

        # Add button
        tk.Button(add_frame, text="Tambah Kategori", 
                 command=self.add_category).pack(pady=10)

        # Category list in add tab
        tk.Label(add_frame, text="Daftar Kategori:", font=("Arial", 10, "bold")).pack(pady=5)
        self.add_category_listbox = tk.Listbox(add_frame, width=40, height=10)
        self.add_category_listbox.pack(pady=5, padx=10)

        # Setup Delete Category Tab
        tk.Label(delete_frame, text="Hapus Kategori", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Create delete_category_listbox
        self.delete_category_listbox = tk.Listbox(delete_frame, width=40, height=10)
        self.delete_category_listbox.pack(pady=10, padx=10)
        
        # Delete button
        tk.Button(delete_frame, text="Hapus Kategori Terpilih", 
                 command=self.delete_category).pack(pady=10)

        # Warning label
        tk.Label(delete_frame, text="Catatan: Kategori yang sedang digunakan\ntidak dapat dihapus", 
                fg="red").pack(pady=10)

        # Add the frames to notebook
        notebook.add(add_frame, text="Tambah Kategori")
        notebook.add(delete_frame, text="Hapus Kategori")

        # Update both listboxes
        self.update_category_listboxes()

    def on_category_window_close(self):
        """Handle category window closure"""
        self.category_window.destroy()
        self.category_window = None
        self.add_category_listbox = None
        self.delete_category_listbox = None

    def update_category_listboxes(self):
        """Update category listboxes if they exist"""
        if self.add_category_listbox is not None and self.delete_category_listbox is not None:
            # Update add tab listbox
            self.add_category_listbox.delete(0, tk.END)
            # Update delete tab listbox
            self.delete_category_listbox.delete(0, tk.END)
            
            # Sort categories by ID for consistent display
            sorted_categories = sorted(self.categories.items())
            
            for category_id, category_name in sorted_categories:
                display_text = f"{category_id}: {category_name}"
                self.add_category_listbox.insert(tk.END, display_text)
                self.delete_category_listbox.insert(tk.END, display_text)

    def add_category(self):
        category = self.new_category_entry.get().strip()
        if category:
            # Check if category already exists
            if category in self.categories.values():
                messagebox.showwarning("Warning", "Kategori ini sudah ada!")
                return

            # Generate new category ID
            new_id = max(self.categories.keys(), default=0) + 1
            self.categories[new_id] = category
        
            # Save to file
            if Baca.simpan_file_kategori("Data_Kategori.txt", self.categories):
                messagebox.showinfo("Success", "Kategori baru berhasil ditambahkan")
                self.new_category_entry.delete(0, tk.END)
                self.update_category_listboxes()
                self.update_category_menu()
            else:
                messagebox.showerror("Error", "Gagal menyimpan kategori baru")
        else:
            messagebox.showwarning("Warning", "Nama kategori tidak boleh kosong")

    def delete_category(self):
        selected = self.delete_category_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Pilih kategori yang akan dihapus")
            return

        # Get selected category ID
        selected_item = self.delete_category_listbox.get(selected[0])
        category_id = int(selected_item.split(':')[0])
    
        # Check if category is in use
        for food in self.foods:
            if food['category_id'] == category_id:
                messagebox.showwarning("Warning", 
                    "Kategori ini sedang digunakan oleh makanan. Hapus atau ubah makanan terlebih dahulu.")
                return
    
        # Delete category
        del self.categories[category_id]
    
        # Save changes
        if Baca.simpan_file_kategori("Data_Kategori.txt", self.categories):
            messagebox.showinfo("Success", "Kategori berhasil dihapus")
            self.update_category_listboxes()
            self.update_category_menu()
        else:
            messagebox.showerror("Error", "Gagal menyimpan perubahan")

    # Color management
    def show_color_frame(self):
        # If window exists, bring it to front instead of creating new one
        if hasattr(self, 'color_window') and self.color_window is not None:
            self.color_window.lift()
            self.color_window.focus_force()
            return

        self.color_window = tk.Toplevel(self.root)
        self.color_window.title("Menu Warna")
        self.color_window.geometry("500x400")

        # Handle window close event
        self.color_window.protocol("WM_DELETE_WINDOW", self.on_color_window_close)

        # Create notebook for tabs
        notebook = ttk.Notebook(self.color_window)
        notebook.pack(expand=True, fill="both", padx=10, pady=5)

        # Create frames for tabs
        add_frame = ttk.Frame(notebook)
        delete_frame = ttk.Frame(notebook)

        # Setup Add Color Tab
        tk.Label(add_frame, text="Tambah Warna Baru", font=("Arial", 12, "bold")).pack(pady=10)
    
        # Color input
        tk.Label(add_frame, text="Nama Warna:").pack(pady=5)
        self.new_color_entry = tk.Entry(add_frame)
        self.new_color_entry.pack(pady=5)

        # Add button
        tk.Button(add_frame, text="Tambah Warna", 
                 command=self.add_color).pack(pady=10)

        # Color list in add tab
        tk.Label(add_frame, text="Daftar Warna:", font=("Arial", 10, "bold")).pack(pady=5)
        self.add_color_listbox = tk.Listbox(add_frame, width=40, height=10)
        self.add_color_listbox.pack(pady=5, padx=10)

        # Setup Delete Color Tab
        tk.Label(delete_frame, text="Hapus Warna", font=("Arial", 12, "bold")).pack(pady=10)
    
        # Create delete_color_listbox
        self.delete_color_listbox = tk.Listbox(delete_frame, width=40, height=10)
        self.delete_color_listbox.pack(pady=10, padx=10)
    
        # Delete button
        tk.Button(delete_frame, text="Hapus Warna Terpilih", 
                 command=self.delete_color).pack(pady=10)

        # Warning label
        tk.Label(delete_frame, text="Catatan: Warna yang sedang digunakan\ntidak dapat dihapus", 
                fg="red").pack(pady=10)

        # Add the frames to notebook
        notebook.add(add_frame, text="Tambah Warna")
        notebook.add(delete_frame, text="Hapus Warna")

        # Update both listboxes
        self.update_color_listboxes()

    def on_color_window_close(self):
        """Handle color window closure"""
        self.color_window.destroy()
        self.color_window = None
        self.add_color_listbox = None
        self.delete_color_listbox = None

    def update_color_listboxes(self):
        """Update color listboxes if they exist"""
        if hasattr(self, 'add_color_listbox') and hasattr(self, 'delete_color_listbox'):
            if self.add_color_listbox is not None and self.delete_color_listbox is not None:
                # Update add tab listbox
                self.add_color_listbox.delete(0, tk.END)
                # Update delete tab listbox
                self.delete_color_listbox.delete(0, tk.END)

                # Sort colors by ID for consistent display
                sorted_colors = sorted(self.colors.items())
            
                for color_id, color_name in sorted_colors:
                    display_text = f"{color_id}: {color_name}"
                    self.add_color_listbox.insert(tk.END, display_text)
                    self.delete_color_listbox.insert(tk.END, display_text)

    def add_color(self):
        color = self.new_color_entry.get().strip()
        if color:
            # Check if color already exists
            if color in self.colors.values():
                messagebox.showwarning("Warning", "Warna ini sudah ada!")
                return

            # Generate new color ID
            new_id = max(self.colors.keys(), default=0) + 1
            self.colors[new_id] = color
    
            # Save to file
            if Baca.simpan_file_warna("Data_Warna.txt", self.colors):
                messagebox.showinfo("Success", "Warna baru berhasil ditambahkan")
                self.new_color_entry.delete(0, tk.END)
                self.update_color_listboxes()
                self.update_color_menu()
            else:
                messagebox.showerror("Error", "Gagal menyimpan warna baru")
        else:
            messagebox.showwarning("Warning", "Nama warna tidak boleh kosong")

    def delete_color(self):
        selected = self.delete_color_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Pilih warna yang akan dihapus")
            return

        # Get selected color ID
        selected_item = self.delete_color_listbox.get(selected[0])
        color_id = int(selected_item.split(':')[0])

        # Check if color is in use
        for food in self.foods:
            if food['color_id'] == color_id:
                messagebox.showwarning("Warning", 
                    "Warna ini sedang digunakan oleh makanan. Hapus atau ubah makanan terlebih dahulu.")
                return

        # Delete color
        del self.colors[color_id]

        # Save changes
        if Baca.simpan_file_warna("Data_Warna.txt", self.colors):
            messagebox.showinfo("Success", "Warna berhasil dihapus")
            self.update_color_listboxes()
            self.update_color_menu()
        else:
            messagebox.showerror("Error", "Gagal menyimpan perubahan")

    def show_transaction_menu(self):
        self.transaction_window = tk.Toplevel(self.root)
        self.transaction_window.title("Menu Transaksi")
        self.transaction_window.geometry("600x500")

        # Create notebook for tabs
        notebook = ttk.Notebook(self.transaction_window)
        notebook.pack(expand=True, fill="both", padx=10, pady=5)

        # Add Transaction Tab
        add_frame = ttk.Frame(notebook)
        notebook.add(add_frame, text="Tambah Transaksi")

        # Transaction History Tab
        history_frame = ttk.Frame(notebook)
        notebook.add(history_frame, text="Riwayat Transaksi")

        # Setup Add Transaction Tab
        tk.Label(add_frame, text="Tambah Transaksi Baru", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Food selection
        tk.Label(add_frame, text="Pilih Makanan:").pack(pady=5)
        self.transaction_food_var = tk.StringVar()
        self.transaction_food_menu = ttk.Combobox(add_frame, textvariable=self.transaction_food_var)
        self.update_food_menu()
        self.transaction_food_menu.pack(pady=5)

        # Quantity input
        tk.Label(add_frame, text="Jumlah:").pack(pady=5)
        self.quantity_entry = tk.Entry(add_frame)
        self.quantity_entry.pack(pady=5)

        # Calendar input
        tk.Label(add_frame, text="Pilih Tanggal Transaksi:").pack(pady=5)
        self.calendar = Calendar(add_frame, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendar.pack(pady=5)

        # Add transaction button
        tk.Button(add_frame, text="Tambah Transaksi", 
                 command=self.add_transaction).pack(pady=10)

        # Transaction list
        tk.Label(add_frame, text="Daftar Transaksi:", font=("Arial", 10, "bold")).pack(pady=5)
        self.transaction_listbox = tk.Listbox(add_frame, width=50, height=10)
        self.transaction_listbox.pack(pady=5, padx=10)
        self.update_transaction_list()

        # Setup Transaction History Tab
        tk.Label(history_frame, text="Riwayat Transaksi", font=("Arial", 12, "bold")).pack(pady=10)

        # Filter frame
        filter_frame = ttk.Frame(history_frame)
        filter_frame.pack(pady=5, padx=10, fill='x')

        # Filter inputs
        tk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT, padx=5)
        self.filter_entry = tk.Entry(filter_frame, width=20)
        self.filter_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(filter_frame, text="Cari", command=self.filter_transactions).pack(side=tk.LEFT, padx=5)
        tk.Button(filter_frame, text="Reset", command=self.reset_transaction_filter).pack(side=tk.LEFT, padx=5)

        # Treeview for transactions
        self.transaction_tree = ttk.Treeview(history_frame, columns=("Tanggal", "Makanan", "Jumlah", "Kategori", "Warna"), show='headings')

        # Define column headings
        self.transaction_tree.heading("Tanggal", text="Tanggal", command=lambda: self.sort_column("Tanggal", False))
        self.transaction_tree.heading("Makanan", text="Makanan", command=lambda: self.sort_column("Makanan", False))
        self.transaction_tree.heading("Jumlah", text="Jumlah", command=lambda: self.sort_column("Jumlah", False))
        self.transaction_tree.heading("Kategori", text="Kategori", command=lambda: self.sort_column("Kategori", False))
        self.transaction_tree.heading("Warna", text="Warna", command=lambda: self.sort_column("Warna", False))

        # Define column widths
        self.transaction_tree.column("Tanggal", width=100, anchor='center')
        self.transaction_tree.column("Makanan", width=150, anchor='center')
        self.transaction_tree.column("Jumlah", width=50, anchor='center')
        self.transaction_tree.column("Kategori", width=100, anchor='center')
        self.transaction_tree.column("Warna", width=100, anchor='center')

        # Scrollbar for treeview
        transaction_scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.transaction_tree.yview)
        self.transaction_tree.configure(yscroll=transaction_scrollbar.set)

        self.transaction_tree.pack(side=tk.LEFT, fill='both', expand=True, padx=10, pady=10)
        transaction_scrollbar.pack(side=tk.RIGHT, fill='y')

        # Delete transaction button
        tk.Button(history_frame, text="Hapus Transaksi Terpilih", 
                 command=self.delete_transaction).pack(pady=10)

        # Populate treeview
        self.update_transaction_list()

    def update_food_menu(self):
        food_names = [food['name'] for food in self.foods]
        self.transaction_food_menu['values'] = food_names
        if food_names:
            self.transaction_food_menu.set(food_names[0])

    def add_transaction(self):
        pass
        food_name = self.transaction_food_var.get()
        quantity = self.quantity_entry.get().strip()

        if not food_name or not quantity:
            messagebox.showwarning("Error", "Pilih makanan dan masukkan jumlah")
            return

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            messagebox.showwarning("Error", "Jumlah harus berupa angka positif")
            return

        # Find the selected food in the foods list
        selected_food = next((food for food in self.foods if food['name'] == food_name), None)
        if selected_food:
            selected_date = self.calendar.get_date()  # Mengambil tanggal dari kalender
            category_name = self.categories.get(selected_food['category_id'], 'Unknown')
            color_name = self.colors.get(selected_food['color_id'], 'Unknown')

            transaction = {
                'date': selected_date,
                'food_name': food_name,
                'quantity': quantity,
                'category': category_name,
                'color': color_name
            }

            self.transaction_history.append(transaction)

            # Simpan transaksi ke file
            if Baca.simpan_file_transaksi("Data_Transaksi.txt", self.transaction_history):
                self.update_transaction_list()
                self.update_delete_transaction_list()
                self.quantity_entry.delete(0, tk.END)
                messagebox.showinfo("Success", "Transaksi berhasil ditambahkan")
            else:
                messagebox.showerror("Error", "Gagal menyimpan transaksi")
        else:
            messagebox.showerror("Error", "Makanan tidak ditemukan")

    def delete_transaction(self):
        selected = self.delete_transaction_listbox.curselection()
        if not selected:
            messagebox.showwarning("Error", "Pilih transaksi yang akan dihapus")
            return

        index = selected[0]
        if 0 <= index < len(self.transaction_history):
            self.transaction_history.pop(index)
            
            # Save changes to file
            if Baca.simpan_file_transaksi("Data_Transaksi.txt", self.transaction_history):
                self.update_transaction_list()
                self.update_delete_transaction_list()
                messagebox.showinfo("Success", "Transaksi berhasil dihapus")
            else:
                messagebox.showerror("Error", "Gagal menyimpan perubahan transaksi")
        else:
            messagebox.showerror("Error", "Indeks transaksi tidak valid")

    def update_transaction_list(self):
        # Clear existing items
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)
    
        # Populate treeview
        for transaction in self.transaction_history:
            self.transaction_tree.insert('', 'end', values=(
                transaction['timestamp'], 
                transaction['food_name'], 
                transaction['quantity'], 
                transaction['category'], 
                transaction['color']
            ))

    def sort_column(self, col, reverse):
        # Get the data to sort
        data = [(self.transaction_tree.set(child, col), child) for child in self.transaction_tree.get_children('')]
    
        # Sort based on the column
        data.sort(reverse=reverse)
    
        # Rearrange items in treeview
        for index, (val, child) in enumerate(data):
            self.transaction_tree.move(child, '', index)
    
        # Toggle sort direction for next click
        self.transaction_tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    def filter_transactions(self):
        filter_text = self.filter_entry.get().lower().strip()
    
        # Clear existing items
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)
    
        # Filter and repopulate
        for transaction in self.transaction_history:
            # Check if filter text is in any of the transaction details
            if (filter_text in transaction['timestamp'].lower() or 
                filter_text in transaction['food_name'].lower() or 
                filter_text in str(transaction['quantity']).lower() or 
                filter_text in transaction['category'].lower() or 
                filter_text in transaction['color'].lower()):
                self.transaction_tree.insert('', 'end', values=(
                    transaction['timestamp'], 
                    transaction['food_name'], 
                    transaction['quantity'], 
                    transaction['category'], 
                    transaction['color']
                ))

    def reset_transaction_filter(self):
        # Clear filter entry
        self.filter_entry.delete(0, tk.END)
    
        # Repopulate with all transactions
        self.update_transaction_list()

    def update_delete_transaction_list(self):
        if self.delete_transaction_listbox:
            self.delete_transaction_listbox.delete(0, tk.END)
            for transaction in self.transaction_history:
                self.delete_transaction_listbox.insert(tk.END, 
                    f"{transaction['timestamp']} - {transaction['food_name']} "
                    f"({transaction['quantity']}) - {transaction['category']} - {transaction['color']}")


    def update_listbox(self):
        self.food_listbox.delete(0, tk.END)
        for food in self.foods:
            category_name = self.categories.get(food['category_id'], 'Unknown')
            color_name = self.colors.get(food['color_id'], 'Unknown')
            self.food_listbox.insert(tk.END, f"{food['name']} - {category_name} - {color_name}")

    def get_id_by_value(self, dictionary, value):
        for key, val in dictionary.items():
            if val == value:
                return key
        return None

    def save_food(self):
        name = self.food_name_entry.get().strip()
        color = self.food_color_var.get()
        category = self.food_category_var.get()
        
        if name and color and category:
            color_id = self.get_id_by_value(self.colors, color)
            category_id = self.get_id_by_value(self.categories, category)
            
            if color_id is None:
                messagebox.showwarning("Error", "Pilih warna yang valid")
                return
                
            if category_id is None:
                messagebox.showwarning("Error", "Pilih kategori yang valid")
                return
            
            new_id = max([food['id'] for food in self.foods], default=0) + 1
            
            new_food = {
                "id": new_id,
                "name": name,
                "category_id": category_id,
                "color_id": color_id
            }
            
            self.foods.append(new_food)
            
            # Save to file
            if Baca.simpan_file_makanan("Data_Makanan.txt", self.foods):
                self.update_listbox()
                self.food_name_entry.delete(0, tk.END)
                messagebox.showinfo("Success", "Data makanan berhasil disimpan")
            else:
                messagebox.showerror("Error", "Gagal menyimpan data makanan")
        else:
            messagebox.showwarning("Error", "Semua field harus diisi!")

    def add_food(self):
        self.food_name_entry.delete(0, tk.END)
        if self.colors:
            self.food_color_var.set(list(self.colors.values())[0])
        if self.categories:
            self.food_category_var.set(list(self.categories.values())[0])

    def edit_food(self):
        selected = self.food_listbox.curselection()
        if selected:
            index = selected[0]
            if 0 <= index < len(self.foods):
                food = self.foods[index]
                
                self.food_name_entry.delete(0, tk.END)
                self.food_name_entry.insert(0, food['name'])
                
                if food['color_id'] in self.colors:
                    self.food_color_var.set(self.colors[food['color_id']])
                if food['category_id'] in self.categories:
                    self.food_category_var.set(self.categories[food['category_id']])
                
                # Remove the old entry
                self.foods.pop(index)
                self.update_listbox()
            else:
                messagebox.showwarning("Error", "Invalid selection index")
        else:
            messagebox.showwarning("Selection Error", "Pilih makanan untuk diedit")


    def delete_food(self):
        selected = self.food_listbox.curselection()
        if selected:
            index = selected[0]
            if 0 <= index < len(self.foods):
                food = self.foods.pop(index)
                
                # Save to file
                if Baca.simpan_file_makanan("Data_Makanan.txt", self.foods):
                    self.update_listbox()
                    
                    # Record transaction
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    category_name = self.categories.get(food['category_id'], 'Unknown')
                    color_name = self.colors.get(food['color_id'], 'Unknown')
                    
                    self.transaction_history.append(
                        f"{timestamp} - Deleted: {food['name']} - {category_name} - {color_name}"
                    )
                    
                    messagebox.showinfo("Success", "Data makanan berhasil dihapus")
                else:
                    messagebox.showerror("Error", "Gagal menyimpan perubahan")
            else:
                messagebox.showwarning("Error", "Invalid selection index")
        else:
            messagebox.showwarning("Selection Error", "Pilih makanan untuk dihapus")

if __name__ == "__main__":
    root = tk.Tk()
    app = FoodApp(root)
    root.mainloop()
  