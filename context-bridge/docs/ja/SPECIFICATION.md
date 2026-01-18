# Context Bridge for Antigravity - 技術仕様書

**バージョン**: 1.0.0  
**最終更新**: 2026-01-17  
**ステータス**: 実装完了

---

## 📐 システムアーキテクチャ

### 全体構成

```
┌─────────────────────────────────────────────┐
│          User (Antigravity Agent)           │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
    ┌─────────────────────────────┐
    │   /open-airlock workflow    │
    └─────────────┬───────────────┘
                  │
                  ▼
    ┌─────────────────────────────┐
    │    bridge_gui.py (tkinter)  │
    │  ┌─────────┐   ┌──────────┐ │
    │  │ Request │   │ Response │ │
    │  │  Panel  │   │  Panel   │ │
    │  └─────────┘   └──────────┘ │
    └──────┬──────────────┬───────┘
           │              │
      📋 Clipboard    📋 Clipboard
           │              │
           ▼              ▼
    ┌─────────────────────────────┐
    │    Web AI (Browser)         │
    │  - Google AI Studio         │
    │  - ChatGPT                  │
    │  - Claude.ai                │
    └─────────────────────────────┘
```

---

## 🗂️ ファイル構成

```
ContextBridge/
├── tools/
│   └── bridge_gui.py           # メインアプリケーション (653行)
├── skills/
│   └── manual_bridge.md        # Antigravityスキル定義
├── .agent/
│   └── workflows/
│       └── open-airlock.md     # Antigravityワークフロー
├── docs/
│   ├── README.md               # ユーザーガイド
│   ├── PLANNING.md             # 企画書
│   └── SPECIFICATION.md        # この技術仕様書
└── demo/                       # デモプロジェクト
    ├── index.html
    ├── style.css
    └── game.js
```

---

## 🔧 コアモジュール仕様

### 1. ファイル収集モジュール

#### `collect_files(project_root: Path) -> list`

プロジェクト内のテキストファイルを収集します。

**処理フロー**:
1. `.gitignore` ファイルをパース
2. プロジェクトルート配下を再帰的にスキャン
3. 除外パターンとバイナリチェックを適用
4. 結果をソートして返却

**除外ルール**:

| 種別 | パターン例 |
|------|-----------|
| システムディレクトリ | `.git/`, `__pycache__/`, `node_modules/` |
| バイナリ拡張子 | `.exe`, `.png`, `.jpg`, `.pdf` |
| `.gitignore`指定 | ユーザー定義パターン |

**実装詳細**:
```python
# .gitignore パターンマッチング
def should_ignore(path: Path, project_root: Path, gitignore_patterns: list) -> bool:
    # fnmatch でグロブパターン適用
    # 相対パス変換して比較
    # バイナリ拡張子チェック
```

**バイナリ判定**:
```python
def is_text_file(file_path: Path) -> bool:
    # 最初の8KBを読み込み
    # null バイト (\x00) の存在チェック
    # UTF-8デコード試行
    # フォールバック: latin-1, cp1252, shift_jis
```

---

### 2. コンテキストパッキングモジュール

#### `pack_context_xml(files: list, project_root: Path) -> str`

ファイルリストをXML形式に変換します。

**出力形式**:
```xml
<file path="src/main.py">
ファイル内容（複数行可）
</file>

<file path="tests/test_main.py">
テストコード
</file>
```

**特徴**:
- パスは常に `/` 区切り（クロスプラットフォーム対応）
- プロジェクトルートからの相対パス
- ファイル間は2行空行で区切り

**エンコーディング処理**:
```python
def read_file_content(file_path: Path) -> str:
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'shift_jis']
    # フォールバック方式で順次試行
```

---

### 3. プロンプト生成モジュール

#### 生成されるプロンプト構造

```markdown
[システムプロンプト]
  - AIへの厳格な指示
  - SEARCH/REPLACE フォーマット強制
  - 出力例の提示

[XML形式のファイルコンテキスト]
  <file path="...">...</file>
  <file path="...">...</file>

---
## User Instruction
[ユーザーの指示]
```

**システムプロンプトの内容**:
- SEARCH/REPLACEブロックの必須化
- インデント・空白の正確性要求
- 新規ファイル/削除の記法説明

---

### 4. パッチ解析・適用モジュール

#### `parse_patches(text: str) -> list`

クリップボード内容からパッチブロックを抽出します。

**正規表現パターン**:
```python
pattern = r'<<<<\s*SEARCH\s+([^\n]+)\n(.*?)\n====\n(.*?)\n>>>>'
```

**抽出結果**:
```python
[
    {
        'file': 'path/to/file.py',
        'search': '検索対象コード',
        'replace': '置換後コード'
    },
    ...
]
```

#### `apply_patch(patch: dict, project_root: Path) -> tuple`

