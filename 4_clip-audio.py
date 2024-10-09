from pathlib import Path
from mutagen.mp3 import MP3
import subprocess
import shlex
import math

def get_mp3_duration(file_path):
    audio = MP3(file_path)
    return audio.info.length  # Duration in seconds

def split_audio(file_path, start_time, end_time, output_file, is_end):
   command = shlex.split(f"ffmpeg -y -i {file_path} -ss {start_time} -to {end_time} -c copy {output_file}")
   subprocess.run(command)
   if not is_end:
       # add silence to the end of the clip
       silence_file = Path(__file__).parent / "template-audios/next_part.mp3"
       new_output_file = output_file.parent / f"{output_file.stem}_next{output_file.suffix}"
       command = shlex.split(f"ffmpeg -y -i {output_file} -i {silence_file} -filter_complex '[0:0][1:0]concat=n=2:v=0:a=1[out]' -map '[out]' {new_output_file}")
       subprocess.run(command)
       command = shlex.split(f"mv {new_output_file} {output_file}")
       subprocess.run(command)

curr_dir = Path(__file__).parent
audio = curr_dir / "audio"
audio_clips = curr_dir / "audio-clips"
clip_size = 50
for file_path in audio.iterdir():
  if file_path.suffix == ".mp3":
    file = open(file_path, "r")
    file_name = file_path.stem
    # get the length of the audio file
    duration = get_mp3_duration(file_path)

    if duration < clip_size:
        continue
    
    div_val = 1
    while True: 
        if duration // div_val <= clip_size:
            break
        div_val += 1 
    clip_size = math.ceil(duration / div_val)
    
    num_clips = math.ceil(duration / clip_size)
    for i in range(int(num_clips)):
        end_time = (i + 1) * clip_size
        is_end = end_time > duration
        end_time = end_time if not is_end else duration
        split_audio(file_path, i * clip_size, (i + 1) * clip_size, audio_clips / f"{file_name}_{i}.mp3", is_end)

    file.close()
