import OpenAI from "openai";

const client = new OpenAI(); // OPENAI_API_KEY 環境変数を自動で読み取る

const messages = [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user",   content: "Give me my horoscope for Taurus." },
];

const tools = [
    {
        type: "function",
        function: {
            name: "get_horoscope",
            description: "Get the horoscope for a given zodiac sign",
            parameters: {
                type: "object",
                properties: {
                    sign: { type: "string", description: "Zodiac sign, e.g. 'Taurus'" },
                    day:  { type: "string", enum: ["today", "tomorrow"], description: "Which day to get the horoscope for" },
                },
                required: ["sign"],
                additionalProperties: false,
            },
        },
    },
];

// ステップ1〜2: ツール定義を添えてモデルへ送信する
const response = await client.chat.completions.create({
    model: "gpt-4o-mini",
    messages,
    tools,
    tool_choice: "auto",
});

const message = response.choices[0].message;
console.log("finish_reason:", response.choices[0].finish_reason);

// ステップ3〜4: tool_callsが返ってきたらアプリ側で処理して結果を返す
if (message.tool_calls) {
    for (const toolCall of message.tool_calls) {
        const funcName = toolCall.function.name;
        const funcArgs = JSON.parse(toolCall.function.arguments);
        console.log(`tool_call: ${funcName}(${JSON.stringify(funcArgs)})`);

        let toolResult;
        if (funcName === "get_horoscope") {
            // ダミーの実行結果（実務では外部APIやDBを呼び出す）
            toolResult = { horoscope: `Today's ${funcArgs.sign} horoscope: Your fortune is looking great!` };
        } else {
            throw new Error(`Unknown function: ${funcName}`);
        }

        messages.push(message);
        messages.push({
            role: "tool",
            tool_call_id: toolCall.id,
            content: JSON.stringify(toolResult),
        });
    }

    // ステップ5: 最終応答を取得する
    const response2 = await client.chat.completions.create({
        model: "gpt-4o-mini",
        messages,
    });

    console.log(response2.choices[0].message.content);
} else {
    console.log(message.content);
}
