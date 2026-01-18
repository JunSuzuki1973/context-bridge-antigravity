---
description: Context Bridgeを起動してWeb AIと連携する
---

# Context Bridge

外部Web AI（Google AI Studio, ChatGPT等）を使用してコーディングするための「Human Relay」GUIツールを起動します。

## 起動コマンド

// turbo
1. Context Bridge GUIを起動する
```bash
python tools/bridge_gui.py
```

## 使い方

### 往路（プロジェクトコンテキストをWeb AIへ送信）
1. GUIウィンドウで「指示」欄にタスクを入力
2. 必要に応じて送信ファイルを選択（デフォルト：全ファイル）
3. 「📋 プロンプトをコピー」をクリック
4. [Google AI Studio](https://aistudio.google.com/)または[ChatGPT](https://chat.openai.com/)を開く
5. プロンプトをペースト（Ctrl+V）して送信

### 復路（AIの応答をローカルに適用）
1. AIの応答全体をコピー（Ctrl+A → Ctrl+C）
2. GUIウィンドウに戻る
3. 「🔨 パッチを適用」をクリック
4. 結果ログを確認

## トリガーワード
ユーザーが以下のように言った場合、このワークフローを実行してください：
- "Context Bridgeを起動"
- "コンテキストブリッジのスキルを使います"
- "Manual Bridge Modeを使いたい"
- "Open Airlock"
- "Web AIを使ってコーディングしたい"
- "APIキーを使わずにAIに依頼したい"

## 推奨AI
- **Google AI Studio (Gemini 3.0 Pro)**: 100万トークン対応（大規模プロジェクト向け）
- **Claude (Sonnet 4.5)**: 200Kトークン（中規模プロジェクト向け）
