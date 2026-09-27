import pyttsx3

engine = pyttsx3.init()

# make it sound a bit more natural
voices = engine.getProperty('voices')

# voices[0] is usually male, voices[1] is usually female
engine.setProperty('voice', voices[1].id)

engine.setProperty('rate', 150)    # speed, default is 200 which is too fast
engine.setProperty('volume', 1.0)  # max volume

def speak(text):
    engine.say(text)
    engine.runAndWait()
