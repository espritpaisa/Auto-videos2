import os
import whisper

INPUT = "videos"
OUTPUT = "output"

os.makedirs(OUTPUT, exist_ok=True)

print("🔥 Sistema iniciado")

model = whisper.load_model("tiny")


def format_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"


def generar_hook(texto):
    texto = texto.lower()

    if "dinero" in texto:
        return "Nadie te dice esto sobre el dinero"
    elif "éxito" in texto or "exito" in texto:
        return "Esto explica el verdadero éxito"
    else:
        return "Esto puede cambiar tu mentalidad"


for file in os.listdir(INPUT):
    if file.lower().endswith((".mp4", ".mov", ".mkv")):
        input_path = os.path.join(INPUT, file)

        for i, start in enumerate([0, 20, 40]):

            clip_path = os.path.join(OUTPUT, f"{file}_clip_{i}.mp4")
            srt_path = os.path.join(OUTPUT, f"{file}_clip_{i}.srt")
            final_path = os.path.join(OUTPUT, f"{file}_FINAL_{i}.mp4")

            print(f"🎬 Clip {i}")

            # 🎥 VIDEO BASE SIMPLE (ESTABLE)
            os.system(
                f'ffmpeg -y -ss {start} -i "{input_path}" -t 18 '
                f'-vf "scale=1080:-1,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" '
                f'-c:a copy "{clip_path}"'
            )

            print("🧠 Subtítulos...")

            result = model.transcribe(clip_path)
            hook = generar_hook(result["text"])

            # 📝 SRT
            with open(srt_path, "w", encoding="utf-8") as f:
                for j, seg in enumerate(result["segments"]):
                    f.write(f"{j+1}\n")
                    f.write(f"{format_time(seg['start'])} --> {format_time(seg['end'])}\n")
                    f.write(f"{seg['text'].strip()}\n\n")

            print("🔥 Render final")

            # 🎬 FINAL SIMPLE
            os.system(
                f'ffmpeg -y -i "{clip_path}" '
                f'-vf "subtitles={srt_path},'
                f'drawtext=text=\'{hook}\':x=(w-text_w)/2:y=100:fontsize=50:fontcolor=white:box=1:boxcolor=black@0.5" '
                f'"{final_path}"'
            )

print("🚀 Listo")