単一パッチをファイルに適用します。

**処理パターン**:

| ケース | search | replace | 動作 |
|--------|--------|---------|------|
| 新規作成 | 空 | 内容あり | ファイル作成 |
| 削除 | 内容あり | 空 | ファイル削除 |
| 変更 | 内容あり | 内容あり | 内容置換 |

**マッチングアルゴリズム**:

1. **Exact Match（優先）**: 文字列完全一致
   ```python
   if search_content in content:
       new_content = content.replace(search_content, replace_content, 1)
   ```

2. **Fuzzy Match（フォールバック）**: 空白揺らぎ許容
   ```python
   # 行ごとに strip() して比較
   for i in range(len(content_lines) - len(search_lines) + 1):
       if all(content_lines[i+j].strip() == search_lines[j].strip()):
           # マッチ成功
   ```

**エラーハンドリング**:
- ファイル不存在: `❌ File not found: {path}`
- 検索失敗: `❌ Search content not found in: {path}`
- 書き込み失敗: `❌ Failed to modify {path}: {error}`

---

## 🎨 GUI仕様

### ウィンドウ設定

| 項目 | 値 |
|------|-----|
| 初期サイズ | 900 × 650 |
| 最小サイズ | 700 × 500 |
| レイアウト | 2ペイン（水平分割） |

### 左パネル（往路 / Request）

#### 構成要素

1. **指示入力エリア**
   - Widget: `ScrolledText`
   - 高さ: 4行
   - デフォルトテキスト: "以下の変更を行ってください："

2. **コンテキストオプション**
   - LabelFrame: "コンテキストオプション"
   - チェックボックス: "すべてのファイルを送信"
   - デフォルト: ON

3. **ファイルリスト**
   - スクロール可能Canvas
   - 各ファイルにCheckbutton
   - マウスホイール対応

4. **統計表示**
   - フォーマット: "ファイル数: X/Y | サイズ: Z KB"
   - リアルタイム更新

5. **コピーボタン**
   - テキスト: "📋 プロンプトをコピー"
   - アクション: `_copy_to_clipboard()`

### 右パネル（復路 / Response）

#### 構成要素

1. **ログ表示エリア**
   - Widget: `ScrolledText` (readonly)
   - カラータグ:
     - `success`: 緑
     - `error`: 赤
     - `info`: 青
     - `warning`: オレンジ

2. **適用ボタン**
   - テキスト: "🔨 パッチを適用"
   - アクション: `_apply_from_clipboard()`

3. **更新ボタン**
   - テキスト: "🔄 ファイルリスト更新"
   - アクション: `_load_files()`

---

## 🔄 処理フロー詳細

### 往路（Request Flow）

```
User Input
    ↓
[指示入力 + ファイル選択]
    ↓
_copy_to_clipboard()
    ├─ instruction取得
    ├─ selected files取得
    ├─ pack_context_xml()
    ├─ SYSTEM_PROMPT結合
    ├─ clipboard_append()
    └─ 統計情報表示
    ↓
[クリップボードにプロンプト]
    ↓
User: Web AIにペースト
```

**トークン推定**:
```python
token_estimate = char_count // 4  # 1トークン ≈ 4文字（英語基準）
```

### 復路（Response Flow）

```
User: AI応答をコピー
    ↓
[クリップボードにAI応答]
    ↓
_apply_from_clipboard()
    ├─ clipboard_get()
    ├─ parse_patches()  # 正規表現で抽出
    ├─ for each patch:
    │   └─ apply_patch()
    │       ├─ 新規作成 / 削除 / 変更 判定
    │       ├─ exact match 試行
    │       ├─ fuzzy match 試行
    │       └─ ファイル書き込み
    └─ 結果ログ表示
    ↓
[ファイル更新完了]
```

---

## 🛡️ セキュリティとエラーハンドリング

### セキュリティ考慮事項

1. **パス検証**
   ```python
   # プロジェクトルート外への書き込み防止
   file_path = project_root / patch['file']
   # 相対パスのみ許可、絶対パスは拒否
   ```

2. **ファイル上書き保護**
   - 既存ファイルへの変更は必ずSEARCH指定必須
   - 空SEARCHは新規作成のみ

3. **センシティブファイル除外**
   - `.git/`, `.env`, `*.key` 等をデフォルト除外
   - `.gitignore` に従う

### エラーハンドリング

| エラー種別 | 検出箇所 | 処理 |
|-----------|---------|------|
| 空指示 | `_copy_to_clipboard` | Warning表示、中断 |
| ファイル未選択 | `_copy_to_clipboard` | Warning表示、中断 |
| クリップボード空 | `_apply_from_clipboard` | Warning表示、中断 |
| パッチ未検出 | `parse_patches` | Warning + 書式説明 |
| ファイル不存在 | `apply_patch` | エラーログ、処理継続 |
| 検索失敗 | `apply_patch` | エラーログ、処理継続 |

