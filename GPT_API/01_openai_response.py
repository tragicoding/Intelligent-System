
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

question = "Hello How are you?"

response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages = [
        {
            "role" : "user",
            "content" : question
        }
    ]
)

print(response.choices[0].message.content)