from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


while True:
    question = input("Ask to AI: ")

    if question == "quit":
        break

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

