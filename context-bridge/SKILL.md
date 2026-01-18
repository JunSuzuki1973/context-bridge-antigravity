---
name: Context Bridge
description: 外部Web AI（Gemini/ChatGPT）を使用してコーディングを行うための「Human Relay」ツール。API消費ゼロで大規模コンテキストを扱える。
---

# Context Bridge

外部のWebチャットボット（Google AI Studio, ChatGPT等）を推論エンジンとして使用するための「Human Relay（人間中継）」機能です。

## 概要

- **コンセプト**: プロジェクトのコンテキストをクリップボード経由でWeb AIに渡し、生成されたコード差分を受け取ってローカルに適用
- **メリット**: API消費ゼロ、Gemini 3.0 Proなら100万トークン対応で大規模プロジェクトも一括送信可能
- **安全性**: 専用GUIウィンドウで操作を完結、ターミナルへの誤ペースト事故を防止

## 起動コマンド

```bash
python tools/bridge_gui.py
```

オプション：
```bash
python tools/bridge_gui.py --cwd /path/to/project
```

## 使用シナリオ

以下のような場合にこのスキルを使用してください：

1. ユーザーが「Webチャットボットを使いたい」「APIを節約したい」「Bridgeモード」と指示した場合
2. プロジェクト全体の大規模なリファクタリングなど、長文脈が必要な場合
3. Gemini 3.0 Proの100万トークンコンテキストを活用したい場合
4. APIキーの制限に達した場合の代替手段として

## 操作手順

### 往路（Request）

1. GUIを起動
2. `User Instruction` 欄に変更指示を入力
3. 必要に応じてファイルリストから送信ファイルを選択（デフォルトは全ファイル送信）
4. `Copy Prompt to Clipboard` をクリック
5. ブラウザで [Google AI Studio](https://aistudio.google.com/) または ChatGPT を開く
6. プロンプトをペースト、送信

### 復路（Response）

1. Web AIの応答をコピー（Ctrl+A → Ctrl+C）
2. GUIに戻り `Apply Patch from Clipboard` をクリック
3. パッチが自動的に適用される
4. 結果ログを確認

## 推奨AI

| AI | コンテキスト長 | 推奨度 |
|----|--------------|--------|
| Google AI Studio (Gemini 3.0 Pro) | 100万トークン | ⭐⭐⭐ 強く推奨 |
| Claude (Sonnet 4.5) | 200Kトークン | ⭐⭐ 中規模プロジェクト向け |

## パッチフォーマット

Web AIには以下の形式で出力するよう指示されます：

```
<<<< SEARCH path/to/file.ext
検索対象の既存コード
====
置換後の新しいコード
>>>>
```

### 新規ファイル作成
```
<<<< SEARCH path/to/newfile.ext
====
新規ファイルの内容
>>>>
```

### ファイル削除
```
<<<< SEARCH path/to/deletefile.ext
削除するファイルの内容
====
>>>>
```

## トラブルシューティング

### パッチが適用されない

- Web AIの出力が正しいフォーマットになっているか確認
- `<<<< SEARCH` と `>>>>` が正しくペアになっているか確認
- 検索対象のコードが現在のファイルと完全に一致しているか確認（空白・インデント含む）

### ファイルが見つからない

- パス区切りが `/` になっているか確認
- プロジェクトルートからの相対パスになっているか確認

### 文字化け

- ファイルがUTF-8エンコーディングであることを確認
