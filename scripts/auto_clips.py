import os
import whisper

INPUT = "videos"
OUTPUT = "output"

os.makedirs(OUTPUT, exist_ok=True)

print("🔥 Millionaire Mindset PRO System iniciado")

model = whisper.load_model("base")


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
    elif "rico" in texto or "ricos" in texto:
        return "Así piensan los ricos"
    elif "mentalidad" in texto:
        return "Esto puede cambiar tu mentalidad"
    else:
        return "Esto puede cambiar tu vida"


for file in os.listdir(INPUT):
    if file.lower().endswith((".mp4", ".mov", ".mkv")):
        input_path = os.path.join(INPUT, file)

        for i, start in enumerate([0, 20, 40]):

            clip_path = os.path.join(OUTPUT, f"{file}_clip_{i}.mp4")
            srt_path = os.path.join(OUTPUT, f"{file}_clip_{i}.srt")
            final_path = os.path.join(OUTPUT, f"{file}_FINAL_{i}.mp4")

            print(f"🎬 Creando clip {i}")

            # 🎥 1. VIDEO FORMATO TIKTOK PRO (SIN ESTIRAR)
            os.system(
                f'ffmpeg -y -ss {start} -i "{input_path}" -t 18 '
                f'-filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,'
                f'crop=1080:1920,boxblur=20:10[bg];'
                f'[0:v]scale=1080:-1:force_original_aspect_ratio=decrease[fg];'
                f'[bg][fg]overlay=(W-w)/2:(H-h)/2,'
                f'zoompan=z=\'min(zoom+0.001,1.3)\':d=1" '
                f'-c:a copy "{clip_path}"'
            )

            print("🧠 Generando subtítulos...")

            result = model.transcribe(clip_path)
            texto_completo = result["text"]

            hook = generar_hook(texto_completo)
            print(f"🔥 Hook: {hook}")

            # 📝 SRT
            with open(srt_path, "w", encoding="utf-8") as f:
                for j, seg in enumerate(result["segments"]):
                    f.write(f"{j+1}\n")
                    f.write(f"{format_time(seg['start'])} --> {format_time(seg['end'])}\n")
                    f.write(f"{seg['text'].strip()}\n\n")

            print("🔥 Aplicando estilo final")

            # 🎬 2. SUBTÍTULOS + HOOK (ESTILO MINIMALISTA PRO)
            os.system(
                f'ffmpeg -y -i "{clip_path}" '
                f'-vf "subtitles={srt_path}:force_style=\'Fontsize=42,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BorderStyle=1,Outline=3,Alignment=2\','
                f'drawtext=text=\'{hook}\':fontcolor=white:fontsize=60:box=1:boxcolor=black@0.5:'
                f'x=(w-text_w)/2:y=120" '
                f'-c:a copy "{final_path}"'
            )

print("🚀 SISTEMA PRO LISTO")
