import os
import whisper

INPUT = "videos"
OUTPUT = "output"

os.makedirs(OUTPUT, exist_ok=True)

print("🔥 Sistema con subtítulos reales iniciado")

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

        for i, start in enumerate([0, 15, 30]):
            clip_path = os.path.join(OUTPUT, f"{file}_clip_{i}.mp4")
            srt_path = os.path.join(OUTPUT, f"{file}_clip_{i}.srt")
            final_path = os.path.join(OUTPUT, f"{file}_final_{i}.mp4")

            print(f"🎬 Creando clip {i}")

            # 1. cortar clip vertical
            os.system(
                f'ffmpeg -y -ss {start} -i "{input_path}" -t 15 '
                f'-vf "scale=1080:1920,setsar=1" "{clip_path}"'
            )

            print("🧠 Transcribiendo audio...")
            result = model.transcribe(clip_path)

            # 2. crear subtítulos SRT
            with open(srt_path, "w", encoding="utf-8") as f:
                for j, seg in enumerate(result["segments"]):
                    start_time = format_time(seg["start"])
                    end_time = format_time(seg["end"])
                    text = seg["text"].strip()

                    f.write(f"{j+1}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{text}\n\n")

            print("🔥 Pegando subtítulos al video")

            # 3. quemar subtítulos
            os.system(
                f'ffmpeg -y -i "{clip_path}" '
                f'-vf "subtitles={srt_path}:force_style=\'Fontsize=24,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BorderStyle=1,Outline=2\'" '
                f'"{final_path}"'
            )

print("🚀 Todo listo con subtítulos")
