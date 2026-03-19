# Node.js 版 Tool Calling デモ

## 前提条件

- Node.js v20.6 以上

## セットアップ

```bash
cd nodejs
npm install
```

## 実行

```bash
node --env-file=../.env demo-function-call.mjs
```

`--env-file` フラグでプロジェクトルートの `.env` から API キーを読み込みます。
