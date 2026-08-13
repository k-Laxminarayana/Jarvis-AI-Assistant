from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

import os
import webbrowser
import speech_recognition as sr
import edge_tts
import asyncio
from playsound import playsound
# Load API Keys
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

client = Groq(api_key=GROQ_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)
# -----------------------------
# Voice Output
# -----------------------------
async def speak_async(text):
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-AriaNeural"
    )
    await communicate.save("voice.mp3")


def speak(text):
    print(f"Jarvis: {text}")

    asyncio.run(speak_async(str(text)))

    playsound("voice.mp3")

    if os.path.exists("voice.mp3"):
        os.remove("voice.mp3")


# -----------------------------
# Voice Input
# -----------------------------
def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        speak("I'm listening.")
        print("🎤 Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text

    except Exception:
        speak("Sorry, I couldn't understand.")
        return ""
    
    # -----------------------------
# AI Memory
# -----------------------------
messages = [
    {
        "role": "system",
        "content": (
            "You are Jarvis, a helpful AI assistant. "
            "Answer clearly and naturally. "
            "Remember the conversation during this chat."
        )
    }
]


# -----------------------------
# Internet Search
# -----------------------------
def search_internet(query):
    try:
        result = tavily.search(
            query=query,
            max_results=3
        )

        return result["results"]

    except Exception:
        return []


print("===================================")
print("   Jarvis V6 Stable is Ready!")
print("===================================")

while True:

    question = listen()

    if question == "":
        continue

    question = question.lower()

    # Exit
    if "bye" in question or "goodbye" in question or "exit" in question or "stop" in question:
        speak("Goodbye! Have a nice day.")
        break

    # Open Apps
    if "open chrome" in question:
        speak("Opening Chrome")
        webbrowser.open("https://www.google.com")
        continue

    elif "open youtube" in question:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        continue

    elif "open google" in question:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
        continue

    elif "open gmail" in question:
        speak("Opening Gmail")
        webbrowser.open("https://mail.google.com")
        continue

    elif "open github" in question:
        speak("Opening GitHub")
        webbrowser.open("https://github.com")
        continue

    elif "open calculator" in question:
        speak("Opening Calculator")
        os.system("calc")
        continue

    elif "open notepad" in question:
        speak("Opening Notepad")
        os.system("notepad")
        continue

    elif "open paint" in question:
        speak("Opening Paint")
        os.system("mspaint")
        continue

    elif "open file explorer" in question:
        speak("Opening File Explorer")
        os.system("explorer")
        continue

    elif "open settings" in question:
        speak("Opening Settings")
        os.system("start ms-settings:")
        continue

    elif "open command prompt" in question or "open cmd" in question:
        speak("Opening Command Prompt")
        os.system("start cmd")
        continue

    elif "open vscode" in question or "open vs code" in question:
        speak("Opening VS Code")
        os.system("code")
        continue

    # Internet Search
    internet = search_internet(question)

    messages.append({
        "role": "system",
        "content": f"Latest internet information: {internet}"
    })

    messages.append({
        "role": "user",
        "content": question
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    reply = response.choices[0].message.content

    speak(reply)

    messages.append({
        "role": "assistant",
        "content": reply
    })