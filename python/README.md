# Python 版 Tool Calling デモ

## 前提条件

- Python 3.9 以上

## セットアップ

```bash
cd python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 実行

```bash
source .venv/bin/activate
python3 demo-function-call.py
```

`.env` はプロジェクトルート（`../.env`）から `python-dotenv` で自動読み込みされます。
