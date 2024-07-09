# PDF to Notion Importer

PDF to Notion Importerは、PDF論文から書誌情報を抽出し、Notionデータベースに追加するツールです。ローカルPDFファイルとURL入力の両方をサポートし、重複チェックやBibTeX形式の整形などの機能を備えています。

## 主な機能

- PDFファイルから書誌情報を抽出
- ローカルPDFファイルとURL入力のサポート
- 抽出した情報をNotionデータベースに追加
- 重複エントリーのチェック
- BibTeX形式の整形とクリーニング
- 重複エントリーを上書きするためのforceオプション

## インストール方法

1. Python 3.8以上がシステムにインストールされていることを確認してください。
2. このリポジトリをクローンします：
   ```
   git clone https://github.com/yutojubako/notion-paperr
   cd notion-paper
   ```
3. Poetryを使用して必要な依存関係をインストールします：
   ```
   poetry install
   ```

## 設定

1. Notion統合をセットアップし、APIトークンを取得します。[方法はこちら](https://developers.notion.com/docs/getting-started)
2. 論文情報を保存するためのNotionデータベースを作成します。
3. 以下の環境変数を設定します：
   ```
   export DEFAULT_NOTION_TOKEN="your_notion_api_token"
   export DEFAULT_DATABASE_ID="your_notion_database_id"
   ```

## 使用方法

### ローカルPDFファイル

ローカルのPDFファイルをNotionデータベースに追加するには：

```
poetry run python main.py path/to/your/paper.pdf
```

### URL入力

URLからペーパーを追加するには：

```
poetry run python main.py -u https://example.com/paper.pdf
```

### forceオプション

重複が見つかった場合でもエントリーを強制的に追加するには：

```
poetry run python main.py path/to/your/paper.pdf -f
```

または

```
poetry run python main.py -u https://example.com/paper.pdf --force
```

## コントリビューション

コントリビューションは歓迎します！お気軽にPull Requestを提出してください。

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています - 詳細は[LICENSE](LICENSE)ファイルをご覧ください。