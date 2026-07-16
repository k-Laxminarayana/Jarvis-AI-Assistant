from dotenv import load_dotenv
from groq import Groq
import os

# Load API key from .env
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

print("Jarvis V3 AI Brain Connected!")

messages = [
    {
        "role": "system",
        "content": "You are Jarvis, a helpful AI assistant. Remember the conversation during this chat."
    }
]

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