**ログレベル**:
```python
# ログタグとメッセージ例
'info'    → "ファイルをスキャン中..."
'success' → "✅ クリップボードにコピーしました！"
'warning' → "⚠️ 一部のパッチ適用に失敗"
'error'   → "❌ Search content not found"
```

---

## 🧪 テスト戦略

### 単体テスト対象

1. **ファイル収集**
   - `.gitignore` パターンマッチング
   - バイナリファイル判定
   - 文字エンコーディング検出

2. **XML生成**
   - 特殊文字のエスケープ
   - パス区切り文字の正規化

3. **パッチ解析**
   - 正規表現マッチング
   - 複数パッチの抽出
   - エッジケース（空行、特殊記号）

4. **パッチ適用**
   - 新規作成
   - 削除
   - 変更（exact / fuzzy）

### 統合テスト

**デモプロジェクトでの確認**:
```bash
python tools/bridge_gui.py --cwd demo
```

**テストシナリオ**:
1. 全ファイル選択 → コピー → トークン数確認
2. AI生成パッチ → 適用 → ファイル変更確認
3. 複数ファイル同時変更
4. エラーケース（存在しないファイル指定等）

---

## 📊 パフォーマンス

### 制限事項

| 項目 | 制限 | 理由 |
|------|------|------|
| 最大ファイル数 | なし | tkinterのメモリ次第 |
| 最大ファイルサイズ | なし | テキストファイルのみ |
| 最大プロンプトサイズ | Web AI依存 | Gemini: 100万トークン |
| パッチ適用速度 | ~10ファイル/秒 | ファイルI/O依存 |

### 最適化ポイント

1. **ファイルスキャン**
   - `Path.rglob('*')` の1パス処理
   - 不要な再スキャン回避

2. **クリップボード操作**
   - `clipboard_get()` は1回のみ
   - 大量テキストでもtk内部バッファで処理

3. **GUI描画**
   - ファイルリストは仮想化なし（数百ファイルまで想定）
   - ログは`state=DISABLED`でパフォーマンス確保

---

## 🔌 拡張性

### プラグインポイント

将来的に拡張可能な箇所：

1. **カスタムパッチフォーマット**
   ```python
   # parse_patches() を拡張
   # 正規表現を変更可能に
   ```

2. **AI別システムプロンプト**
   ```python
   SYSTEM_PROMPTS = {
       'gemini': "...",
       'gpt4': "...",
       'claude': "..."
   }
   ```

3. **履歴管理**
   ```python
   # パッチ適用時に履歴保存
   history_db.save(patch, timestamp)
   ```

---

## 📝 依存関係

### Python標準ライブラリのみ

```python
import os           # ファイル操作
import re           # 正規表現
import sys          # コマンドライン引数
import fnmatch      # グロブパターン
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
```

**外部ライブラリ不要**:
- ✅ `pyperclip` 不要（tkinterのclipboard使用）
- ✅ `gitignore_parser` 不要（自前実装）
- ✅ `lxml` 不要（文字列結合で十分）

---

## 🔧 デバッグ・メンテナンス

### ログ出力

GUIのログエリアに以下を出力：

```
ファイルをスキャン中...
3個のテキストファイルを発見
プロンプトを生成中...
✅ クリップボードにコピーしました！
   文字数: 12,345
   推定トークン数: ~3,086
   含まれるファイル数: 3
==================================================
パッチを適用中 (15:17:23)
3個のパッチを検出
✅ Modified: demo/game.js
✅ Modified: demo/style.css
✅ Created: demo/config.json
------------------------------
完了: 3件成功, 0件失敗
```

### トラブルシューティングフロー

```
問題発生
    ↓
ログ確認 → エラーメッセージから原因特定
    ↓
├─ ファイル見つからない → パス確認
├─ 検索失敗 → 空白・インデント確認
├─ パッチ未検出 → AI出力形式確認
└─ その他 → SPECIFICATION.md 参照
```

---

## 📚 参考資料

- [tkinter公式ドキュメント](https://docs.python.org/3/library/tkinter.html)
- [pathlib公式ドキュメント](https://docs.python.org/3/library/pathlib.html)
- [gitignore仕様](https://git-scm.com/docs/gitignore)
- [Google AI Studio](https://aistudio.google.com/)

---

## 📞 技術サポート

**技術的な質問**:
- この仕様書を参照
- コード内のdocstringを確認
- `bridge_gui.py` のコメント参照

**バグ報告**:
1. 再現手順
2. エラーログ
3. 環境情報（Python version, OS）

---

**作成者**: [JUN SUZUKI](https://junsuzuki-ai-agency.xyz/)  
**最終更新**: 2026-01-17  
**次回レビュー**: 2026-03-17
