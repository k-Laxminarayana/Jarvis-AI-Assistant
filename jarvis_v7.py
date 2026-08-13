from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

import os
import webbrowser
import speech_recognition as sr
import edge_tts
import asyncio
from playsound import playsound
from urllib.parse import quote
import pyautogui
import yt_dlp
from datetime import datetime
import psutil
import psutil

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

def play_youtube(query):
    ydl_opts = {
        "quiet": True,
        "default_search": "ytsearch1",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)

        video = info["entries"][0]

        webbrowser.open(video["webpage_url"])

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
    elif "screenshot" in question.lower():
        speak("Taking a screenshot.")

        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")

        speak("Screenshot saved successfully.")
        continue

    elif "time" in question:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
        continue

    elif "date" in question:
        current_date = datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {current_date}.")
        continue
    elif "battery" in question:
        battery = psutil.sensors_battery()

        if battery:
            percent = int(battery.percent)
            charging = battery.power_plugged

            if charging:
                speak(f"Your battery is at {percent} percent and is charging.")
            else:
                speak(f"Your battery is at {percent} percent.")
        else:
            speak("I couldn't read the battery status.")

        continue

    elif "pause" in question:
        speak("Pausing.")
        pyautogui.press("playpause")
        continue

    elif "search google" in question or "search" in question:
        search_query = question

        if "search google" in search_query:
            search_query = search_query.replace("search google", "", 1).strip()
        else:
            search_query = search_query.replace("search", "", 1).strip()

        if search_query:
            speak(f"Searching Google for {search_query}.")
            webbrowser.open(
            "https://www.google.com/search?q=" + quote(search_query)
        )
        else:
            speak("What would you like me to search for?")

        continue

    elif "play" in question:
        speak("Playing.")
        pyautogui.press("playpause")
        continue

    elif "next song" in question or "next track" in question:
        speak("Playing the next track.")
        pyautogui.press("nexttrack")
        continue

    elif "previous song" in question or "previous track" in question:
        speak("Playing the previous track.")
        pyautogui.press("prevtrack")
        continue

    
    
    elif question.startswith("play "):
        song = question.replace("play", "", 1).strip()

        speak(f"Playing {song}")

        play_youtube(song)

        continue
        song = question.replace("play", "", 1).strip()

        speak(f"Playing {song} on YouTube")

        webbrowser.open(
        f"https://www.youtube.com/results?search_query={quote(song)}"
        )
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

    elif "open github" in question:
        speak("Opening GitHub")
        webbrowser.open("https://github.com")
        continue

    elif "open download" in question or "open downloads" in question:
        speak("Opening Downloads.")
        os.startfile(os.path.join(os.path.expanduser("~"), "Downloads"))
        continue

    elif "create folder" in question or "create a folder" in question:
        folder_name = question.replace("create a folder", "").replace("create folder", "").strip()

        if folder_name:
            folder_path = os.path.join(
            os.path.expanduser("~"),
            "Desktop",
            folder_name
        )

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                speak(f"Folder {folder_name} created on your Desktop.")
            else:
                speak(f"The folder {folder_name} already exists.")
        else:
            speak("Please tell me the folder name.")

        continue

    elif "click" in question.lower():
        speak("Clicking.")
        pyautogui.click()
        continue


    # V7 - Website Commands
    elif "open linkedin" in question:
        speak("Opening LinkedIn.")
        webbrowser.open("https://www.linkedin.com")
        continue

    elif "open instagram" in question:
        speak("Opening Instagram.")
        webbrowser.open("https://www.instagram.com")
        continue

    elif "open chatgpt" in question:
        speak("Opening ChatGPT.")
        webbrowser.open("https://chatgpt.com")
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

    elif "take screenshot" in question:
        speak("Taking screenshot")

        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")

        speak("Screenshot saved successfully.")
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