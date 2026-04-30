import os

INPUT = "videos"
OUTPUT = "output"

os.makedirs(OUTPUT, exist_ok=True)

print("🔥 Iniciando procesamiento PRO")

for file in os.listdir(INPUT):
    if file.lower().endswith((".mp4", ".mov", ".mkv")):
        input_path = os.path.join(INPUT, file)

        # crear 3 clips por video
        for i, start in enumerate([0, 15, 30]):
            output_path = os.path.join(OUTPUT, f"{file}_clip_{i}.mp4")

            comando = f'ffmpeg -y -ss {start} -i "{input_path}" -t 15 -vf "scale=1080:1920,setsar=1" "{output_path}"'
            os.system(comando)

print("🚀 Clips listos")
