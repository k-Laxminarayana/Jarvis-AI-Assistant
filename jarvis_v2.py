import datetime
import webbrowser
import os
import pyttsx3
import asyncio
import edge_tts
from playsound import playsound
import uuid
import speech_recognition as sr
import sys
print("Python:", sys.version)
print("Executable:", sys.executable)

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

async def edge_speak(text):
    filename = f"{uuid.uuid4()}.mp3"
    communicate = edge_tts.Communicate(text, "te-IN-ShrutiNeural")
    await communicate.save(filename)
    playsound(filename)
    os.remove(filename)

def speak(text):
    asyncio.run(edge_speak(text))

def take_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Listening...")
        speak("I am listening")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()

    except Exception:
        print("Sorry, I couldn't understand.")
        speak("Sorry, I couldn't understand.")
        return ""

print("🤖 Hello! I am Jarvis.")
speak("Hello! I am Jarvis.")

name = input("What is your name? ")
age = input("How old are you? ")
city = input("Which city are you from? ")
feeling = input("How are you today? ")

print("\n----- JARVIS REPORT -----")
print("Name :", name)
print("Age :", age)
print("City :", city)
print("Feeling :", feeling)

print("\nNice to meet you,", name)
print("I hope you have a wonderful day!")
print("Welcome to your own AI Assistant!")

current_time = datetime.datetime.now()

hour = current_time.hour

if hour < 12:
    print("🌅 Good Morning,", name)
elif hour < 18:
    print("☀️ Good Afternoon,", name)
else:
    print("🌙 Good Evening,", name)

print("Current Time:", current_time.strftime("%I:%M %p"))

print("Today's Date:", current_time.strftime("%d-%m-%Y"))

print("Testing voice")
speak("Testing voice")

while True:
    command = take_command()
    if command.lower() == "hello":
        print("Hello! Nice to meet you.")

    elif command.lower() == "time":
        print("Current Time:", current_time.strftime("%I:%M %p"))

    elif command.lower() == "date":
        print("Today's Date:", current_time.strftime("%d-%m-%Y"))

    elif command.lower() == "google":
        print("Opening Google...")
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif command.lower() == "youtube":
        print("Opening YouTube...")
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif command.lower() == "chatgpt":
        print("Opening ChatGPT...")
        speak("Opening ChatGPT")
        webbrowser.open("https://chat.openai.com")

    elif "notepad" in command.lower():
        print("Opening notepad...")
        speak("Opening notepad")
        os.system("notepad")

    elif "calculator" in command.lower():
        print("Opening Calculator...")
        speak("Opening Calculator")
        os.system("calc")

    elif "paint" in command.lower():
        print("Opening Paint...")
        speak("Opening Paint")
        os.system("mspaint")

   

    elif "exit" in command.lower() or "stop" in command.lower() or "goodbye" in command.lower():
        print("Goodbye!")
        speak("Goodbye! Have a nice day.")
        break

    else:
        print("Sorry, I don't understand that command yet.")
        speak("Sorry, I don't understand that command yet.")
        


