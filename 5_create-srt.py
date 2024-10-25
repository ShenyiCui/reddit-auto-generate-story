import whisper
import ollama
from datetime import timedelta
from pathlib import Path
from whisper.utils import get_writer 

def create_srt(file_name, transcript):
    segments = transcript['segments']

    # delete the file if it already exists
    if Path(file_name).exists():
        Path(file_name).unlink()

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

        with open(file_name, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)
    print(f"\n****\nCreated {file_name}\n****")


# Load the model
model = whisper.load_model("turbo")

# for each audio clip, transcribe and create a srt file
curr_dir = Path(__file__).parent
audio_clips = curr_dir / "audio-clips"
for file_path in audio_clips.iterdir():
    if file_path.suffix != ".mp3":
        continue
    file_name = file_path.stem
    result = model.transcribe(audio=str(file_path))
    # Set SRT Line and words width
    word_options = {
        "highlight_words": False,
        "max_line_count": 1,
        "max_line_width": 5,
    }
    print("writing srt file")
    srt_writer = get_writer(output_format='srt', output_dir='./transcripts')
    srt_writer(result, file_path, word_options)
    # create_srt(curr_dir / f"transcripts/{file_name}.srt", result)
