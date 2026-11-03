from openai import OpenAI
from openai.types.responses import Response
from dotenv import load_dotenv

client = OpenAI()
load_dotenv()

messages = [
    {
        "role" : "system",
        "content": """
you are helpful AI assistant that searches for the
latest information to provide answer"""
    }
]

while True:
    question = input("Question: ")
    if question.lower() in ["quit","exit"]:
        print("Exiting chatbot")
        break
    messages.append({"role" : "user","content":question})

    try:
        response = client.responses.create(
            model = "gpt-4o",
            input = messages,
            tools = [
                {"type":"web_search",
                 "filters" : {
                     "allowed_domains": [
                         "sbs.co,kr","naver.com"
                     ],
                     "blocked_domains":[
                         "apnews.com"
                     ]
                 }
                 }
            ]
        )
        final_answer = response.output_text

        messages.append({"role":"assistant",
                         "content":final_answer})
        print(f"\nAI: {final_answer}")

    except Exception as e:
        print(f"\nError occured during API call:{e}\n")

    