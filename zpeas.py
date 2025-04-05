import os

# Değiştirmek istediğiniz dizinin yolu
# Bu kısmı kendi dizininizle değiştirin
folder_path = r'C:\Users\aycaa\OneDrive\Masaüstü\drive_fotolar\yenitrain\label\train'

# Dizindeki tüm dosyaları listele

for filename in os.listdir(folder_path):
    if 'peas' in filename:
        file_path = os.path.join(folder_path, filename)

        # Dosyayı oku ve güncelle
        with open(file_path, 'r') as file:
            lines = file.readlines()

        updated_lines = []
        for line in lines:
            parts = line.strip().split()
            if parts and parts[0] == '19':  # Class ID 19 olanları değiştir
                parts[0] = '21'
            updated_lines.append(' '.join(parts))

        # Güncellenmiş içeriği dosyaya yaz
        with open(file_path, 'w') as file:
            file.write('\n'.join(updated_lines))

        print(f"Updated {file_path}")

print("Class ID değişimi tamamlandı!")
