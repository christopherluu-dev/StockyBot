import os
from gtts import gTTS

def get_TextToSpeech(message):
    tts = gTTS(text=message, lang='en')
    tts.save('resources/message.mp3')
