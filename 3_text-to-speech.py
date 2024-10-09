from pathlib import Path
import ollama
from openai import OpenAI

client = OpenAI()

def get_model_voice(content):
  response = ollama.chat(
    model="llama3.1",
    messages=[
      {
        "role": "system",
        "content": "Read the text and determine if it's a male or female voice. " + 
        "IF it is a female voice and you think the speaker is young then return 'nova'. " +
        "IF it is a female voice and you think the speaker is older then return 'shimmer'. " +
        "IF it is a male voice and you think the speaker is young then return 'echo'. " + 
        "IF it is a male voice and you think the speaker is older then return 'onyx'. " +
        "For Context If the speaker is in their teems to 20s then they are young. If they are in their 30s to 40s then they are older. " +
        "DO NOT return anything else except for the voice name."
      },
      {"role": "user", "content": content},
    ]
  )
  res = response["message"]["content"]
  if res != "nova" and res != "shimmer" and res != "echo" and res != "onyx":
    return 'alloy'
  return res


# for each file under ./stories, read the content and convert it to speech
curr_dir = Path(__file__).parent
stories_dir = curr_dir / "stories"
for file_path in stories_dir.iterdir():
  file = open(file_path, "r")
  # get file name without extension
  file_name = file_path.stem
  speech_file_path = curr_dir / f"audio/{file_name}.mp3"

  content = file.read()
  voice = get_model_voice(content)
  response = client.audio.speech.create(
    model="tts-1",
    voice=voice,
    input=content
  )

  response.stream_to_file(speech_file_path)
  file.close()
