import os
import whisper

INPUT = "videos"
OUTPUT = "output"

os.makedirs(OUTPUT, exist_ok=True)

print("🔥 Millionaire Mindset System iniciado")

# cargar modelo
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
    elif "fracaso" in texto:
        return "La razón por la que la mayoría fracasa"
    elif "rico" in texto or "ricos" in texto:
        return "Así piensan los ricos"
    elif "mentalidad" in texto:
        return "Esto puede cambiar tu mentalidad"
    else:
        return "Esto puede cambiar tu vida"


for file in os.listdir(INPUT):
    if file.lower().endswith((".mp4", ".mov", ".mkv")):
        input_path = os.path.join(INPUT, file)

        # clips base
        for i, start in enumerate([0, 20, 40]):

            clip_path = os.path.join(OUTPUT, f"{file}_clip_{i}.mp4")
            srt_path = os.path.join(OUTPUT, f"{file}_clip_{i}.srt")
            final_path = os.path.join(OUTPUT, f"{file}_FINAL_{i}.mp4")

            print(f"🎬 Creando clip {i}")

            # 1. crear clip base (sin texto aún)
            os.system(
                f'ffmpeg -y -ss {start} -i "{input_path}" -t 18 '
                f'-vf "scale=1080:1920,zoompan=z=\'min(zoom+0.0015,1.5)\':d=1" '
                f'"{clip_path}"'
            )

            print("🧠 Generando subtítulos...")

            # 2. transcribir
            result = model.transcribe(clip_path)
            texto_completo = result["text"]

            # generar hook dinámico
            hook = generar_hook(texto_completo)
            print(f"🔥 Hook generado: {hook}")

            # 3. crear archivo SRT
            with open(srt_path, "w", encoding="utf-8") as f:
                for j, seg in enumerate(result["segments"]):
                    start_time = format_time(seg["start"])
                    end_time = format_time(seg["end"])
                    text = seg["text"].strip()

                    f.write(f"{j+1}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{text}\n\n")

            print("🔥 Aplicando subtítulos y hook")

            # 4. video final con subtítulos + hook
            os.system(
                f'ffmpeg -y -i "{clip_path}" '
                f'-vf "subtitles={srt_path}:force_style=\'Fontsize=36,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BorderStyle=1,Outline=3,Alignment=2\','
                f'drawtext=text=\'{hook}\':fontcolor=white:fontsize=60:box=1:boxcolor=black@0.6:'
                f'x=(w-text_w)/2:y=100" '
                f'"{final_path}"'
            )

print("🚀 Sistema terminado - clips listos para subir")
