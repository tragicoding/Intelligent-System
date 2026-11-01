from openai.types.responses import Response
import json
from openai.types.chat import ChatCompletion
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

SYSTEM_PROMPT = {
    "role": "system",
    "content": """
    You have access to the following functions:
    - add(a, b)
    - subtract(a, b)
    - multiply(a, b)
    - divide(a, b)

    If a user's question can be solved using these functions,
    respond ONLY by calling the appropriate function(s),
    with no additional text, explanation, or formatting.
    
    Examples:
    User: What is the capital of the Republic of Korea?
    AI: The capital of the Republic of Korea is Seoul.
    User: What is 4 + 5?
    AI: add(4,5)
    User: What is 5 * 2 + 5 / 4?
    AI: add(multiply(5,2), divide(5,4))
    """,
}

messages = [SYSTEM_PROMPT]
question = input("Ask math to AI: ")
messages.append({"role": "user", "content": question})

client = OpenAI()

response: Response = client.responses.create(
    model="gpt-4o",
    input=messages,
)

print(response.output_text)
