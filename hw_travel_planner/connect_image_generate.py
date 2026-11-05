from openai import OpenAI
from openai.types.responses import Response
from dotenv import load_dotenv

client = OpenAI()
load_dotenv()

messages = [
    {
        "role" : "system",
        "content" : "Generate Image"
    }
]

while True:
    question = input("Question: ")
    if question.lower() in ["quit","exciting"]:
        break
    messages.append({"role":"user",
                     "content":question})
    response = client.responses.create(
        model = "gpt-4o",
        input = messages,
        tools = [
            {"type" : "image_generation",
             "quality" : "low"}
        ]
    )

    messages.append({"role" : "assistant",
                    "content":response.output_text})

    #Display the Entire AI Response!!!!!
    print(response.output)
    