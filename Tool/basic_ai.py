from openai.types.responses import Response
import json
from openai.types.chat import ChatCompletion
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


messages = []
question = input("Ask math to AI: ")
messages.append({"role": "user", "content": question})

client = OpenAI()

response: Response = client.responses.create(
    model="gpt-4o",
    input=messages,
)

print(response.output_text)
