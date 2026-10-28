from openai.types.responses import Response
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

messages = [
    {
        "role": "system",
        "content": """
         You are a chef.
         **Only answer cooking-related questions**.
         If the question is not about cooking,say:
            "I can only help with cooking questions."
        """,
    }
]

question = "What is a Python??"
messages = [*messages, {"role": "user", "content": question}]
response: Response = client.responses.create(model="gpt-4o-mini", input=messages)
print(response.output_text)