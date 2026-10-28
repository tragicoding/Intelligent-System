from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

#Schema of OpenAI API : messages's data structure is "list"
message_memory=[]
client = OpenAI()   

while True:
    question = input("Ask to AI: ")
    if question == "quit":
        break

    # When user's input the prompt, new element what is dict.
    message_memory.append({"role" : "user", "content":question})
    
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = message_memory 
        #MUST request messages list that include all history
    )
    ai_message = response.choices[0].message.content
    print(f"AI: {ai_message}")

    #New Dict element about ai's response.
    #This data will be role of assistant
    message_memory.append({"role":"assistant", "content":ai_message})