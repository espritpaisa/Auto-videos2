import os

INPUT = "videos"
OUTPUT = "output"

os.makedirs(OUTPUT, exist_ok=True)

print("🔥 Sistema rápido iniciado")

for file in os.listdir(INPUT):
    if file.lower().endswith((".mp4", ".mov", ".mkv")):
        input_path = os.path.join(INPUT, file)

        # generar 3 clips
        for i, start in enumerate([0, 15, 30]):
            output_path = os.path.join(OUTPUT, f"{file}_clip_{i}.mp4")

            print(f"🎬 Clip {i}")

            comando = (
                f'ffmpeg -y -ss {start} -i "{input_path}" -t 15 '
                f'-vf "scale=1080:1920,'
                f'drawtext=text=\'Si eres paisa esto te ha pasado\':'
                f'fontcolor=white:fontsize=60:box=1:boxcolor=black@0.5:'
                f'x=(w-text_w)/2:y=h-300" '
                f'"{output_path}"'
            )

            os.system(comando)

print("🚀 Clips listos")
