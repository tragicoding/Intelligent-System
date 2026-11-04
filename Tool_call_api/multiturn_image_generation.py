from dotenv import load_dotenv
from openai import OpenAI
from openai.types.resposnes import Response
import base64

load_dotenv()
client = OpenAI()

messages = [{
    "role" : "system",
    "content" : "image generation"
}]

question = input("Ask to AI")
messages.append({"role" : "user",
                 "content":question})
response = client.responses.create(
    model = "gpt-4o-mini",
    input = messages,
    tools = [
        {
            "type" : "image_generation",
            "quality" : "low"
        }
    ]
)

#The response id in openai server.
#If you use response id, AI can reference previous response
response_id = response.id

for output in response.output:
    if output.type == "message":
        ai_message = output.content[0].text
        messages.append({
            "role" : "assistant",
            "content" : ai_message
        })

    elif output.type == "image_generation_call":
        image_base64 = output.result

        #---------Loop : user's satisfiy---------
        while True:
            #Ask for feedback until The user is satified with the image
            filename = input("your image name: ")
            with open(f"{filename}","wb") as f:
                f.write(base64.b64decode(image_base64))
            user_feedback = input("\
                Review and enter revision feedback or exit")
            
            if user_feedback == "exit":
                pass

            #if user is unsatisfied, retry
            else:
                messages.append({
                    "role" : "user",
                    "content" : user_feedback
                })
                feedback_response = client.responses.create(
                    model = "gpt-4o-mini",
                    previous_response_id = response_id,
                    input = messages,
                    tools = [
                        {
                            "type" : "image_generation",
                            "quality" : "low"
                        }
                    ]
                )

                response_id = feedback_response.id

                #-------loop : for new reponse when user's re-request
                for feedback_output in feedback_response:
                    if feedback_output.type == "message":
                        ai_message = feedback_output.content[0].text
                        messages.append({
                            "role":"assistant",
                            "content" : ai_message
                        })
                    elif feedback_output.type == "image_generation_call":
                        image_base64 = feedback_output.result
                        print(f"revised image has been saved to {filename}")
                        break