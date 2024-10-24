import os

#class up:
#    def tambah_data(nama_file):
#        try:
#            with open(nama_file, 'r') as file:
#               lines = file.readlines()
#                last_id = max(int(line.split(':')[0]) for line in lines[1:] if ':' in line)
#        except FileNotFoundError:   
#            last_id = 0
#
#        value = input("Masukkan nama data: ")
#        new_id = last_id + 1

#        with open(nama_file, 'a') as file:
#            if not lines[-1].endswith('\n'):
#                file.write('\n')
#            file.write(f"{new_id}:{value}\n")
#        print(f"Data '{new_id}:{value}' berhasil ditambahkan ke {nama_file}")

# Fungsi untuk mendapatkan ID terakhir dari file
#    def baca_id_terakhir(nama_file):
#        if not os.path.exists(nama_file):
#            return 0
#        with open(nama_file, 'r') as file:
#            lines = file.readlines()
#            if len(lines) > 1:
#                last_line = lines[-1].strip()
#                if ':' in last_line:
#                    return int(last_line.split(':')[0])
#        return 0