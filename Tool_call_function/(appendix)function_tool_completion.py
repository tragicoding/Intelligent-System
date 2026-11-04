import json
from openai.types.chat import ChatCompletion
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


def calculator(a, b, operator):
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return a / b if b != 0 else "Error: Division by zero"
    return "Error: Unknown operator"


FUNCTION_LOOKUP = {"calculator": calculator}

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": """
                    Perform basic arithmetic operations
                    (add, subtract, multiply, divide) on two numbers
                """,
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The first number"},
                    "b": {"type": "number", "description": "The second number"},
                    "operator": {
                        "type": "string",
                        "enum": ["+", "-", "*", "/"],
                        "description": "The arithmetic operator to apply",
                    },
                },
                "required": ["a", "b", "operator"],
            },
        },
    }
]

messages = []

while True:
    question = input("Ask to AI: ")

    if question == "quit":
        break

    messages.append({"role": "user", "content": question})

    client = OpenAI()
    response: ChatCompletion = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, tools=tools
    )

    ai_message = response.choices[0].message

    while ai_message.tool_calls:
        messages.append(ai_message)
        print(ai_message)

        for tool_call in ai_message.tool_calls or []:
            id = tool_call.id
            fn_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            fn = FUNCTION_LOOKUP.get(fn_name)
            if fn:
                result = fn(**args)
                messages.append(
                    {
                        "role": "tool",
                        "content": str(result),
                        "name": fn_name,
                        "tool_call_id": id,
                    }
                )

        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, tools=tools
        )
        ai_message = response.choices[0].message

    ai_message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ai_message})
    print(f"AI: {ai_message}")
