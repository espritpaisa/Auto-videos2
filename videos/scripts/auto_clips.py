import os

INPUT = "videos"
OUTPUT = "output"

os.makedirs(OUTPUT, exist_ok=True)

print("🔥 Script iniciado")

if not os.path.exists(INPUT):
    print("❌ No existe carpeta videos")
    exit(1)

files = os.listdir(INPUT)

if not files:
    print("❌ No hay archivos en videos")
    exit(1)

for file in files:
    if file.lower().endswith((".mp4", ".mov", ".mkv")):
        input_path = os.path.join(INPUT, file)
        output_path = os.path.join(OUTPUT, file + "_clip.mp4")

        print(f"🎬 Procesando: {input_path}")

        comando = f'ffmpeg -y -i "{input_path}" -t 10 "{output_path}"'
        print(comando)

        os.system(comando)

print("🚀 Script terminado")
