import os

INPUT = "videos"
OUTPUT = "output"

os.makedirs(OUTPUT, exist_ok=True)

print("🔥 Script iniciado")

# Verificar carpeta videos
if not os.path.exists(INPUT):
    print("❌ La carpeta 'videos' no existe")
    exit(1)

files = os.listdir(INPUT)

if len(files) == 0:
    print("❌ No hay archivos en la carpeta videos")
    exit(1)

for file in files:
    if file.endswith(".mp4"):
        input_path = os.path.join(INPUT, file)
        output_path = os.path.join(OUTPUT, file.replace(".mp4", "_clip.mp4"))

        print(f"🎬 Procesando: {input_path}")

        comando = f'ffmpeg -y -i "{input_path}" -t 10 "{output_path}"'
        resultado = os.system(comando)

        if resultado != 0:
            print(f"❌ Error procesando {file}")
        else:
            print(f"✅ Clip creado: {output_path}")

print("🚀 Script terminado")
