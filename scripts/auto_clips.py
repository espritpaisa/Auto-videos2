import os

INPUT = "videos"
OUTPUT = "output"

os.makedirs(OUTPUT, exist_ok=True)

print("🔥 Iniciando procesamiento")

for file in os.listdir(INPUT):
    if file.lower().endswith((".mp4", ".mov", ".mkv")):
        input_path = os.path.join(INPUT, file)
        output_path = os.path.join(OUTPUT, file + "_clip.mp4")

        print(f"🎬 Procesando: {file}")

        # clip de 10 segundos desde el inicio
        comando = f'ffmpeg -y -i "{input_path}" -t 10 "{output_path}"'
        os.system(comando)

print("✅ Proceso terminado")
