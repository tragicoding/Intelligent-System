#from openai.types.responses import Response
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

system_prompt = {
    "role" : "system",
    "content" : """
    You are a code debugger. Find the error, 
    explain it simply, and provide corrected code."""
}

message_memory = [system_prompt]

while True:
    question = input("Ask to AI: ")
    if question == "quit":
        break
    message_memory = [*message_memory , {"role": "user",\
                      "content":question}]
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = message_memory
    )
    ai_answer = response.choices[0].message.content
    print(f"AI: {ai_answer}")
    message_memory=[*message_memory, {
        "role" : "assistant",
        "content" : ai_answer
    }]

