
# get_top_site.py

Google Custom Search APIを使って、キーワードリストから最上位のサイトURLを取得するツールです。

## 使い方

1. 依存パッケージのインストール

```
pip install python-dotenv google-api-python-client
```

2. `.env` ファイルを `get_hp/` ディレクトリに用意し、以下の内容を記述してください。

```
GOOGLE_API_KEY=あなたのAPIキー
CUSTOM_SEARCH_ENGINE_ID=あなたのカスタム検索エンジンID
```

3. 入力ファイル（例: `example/input.txt`）を用意し、1行ごとに検索キーワードを記述します。

例:
```plaintext
google
github
```

4. 実行例

```
python get_top_site.py example/input.txt -o example/output.txt
```

- 標準出力と `-o` で指定したファイルの両方に結果が出力されます。
- 出力形式は `キーワード|URL` です。URLが見つからない場合は `None` となります。

## Example

- `example/input.txt` : 検索キーワードリスト
- `example/output.txt` : 実行結果サンプル

---

## 注意
- Google Custom Search APIのクォータ制限に注意してください。クォータ超過時は自動で停止します。
