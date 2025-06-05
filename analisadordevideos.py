import pytubefix
import ffmpeg
import openai 

client = openai.OpenAI(api_key="Chave API da OpenAI")

import sys

if len(sys.argv) < 2:
    print("Uso: python analisadordevideos.py <URL do vídeo>")
    sys.exit(1)
url = sys.argv[1]
filename = "audio.wav"
yt = pytubefix.YouTube(url)
stream = yt.streams.filter(only_audio=True).first().url
ffmpeg.input(stream).output(filename, format='wav', loglevel='error').run(overwrite_output=True)


audio_file = open(filename, "rb")
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
).text

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system",
         "content": """
            Você é um assistente que faz resumos videos detalhados do Youtube
            Responda com formatação Markdown
            """},

        {"role": "user",
        "content": f"Descreva o seguinte vídeo do Youtube: {transcript}"}
    ])

print("Transcrição:", transcript)
print("Resumo:", completion.choices[0].message.content)

with open(f"resumo.md", "w+") as md:
    md.write(completion.choices[0].message.content)

