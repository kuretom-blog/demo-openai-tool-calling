import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path="../.env")

client = OpenAI()

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Give me my horoscope for Taurus."},
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_horoscope",
            "description": "Get the horoscope for a given zodiac sign",
            "parameters": {
                "type": "object",
                "properties": {
                    "sign": {
                        "type": "string",
                        "description": "Zodiac sign, e.g. 'Taurus'",
                    },
                    "day": {
                        "type": "string",
                        "enum": ["today", "tomorrow"],
                        "description": "Which day to get the horoscope for",
                    },
                },
                "required": ["sign"],
                "additionalProperties": False,
            },
        },
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
    tool_choice="auto",
)

message = response.choices[0].message
print("finish_reason:", response.choices[0].finish_reason)

if message.tool_calls:
    for tool_call in message.tool_calls:
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)
        print(f"tool_call: {func_name}({func_args})")

        if func_name == "get_horoscope":
            tool_result = {
                "horoscope": f"Today's {func_args.get('sign')} horoscope: Your fortune is looking great!"
            }
        else:
            raise RuntimeError(f"Unknown function: {func_name}")

        messages.append(message)
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result, ensure_ascii=False),
            }
        )

    response2 = client.chat.completions.create(
        model="gpt-5-mini",
        messages=messages,
    )

    print(response2.choices[0].message.content)
else:
    print(message.content)
