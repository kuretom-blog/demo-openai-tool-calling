import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path="../.env")

client = OpenAI()

messages = [
    {"role": "system", "content": "あなたは親切なアシスタントです。"},
    {"role": "user", "content": "おうし座の今日の運勢を教えてください。"},
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_horoscope",
            "description": "指定された星座の運勢を取得する",
            "parameters": {
                "type": "object",
                "properties": {
                    "sign": {
                        "type": "string",
                        "description": "星座名（例: 'おうし座'）",
                    },
                    "day": {
                        "type": "string",
                        "enum": ["today", "tomorrow"],
                        "description": "運勢を取得する日（今日または明日）",
                    },
                },
                "required": ["sign"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]

response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=messages,
    tools=tools,
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
                "horoscope": f"今日の{func_args.get('sign')}の運勢: 全体運は好調です！積極的に行動すると吉。"
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
