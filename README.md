# demo-openai-function-calling

OpenAI の Tool Calling API を使ったデモプロジェクト。Python と Node.js の両言語で同じ処理を実装しています。

## 前提条件

- OpenAI の API キーを取得済みであること

## セットアップ

プロジェクトルートに `.env` ファイルを作成し、API キーを設定します:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
```

各言語の実行方法は、それぞれのディレクトリ内の README.md を参照してください。

- [Python 版](python/README.md)
- [Node.js 版](nodejs/README.md)

## ディレクトリ構成

```
.
├── .env                 # OpenAI API キー（共有）
├── python/
│   ├── demo-function-call.py
│   └── requirements.txt
└── nodejs/
    ├── demo-function-call.mjs
    └── package.json
```
