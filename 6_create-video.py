from pathlib import Path
from mutagen.mp3 import MP3
import subprocess
import shlex
import random
import math
from moviepy.editor import VideoFileClip


def get_video_duration_moviepy(video_path):
    """
    Returns the duration of a video file in seconds using MoviePy.

    :param file_path: Path to the video file.
    :return: Duration in seconds.
    """
    try:
        # Ensure the path is a string
        if isinstance(video_path, Path):
            video_path = str(video_path)
        
        clip = VideoFileClip(video_path)
        duration = clip.duration  # Duration in seconds
        clip.reader.close()
        if clip.audio:
            clip.audio.reader.close_proc()
        return duration
    except Exception as e:
        print(f"Error: {e}")
        return None

def convert_seconds_to_hhmmss(seconds):
    seconds = math.ceil(seconds)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def get_mp3_duration(file_path):
    audio = MP3(file_path)
    return audio.info.length  # Duration in seconds

def trim_video(video_file, start_time, end_time, output_file):
    temp_output_file = output_file.parent / f"{output_file.stem}_temp{output_file.suffix}"  
    command = shlex.split(f"ffmpeg -y -ss {start_time} -to {end_time} -i {video_file} -c copy {temp_output_file}")
    subprocess.run(command)
    command = shlex.split(f"mv {temp_output_file} {output_file}")
    subprocess.run(command)

def burn_subtitles(video_file, srt_file, output_file):
    temp_output_file = output_file.parent / f"{output_file.stem}_temp{output_file.suffix}"  
    command = shlex.split(f"ffmpeg -y -i {video_file} -vf \"subtitles={srt_file}:force_style='Alignment=10,FontName=Lato'\" {temp_output_file}")
    subprocess.run(command)
    command = shlex.split(f"mv {temp_output_file} {output_file}")
    subprocess.run(command)

# ffmpeg -i subtitled_output.mp4 -i aith_1.mp3 -map 0:v -map 1:a -c:v copy -shortest audio_output.mp4
def burn_audio(video_file, audio_file, output_file):
    temp_output_file = output_file.parent / f"{output_file.stem}_temp{output_file.suffix}"  
    command = shlex.split(f"ffmpeg -y -i {video_file} -i {audio_file} -map 0:v -map 1:a -c:v copy -c:a copy -shortest {temp_output_file}")
    subprocess.run(command)
    command = shlex.split(f"mv {temp_output_file} {output_file}")
    subprocess.run(command)

curr_dir = Path(__file__).parent
audio_clips = curr_dir / "audio-clips"
template_videos = curr_dir / "template-videos"
output_dir = curr_dir / "output"
_map = {}
for audio_clip in audio_clips.iterdir():
    if audio_clip.suffix != ".mp3":
        continue
    audio_clip_name = audio_clip.stem
    audio_clip_duration = get_mp3_duration(audio_clip)
    # get all videos in the template-videos directory and store them in a list

    template_video = ""
    video_name_prefix = audio_clip_name.split("_")[0]
    if video_name_prefix in _map:
        template_video = _map[video_name_prefix]
    else:
        template_videos_list = list(template_videos.iterdir())
        # get a random video from the list
        template_video = random.choice(template_videos_list)
        _map[video_name_prefix] = template_video

    print(template_video)
    video_duration = get_video_duration_moviepy(template_video)
    # randomly pick a start time between 0 and video_duration - (audio_clip_duration + 1)
    start_time = random.randint(0, int(video_duration - (audio_clip_duration + 1)))
    end_time = start_time + audio_clip_duration + 1
    output_file = output_dir / f"{audio_clip_name}.mp4"
    trim_video(template_video, convert_seconds_to_hhmmss(start_time), convert_seconds_to_hhmmss(end_time), output_file)
    burn_subtitles(output_file, curr_dir / f"transcripts/{audio_clip_name}.srt", output_file)
    burn_audio(output_file, audio_clip, output_file)
    print(f"Created {output_file}")