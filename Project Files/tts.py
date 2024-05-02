import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

# On Windows, for example, try selecting different voices
for voice in voices:
    print(f"ID: {voice.id} | Name: {voice.name} | Languages: {voice.languages} | Gender: {voice.gender}")
    engine.setProperty('voice', voice.id)  # Set voice
    engine.say("This is a test.")
    engine.runAndWait()


def text_to_speech(text):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()
    
    # Set properties before adding anything to speak
    # You can set the rate, volume, and voice properties of the engine here
    # engine.setProperty('rate', 150)  # Speed percent (can go over 100)
    # engine.setProperty('volume', 0.9)  # Volume 0-1

    # Adding text to the queue
    engine.say(text)
    
    # Blocks while processing all the commands in the queue
    engine.runAndWait()

# Input text
text = input("Enter text to read aloud: ")
text_to_speech(text)

