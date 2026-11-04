from openai.types.responses import Response
import json
from openai.types.chat import ChatCompletion
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = {
    "role": "system",
    "content": """
        You are a Fields Medal–winning mathematician.
        Answer the user's math questions with rigorous reasoning,
        clear intuition, and elegant solutions.
    """,
}

messages = [SYSTEM_PROMPT]
question = input("Ask to AI: ")
messages.append({"role" : "user","content":question})
response: Response = client.responses.create(
    model = "gpt-4o-mini",
    input = messages

)
print(response.output_text)