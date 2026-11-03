from openai import OpenAI
from openai.types.responses import Response
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

messages = [
    {
        "role" : "system",
        "content": """
you are helpful AI assistant that searches for the
latest information to provide answer"""
    }
]

while True:
    question = input("Ask to AI: ")
    if question.lower() == "quit":
        print("Exiting chatbot")
        break
    messages.append({"role":"user","content":question})
    response: Response = client.responses.create(
        model = "gpt-4o-mini",
        input = messages
    )

    final_answer = response.output_text

    #memory for history about previous conversation
    messages.append({"role":"assistant","content":final_answer})
    print("\n AI: ",final_answer)