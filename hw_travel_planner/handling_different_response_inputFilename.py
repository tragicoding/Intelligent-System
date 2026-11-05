from openai import OpenAI
from openai.types.responses import Response
from dotenv import load_dotenv
import base64

load_dotenv()
client = OpenAI()

messages = [{
    "role" : "system",
    "content" : ""
}]

response = client.responses.create(
    model = "gpt-4o-mini",
    input = messages,
    tools = [
        {"type" : "image_generation"}
    ]
)

for output in response.output:
    if output.type == "message":
        ai_message = output.content[0].text
        messages.append({"role":"assistant",
                        "content":ai_message})
        print(ai_message)
    elif output.type == "image_generation_call":
        print("There is a image saving image to png or jpg...")
        filename = input("Image Created! Enter Image Name:")
        image_base64 = output.result

        with open(f"{filename}","wb") as f:
            f.write(base64.b64decode(image_base64))
            print("image saved!")