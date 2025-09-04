

# get_hp ツール群

このディレクトリには、Webサイトのトップページや問い合わせページのURLを取得するためのPythonスクリプトが含まれています。

## 概要

- `get_top_site.py` : Google Custom Search APIを使って、キーワードリストから最上位のサイトURLを取得します。
- `get_contact_link.py` : 企業サイトのURLリストから問い合わせページ（Contact/Inqury/お問い合わせ等）を自動で抽出します。

---

## 使い方

pip install python-dotenv google-api-python-client

## 依存パッケージのインストール

```
pip install python-dotenv google-api-python-client beautifulsoup4 requests
```


---

## get_top_site.py の使い方

1. `.env` ファイルを `get_hp/` ディレクトリに用意し、以下の内容を記述してください。

```
GOOGLE_API_KEY=あなたのAPIキー
CUSTOM_SEARCH_ENGINE_ID=あなたのカスタム検索エンジンID
```

google
github

2. 入力ファイル（例: `example/input.txt`）を用意し、1行ごとに検索キーワードを記述します。

例:
```plaintext
google
github
```


3. 実行例

```
python get_top_site.py example/input.txt -o example/output.txt
```

- 標準出力と `-o` で指定したファイルの両方に結果が出力されます。
- 出力形式は `キーワード|URL` です。URLが見つからない場合は `None` となります。


---

## get_contact_link.py の使い方

企業名とURLのリスト（`|` 区切り、例: `input.txt`）から、問い合わせページのURLを抽出します。

### 入力ファイル例
```plaintext
株式会社サンプル|https://sample.co.jp
株式会社テスト|https://test.com
```


### 実行例
```
python get_contact_link.py example/output.txt -o output_with_contact.txt
```

- 標準出力と `-o` で指定したファイルの両方に結果が出力されます。
- 出力形式は `会社名|元URL|問い合わせページURL` です。
- 問い合わせページが見つからない場合は `No contact page found` となります。

---

---


## 注意
- Google Custom Search APIのクォータ制限に注意してください。クォータ超過時は自動で停止します。
- `get_contact_link.py` は外部サイトへのアクセスを多数行うため、実行時はネットワーク環境や先方サイトの利用規約にご注意ください。
