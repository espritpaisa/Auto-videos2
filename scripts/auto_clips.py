import os
import whisper

INPUT = "videos"
OUTPUT = "output"

os.makedirs(OUTPUT, exist_ok=True)

print("🔥 Sistema Millionaire Mindset iniciado")

# 🔥 modelo rápido
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
    elif "rico" in texto or "ricos" in texto:
        return "Así piensan los ricos"
    else:
        return "Esto puede cambiar tu mentalidad"


for file in os.listdir(INPUT):
    if file.lower().endswith((".mp4", ".mov", ".mkv")):
        input_path = os.path.join(INPUT, file)

        for i, start in enumerate([0, 20, 40]):

            clip_path = os.path.join(OUTPUT, f"{file}_clip_{i}.mp4")
            processed_path = os.path.join(OUTPUT, f"{file}_processed_{i}.mp4")
            srt_path = os.path.join(OUTPUT, f"{file}_clip_{i}.srt")
            final_path = os.path.join(OUTPUT, f"{file}_FINAL_{i}.mp4")

            print(f"✂️ Cortando clip {i}...")

            # 🔥 PASO 1: CORTE RÁPIDO (NO FALLA)
            os.system(
                f'ffmpeg -y -ss {start} -i "{input_path}" -t 18 -c copy "{clip_path}"'
            )

            print("🎥 Ajustando formato vertical...")

            # 🔥 PASO 2: FORMATO TIKTOK (AQUÍ YA PROCESAMOS)
            os.system(
                f'ffmpeg -y -i "{clip_path}" '
                f'-vf "scale=1080:-1:force_original_aspect_ratio=decrease,'
                f'pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" '
                f'-c:a copy "{processed_path}"'
            )

            print("🧠 Generando subtítulos...")

            result = model.transcribe(processed_path)
            texto_completo = result["text"]

            hook = generar_hook(texto_completo)
            print(f"🔥 Hook: {hook}")

            # 📝 CREAR SRT
            with open(srt_path, "w", encoding="utf-8") as f:
                for j, seg in enumerate(result["segments"]):
                    f.write(f"{j+1}\n")
                    f.write(f"{format_time(seg['start'])} --> {format_time(seg['end'])}\n")
                    f.write(f"{seg['text'].strip()}\n\n")

            print("🎬 Render final...")

            # 🔥 PASO 3: SUBTÍTULOS + HOOK
            os.system(
                f'ffmpeg -y -i "{processed_path}" '
                f'-vf "subtitles={srt_path},'
                f'drawtext=text=\'{hook}\':x=(w-text_w)/2:y=120:fontsize=50:fontcolor=white:box=1:boxcolor=black@0.5" '
                f'-c:a copy "{final_path}"'
            )

print("🚀 CLIPS LISTOS")
