comando = f'ffmpeg -y -i "{input_path}" -t 15 -vf "scale=1080:1920,setsar=1" "{output_path}"'
