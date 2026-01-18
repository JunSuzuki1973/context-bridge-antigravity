# Project Structure / プロジェクト構成

## English

```
ContextBridge/
├── README.md                      # Main documentation (English)
├── README.ja.md                   # Main documentation (Japanese)
├── LICENSE                        # MIT License
│
├── tools/
│   └── bridge_gui.py             # Main GUI application (653 lines)
│
├── skills/
│   └── manual_bridge.md          # Antigravity skill definition
│
├── .agent/
│   └── workflows/
│       └── open-airlock.md       # /open-airlock command workflow
│
├── docs/
│   ├── LICENSE_INFO.md           # License explanation (bilingual)
│   ├── en/                       # English documentation
│   │   └── PLANNING.md           # Planning document
│   └── ja/                       # Japanese documentation
│       ├── PLANNING.md           # 企画書
│       └── SPECIFICATION.md      # 技術仕様書
│
└── demo/                         # Demo project (block breaker game)
    ├── index.html
    ├── style.css
    └── game.js
```

## Documentation / ドキュメント

### User Documentation / ユーザー向け

| File | EN | JA | Description |
|------|----|----|-------------|
| README | ✅ | ✅ | Installation, usage, troubleshooting |
| LICENSE_INFO | ✅ | ✅ | License explanation and rationale |

### Developer Documentation / 開発者向け

| File | EN | JA | Description |
|------|----|----|-------------|
| PLANNING | ✅ | ✅ | Concept, requirements, roadmap |
| SPECIFICATION | ❌ | ✅ | Technical architecture and implementation |

**Note**: English SPECIFICATION.md can be created on demand.

---

## 日本語

```
ContextBridge/
├── README.md                      # メインドキュメント（英語）
├── README.ja.md                   # メインドキュメント（日本語）
├── LICENSE                        # MITライセンス
│
├── tools/
│   └── bridge_gui.py             # メインGUIアプリケーション（653行）
│
├── skills/
│   └── manual_bridge.md          # Antigravityスキル定義
│
├── .agent/
│   └── workflows/
│       └── open-airlock.md       # /open-airlockコマンドワークフロー
│
├── docs/
│   ├── LICENSE_INFO.md           # ライセンス説明（バイリンガル）
│   ├── en/                       # 英語ドキュメント
│   │   └── PLANNING.md           # Planning document
│   └── ja/                       # 日本語ドキュメント
│       ├── PLANNING.md           # 企画書
│       └── SPECIFICATION.md      # 技術仕様書
│
└── demo/                         # デモプロジェクト（ブロック崩しゲーム）
    ├── index.html
    ├── style.css
    └── game.js
```

## ドキュメント一覧

### ユーザー向けドキュメント

| ファイル | EN | JA | 説明 |
|---------|----|----|------|
| README | ✅ | ✅ | インストール、使い方、トラブルシューティング |
| LICENSE_INFO | ✅ | ✅ | ライセンスの説明と選定理由 |

### 開発者向けドキュメント

| ファイル | EN | JA | 説明 |
|---------|----|----|------|
| PLANNING | ✅ | ✅ | コンセプト、要件、ロードマップ |
| SPECIFICATION | ❌ | ✅ | 技術アーキテクチャと実装詳細 |

**注記**: 英語版SPECIFICATION.mdは必要に応じて作成可能です。

---

## Quick Start / クイックスタート

### English

1. Read [README.md](../README.md)
2. Install following instructions
3. Run `/open-airlock` in Antigravity
4. Try with [demo/](../demo/) project

### 日本語

1. [README.ja.md](../README.ja.md) を読む
2. 手順に従ってインストール
3. Antigravityで `/open-airlock` を実行
4. [demo/](../demo/) プロジェクトで試す
