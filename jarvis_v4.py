from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient
import os

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