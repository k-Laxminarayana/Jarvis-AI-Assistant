from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient
import os
import webbrowser

# Load API key from .env
load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

print("Jarvis V3 AI Brain Connected!")

messages = [
    {
        "role": "system",
        "content": "You are Jarvis, a helpful AI assistant. Remember the conversation during this chat."
    }
]

def search_internet(query):
    result = tavily.search(query=query, max_results=3)
    return result["results"]

while True:
    question = input("You: ")

    if "open chrome" in question.lower():
        print("Jarvis: Opening Chrome...")
        webbrowser.open("https://www.google.com")
        continue
    if "open calculator" in question.lower():
        print("Jarvis: Opening Calculator...")
        os.system("calc")
        continue
    if "open notepad" in question.lower():
        print("Jarvis: Opening Notepad...")
        os.system("notepad")
        continue
    if "open file explorer" in question.lower():
        print("Jarvis: Opening File Explorer...")
        os.system("explorer")
        continue
    if "open paint" in question.lower():
        print("Jarvis: Opening Paint...")
        os.system("mspaint")
        continue
    if "open settings" in question.lower():
        print("Jarvis: Opening Settings...")
        os.system("start ms-settings:")
        continue
    if "open command prompt" in question.lower() or "open cmd" in question.lower():
        print("Jarvis: Opening Command Prompt...")
        os.system("start cmd")
        continue
    if "open vscode" in question.lower() or "open vs code" in question.lower():
        print("Jarvis: Opening VS Code...")
        os.system("code")
        continue
    if "open youtube" in question.lower():
        print("Jarvis: Opening YouTube...")
        webbrowser.open("https://www.youtube.com")
        continue
    if "open google" in question.lower():
        print("Jarvis: Opening Google...")
        webbrowser.open("https://www.google.com")
        continue
    if "open gmail" in question.lower():
        print("Jarvis: Opening Gmail...")
        webbrowser.open("https://mail.google.com")
        continue
    if "open github" in question.lower():
        print("Jarvis: Opening GitHub...")
        webbrowser.open("https://github.com")
        continue

    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    if question.lower() == "exit":
        print("Goodbye!")
        break

    internet_result = search_internet(question)

    messages.append(
        {
        "role": "system",
        "content": f"Latest internet information: {internet_result}"
        }
    )

    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages
)

    print("Jarvis:", response.choices[0].message.content)

    messages.append(
    {
        "role": "assistant",
        "content": response.choices[0].message.content
    }
)