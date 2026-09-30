import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)

engine.setProperty('rate', 150)    
engine.setProperty('volume', 1.0)  

def speak(text):
    engine.say(text)
    engine.runAndWait()
