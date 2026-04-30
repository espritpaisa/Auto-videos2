import os

INPUT = "videos"
OUTPUT = "output"

# Crear carpeta output si no existe
os.makedirs(OUTPUT, exist_ok=True)

print("🔥 Script iniciado")

# Revisar si hay videos
for file in os.listdir(INPUT):
    if file.endswith(".mp4"):
        print(f"Procesando: {file}")
        
        nombre = file.replace(".mp4", "")
        
        # Cortar primeros 10 segundos (más seguro)
        comando = f"ffmpeg -i {INPUT}/{file} -t 10 {OUTPUT}/{nombre}_clip.mp4"
        os.system(comando)

print("✅ Script terminado")
