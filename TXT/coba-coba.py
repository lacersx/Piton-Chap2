import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class Baca:
    @staticmethod
    def baca_file_warna(lokasi_file):
        default_colors = {
            1: "Merah",
            2: "Hijau",
            3: "Biru",
            4: "Kuning",
            5: "Orange"
        }
        
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
                    else:
                        print(f"Skipping invalid line: '{line}'")
                
                return color_data if color_data else default_colors
        except FileNotFoundError:
            print(f"File {lokasi_file} tidak ditemukan. Menggunakan data warna default.")
            return default_colors

    @staticmethod
    def baca_file_makanan(lokasi_file):
        default_foods = [
            {"id": 1, "name": "Nasi", "category_id": 4, "color_id": 1},
            {"id": 2, "name": "Ayam Goreng", "category_id": 1, "color_id": 3},
            {"id": 3, "name": "Sayur Bayam", "category_id": 2, "color_id": 2}
        ]
        
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
                
                return food_data if food_data else default_foods
        except FileNotFoundError:
            print(f"File {lokasi_file} tidak ditemukan. Menggunakan data makanan default.")
            return default_foods

class FoodApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Data Management")
        self.root.geometry("800x600")

        # Initialize transaction history
        self.transaction_history = []

        # Load data with default values
        self.colors = Baca.baca_file_warna("Data_Warna.txt")
        self.foods = Baca.baca_file_makanan("Data_Makanan.txt")
        self.categories = {
            1: "Protein",
            2: "Mineral",
            3: "Snack",
            4: "Karbohidrat",
            5: "Segar"
        }

        # Setup UI
        self.setup_ui()
        self.update_listbox()

    def setup_ui(self):
        # Food List Frame
        self.food_list_frame = tk.Frame(self.root, bg="#bdb2ff", bd=2, relief="groove")
        self.food_list_frame.place(x=20, y=20, width=300, height=500)
        
        tk.Label(self.food_list_frame, text="Tampilan Data Makanan", bg="#bdb2ff", font=("Arial", 12, "bold")).pack()
        self.food_listbox = tk.Listbox(self.food_list_frame)
        self.food_listbox.pack(fill="both", expand=True)
        
        # Control buttons
        tk.Button(self.food_list_frame, text="Tambah Data Makanan", command=self.add_food).pack(pady=5)
        tk.Button(self.food_list_frame, text="Edit Data Makanan", command=self.edit_food).pack(pady=5)
        tk.Button(self.food_list_frame, text="Hapus Data Makanan", command=self.delete_food).pack(pady=5)

        # Add Food Frame
        self.add_food_frame = tk.Frame(self.root, bg="#bdb2ff", bd=2, relief="groove")
        self.add_food_frame.place(x=350, y=20, width=400, height=250)
        
        tk.Label(self.add_food_frame, text="Tambah Data Makanan", bg="#bdb2ff", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Food input fields
        tk.Label(self.add_food_frame, text="Nama Makanan:").pack()
        self.food_name_entry = tk.Entry(self.add_food_frame)
        self.food_name_entry.pack()

        # Color dropdown
        tk.Label(self.add_food_frame, text="Warna:").pack()
        self.food_color_var = tk.StringVar()
        self.food_color_menu = tk.OptionMenu(self.add_food_frame, self.food_color_var, *self.colors.values())
        self.food_color_menu.pack()

        # Category dropdown
        tk.Label(self.add_food_frame, text="Kategori:").pack()
        self.food_category_var = tk.StringVar()
        self.food_category_menu = tk.OptionMenu(self.add_food_frame, self.food_category_var, *self.categories.values())
        self.food_category_menu.pack()

        tk.Button(self.add_food_frame, text="Simpan", command=self.save_food).pack(pady=10)

    def update_listbox(self):
        self.food_listbox.delete(0, tk.END)
        for food in self.foods:
            category_name = self.categories.get(food['category_id'], 'Unknown Category')
            color_name = self.colors.get(food['color_id'], 'Unknown Color')
            self.food_listbox.insert(tk.END, f"{food['name']} - {category_name} - {color_name}")

    def get_id_by_value(self, dictionary, value):
        for key, val in dictionary.items():
            if val == value:
                return key
        return None

    def save_food(self):
        name = self.food_name_entry.get()
        color = self.food_color_var.get()
        category = self.food_category_var.get()
        
        if name and color and category:
            color_id = self.get_id_by_value(self.colors, color)
            category_id = self.get_id_by_value(self.categories, category)
            
            new_id = max([food['id'] for food in self.foods], default=0) + 1
            
            new_food = {
                "id": new_id,
                "name": name,
                "category_id": category_id,
                "color_id": color_id
            }
            
            self.foods.append(new_food)
            self.update_listbox()
            
            # Clear inputs
            self.food_name_entry.delete(0, tk.END)
            self.food_color_var.set('')
            self.food_category_var.set('')
            
            messagebox.showinfo("Success", "Data makanan berhasil disimpan.")
        else:
            messagebox.showwarning("Error", "Semua field harus diisi!")

    def add_food(self):
        self.food_name_entry.delete(0, tk.END)
        self.food_color_var.set(list(self.colors.values())[0])
        self.food_category_var.set(list(self.categories.values())[0])

    def edit_food(self):
        selected = self.food_listbox.curselection()
        if selected:
            index = selected[0]
            food = self.foods[index]
            
            self.food_name_entry.delete(0, tk.END)
            self.food_name_entry.insert(0, food['name'])
            self.food_color_var.set(self.colors[food['color_id']])
            self.food_category_var.set(self.categories[food['category_id']])
            
            # Remove the old entry
            self.foods.pop(index)
            self.update_listbox()
        else:
            messagebox.showwarning("Selection Error", "Pilih makanan untuk diedit.")

    def delete_food(self):
        selected = self.food_listbox.curselection()
        if selected:
            index = selected[0]
            food = self.foods.pop(index)
            self.update_listbox()
            
            # Record transaction
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.transaction_history.append(
                f"{timestamp} - Deleted: {food['name']} - "
                f"{self.categories[food['category_id']]} - "
                f"{self.colors[food['color_id']]}"
            )
            
            messagebox.showinfo("Success", "Data makanan berhasil dihapus.")
        else:
            messagebox.showwarning("Selection Error", "Pilih makanan untuk dihapus.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FoodApp(root)
    root.mainloop()