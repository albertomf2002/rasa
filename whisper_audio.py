import whisper
import io
import os
import pyttsx3
import tempfile
import speech_recognition as sr
from pydub import AudioSegment

from rasa.core.agent import Agent
import asyncio

file = tempfile.mkdtemp()
path = os.path.join(file, 'temp.wav')

listener = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('rate', 145)
engine.setProperty('voice', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
             print("Say something...")
             listener.adjust_for_ambient_noise(source)
             audio = listener.listen(source)
             data = io.BytesIO(audio.get_wav_data())
             audio_clip = AudioSegment.from_file(data)
             audio_clip.export(path, format='wav')
    except Exception as e:
            print(e)

    return path

def recognize_audio(path):
    model = whisper.load_model("base")
    transcription = model.transcribe(path, language="spanish", fp16=False)
    return transcription["text"]

async def chat_with_bot(agent, message):
    responses = await agent.handle_text(message)
    print("------------ ", responses, " ------------")
    for response in responses:
        if 'text' in response:
            print("Bot:", response['text'])
            talk(response['text'])
        else:
            print("No te entendí")

async def load_agent():
    agent = Agent.load('models/20240502-110209-balanced-quay.tar.gz')
    return agent

async def main():
    agent = await load_agent()
    print("Puedes empezar a hablar con el bot (di 'terminar' para finalizar el programa).")
    while True:
        message = recognize_audio(listen())
        if message:
            print("Usuario:" + message)
            if message.lower().__contains__('terminar'):
                talk("Finalizar programa")
                break
            else:
                await chat_with_bot(agent, message)

async def test():
    agent = await load_agent()
    message = "Dime la hora"
    #message = "Hola"
    print("Executing...1/2")
    responses = await agent.handle_text(message)
    print("Executing...2/2")
    print(responses)

if __name__ == "__main__":
    #asyncio.run(main())
    asyncio.run(test())