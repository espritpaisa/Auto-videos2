import os
import whisper

INPUT = "videos"
OUTPUT = "output"

os.makedirs(OUTPUT, exist_ok=True)

print("🔥 Millionaire Mindset System iniciado")

# cargar modelo de subtítulos
model = whisper.load_model("base")

def format_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

for file in os.listdir(INPUT):
    if file.lower().endswith((".mp4", ".mov", ".mkv")):
        input_path = os.path.join(INPUT, file)

        # clips estratégicos (puedes ajustar luego)
        for i, start in enumerate([0, 20, 40]):
            
            clip_path = os.path.join(OUTPUT, f"{file}_clip_{i}.mp4")
            srt_path = os.path.join(OUTPUT, f"{file}_clip_{i}.srt")
            final_path = os.path.join(OUTPUT, f"{file}_FINAL_{i}.mp4")

            print(f"🎬 Creando clip {i}")

            # 1. VIDEO BASE (vertical + zoom + hook)
            os.system(
                f'ffmpeg -y -ss {start} -i "{input_path}" -t 15 '
                f'-vf "scale=1080:1920,zoompan=z=\'min(zoom+0.0015,1.5)\':d=1,'
                f'drawtext=text=\'Esto puede cambiar tu vida\':'
                f'fontcolor=white:fontsize=60:box=1:boxcolor=black@0.6:'
                f'x=(w-text_w)/2:y=100" '
                f'"{clip_path}"'
            )

            print("🧠 Generando subtítulos...")

            # 2. TRANSCRIPCIÓN
            result = model.transcribe(clip_path)

            with open(srt_path, "w", encoding="utf-8") as f:
                for j, seg in enumerate(result["segments"]):
                    start_time = format_time(seg["start"])
                    end_time = format_time(seg["end"])
                    text = seg["text"].strip()

                    f.write(f"{j+1}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{text}\n\n")

            print("🔥 Pegando subtítulos")

            # 3. VIDEO FINAL CON SUBTÍTULOS PRO
            os.system(
                f'ffmpeg -y -i "{clip_path}" '
                f'-vf "subtitles={srt_path}:force_style=\'Fontsize=36,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BorderStyle=1,Outline=3,Alignment=2\'" '
                f'"{final_path}"'
            )

print("🚀 Sistema terminado - clips listos para subir")
