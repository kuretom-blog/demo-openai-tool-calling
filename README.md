# demo-openai-function-calling

OpenAI Chat Completions API の **Tool Calling**（旧 Function Calling）を最小構成で試すデモプロジェクトです。
Python と Node.js で同じ処理を実装しており、動作の比較ができます。

## Tool Calling とは

通常の Chat API はテキストを返すだけですが、Tool Calling を使うとモデルが **「この関数をこの引数で呼んでほしい」** という指示を返せるようになります。
アプリ側で関数を実行し、その結果をモデルに戻すことで、外部データを組み込んだ応答が可能になります。

## 動作フロー

このデモでは「おうし座の運勢を教えて」というリクエストを例に、以下の流れで処理します。

```
ユーザー                      アプリ                         OpenAI API
  |                            |                               |
  |  「おうし座の運勢を教えて」  |                               |
  | -------------------------> |  messages + tools 定義を送信   |
  |                            | ----------------------------> |
  |                            |                               |
  |                            |  tool_calls を返却             |
  |                            |  (get_horoscope, sign=おうし座) |
  |                            | <---------------------------- |
  |                            |                               |
  |                            |  アプリ側で関数を実行（ダミー結果） |
  |                            |  結果を role: "tool" で送信     |
  |                            | ----------------------------> |
  |                            |                               |
  |                            |  ツール結果を踏まえた最終応答    |
  |  最終応答を表示             | <---------------------------- |
  | <------------------------- |                               |
```

1. **ツール定義を添えてリクエスト** -- `get_horoscope` 関数のスキーマを `tools` パラメータで渡す
2. **モデルが `tool_calls` を返す** -- `finish_reason` が `"tool_calls"` になる
3. **アプリ側で関数を実行** -- 本デモではダミーの固定文字列を返す（実運用では外部 API や DB を呼び出す）
4. **結果をモデルに返して最終応答を取得** -- `role: "tool"` メッセージを追加して 2 回目のリクエスト

## 前提条件

- OpenAI の API キーを取得済みであること
- Python 3.9+ または Node.js 18+

## セットアップ

プロジェクトルートに `.env` ファイルを作成し、API キーを設定します:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
```

### Python 版

```bash
cd python
pip install -r requirements.txt
python demo-function-call.py
```

### Node.js 版

```bash
cd nodejs
npm install
node demo-function-call.mjs
```

## 実行結果の例

```
finish_reason: tool_calls
tool_call: get_horoscope({"sign": "おうし座"})
今日のおうし座の運勢は好調です！積極的に行動すると良い結果につながるでしょう。
```

## ディレクトリ構成

```
.
├── .env                      # OpenAI API キー（Python・Node.js 共有）
├── python/
│   ├── demo-function-call.py # Python 版デモ
│   └── requirements.txt
└── nodejs/
    ├── demo-function-call.mjs # Node.js 版デモ
    └── package.json
```

## 試してみるポイント

- **ユーザーメッセージを変える** -- ツールが呼ばれるケースと呼ばれないケースを比較する
- **`tool_choice` を指定する** -- `"required"` や `"none"` を渡して挙動の違いを確認する
- **ツールを追加する** -- `tools` 配列に別の関数定義を足して、モデルが正しく選択するか検証する
- **`strict: true` を外す** -- Structured Outputs による引数スキーマ準拠の効果を確認する
