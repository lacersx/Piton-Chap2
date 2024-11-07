import tkinter as tk
from tkinter import messagebox
from datetime import datetime

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

        # Add Food Frame
        self.add_food_frame = tk.Frame(self.root, bg="#bdb2ff", bd=2, relief="groove")
        self.add_food_frame.place(x=350, y=20, width=400, height=400)
        
        tk.Label(self.add_food_frame, text="Tambah Data Makanan", bg="#bdb2ff", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Food input fields
        tk.Label(self.add_food_frame, text="Nama Makanan:").pack()
        self.food_name_entry = tk.Entry(self.add_food_frame)
        self.food_name_entry.pack()

        # Category input fields
        tk.Label(self.add_food_frame, text="Kategori Baru:").pack()
        self.new_category_entry = tk.Entry(self.add_food_frame)
        self.new_category_entry.pack()
        tk.Button(self.add_food_frame, text="Tambah Kategori", command=self.add_category).pack()

        # Category dropdown
        self.food_category_var = tk.StringVar()
        self.food_category_menu = tk.OptionMenu(self.add_food_frame, self.food_category_var, "")
        self.update_category_menu()
        self.food_category_menu.pack()

        # Color input fields
        tk.Label(self.add_food_frame, text="Warna Baru:").pack()
        self.new_color_entry = tk.Entry(self.add_food_frame)
        self.new_color_entry.pack()
        tk.Button(self.add_food_frame, text="Tambah Warna", command=self.add_color).pack()

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

    def add_category(self):
        category = self.new_category_entry.get().strip()
        if category:
            # Generate new category ID
            new_id = max(self.categories.keys(), default=0) + 1
            self.categories[new_id] = category
            
            # Save to file
            if Baca.simpan_file_kategori("Data_Kategori.txt", self.categories):
                messagebox.showinfo("Success", "Kategori baru berhasil ditambahkan")
                self.new_category_entry.delete(0, tk.END)
                self.update_category_menu()
            else:
                messagebox.showerror("Error", "Gagal menyimpan kategori baru")
        else:
            messagebox.showwarning("Warning", "Nama kategori tidak boleh kosong")

    def add_color(self):
        color = self.new_color_entry.get().strip()
        if color:
            # Generate new color ID
            new_id = max(self.colors.keys(), default=0) + 1
            self.colors[new_id] = color
            
            # Save to file
            if Baca.simpan_file_warna("Data_Warna.txt", self.colors):
                messagebox.showinfo("Success", "Warna baru berhasil ditambahkan")
                self.new_color_entry.delete(0, tk.END)
                self.update_color_menu()
            else:
                messagebox.showerror("Error", "Gagal menyimpan warna baru")
        else:
            messagebox.showwarning("Warning", "Nama warna tidak boleh kosong")

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
