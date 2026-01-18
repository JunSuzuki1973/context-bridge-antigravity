#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Context Bridge - Human Relay GUI Tool
外部Web AI（Gemini/ChatGPT）を使用してコーディングを行うための「Human Relay」ツール。
API消費ゼロで大規模コンテキストを扱える。

Usage:
    python tools/bridge_gui.py [--cwd /path/to/project]
"""

import os
import re
import sys
import fnmatch
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# ==============================================================================
# Configuration
# ==============================================================================

# Default excluded directories (always ignored)
DEFAULT_EXCLUDED_DIRS = {
    '.git', '.agent', '__pycache__', 'node_modules', '.venv', 'venv', 'env',
    '.idea', '.vscode', '.vs', 'dist', 'build', '.next', '.nuxt',
    'coverage', '.pytest_cache', '.mypy_cache', '.tox', 'eggs',
    '*.egg-info', '.eggs', 'bower_components', 'jspm_packages',
    '.cache', 'tmp', 'temp', '.temp', '.tmp'
}

# Binary file extensions (always excluded)
BINARY_EXTENSIONS = {
    '.exe', '.dll', '.so', '.dylib', '.bin', '.obj', '.o', '.a',
    '.lib', '.pyc', '.pyo', '.pyd', '.class', '.jar', '.war',
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.webp', '.svg',
    '.mp3', '.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.wav',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.zip', '.tar', '.gz', '.rar', '.7z', '.bz2', '.xz',
    '.ttf', '.otf', '.woff', '.woff2', '.eot',
    '.db', '.sqlite', '.sqlite3', '.mdb',
    '.lock', '.ico'
}

# System prompt for Web AI
SYSTEM_PROMPT = """あなたは熟練したソフトウェアエンジニアです。以下のルールに**厳密に**従ってください。

## 絶対ルール
1. コードの変更は**必ず**以下のブロック形式で出力すること：

<<<< SEARCH path/to/file.ext
検索対象の既存コード（変更前のコード）
====
置換後の新しいコード
>>>>

2. 新規ファイル作成の場合は、SEARCHブロックを空にする：

<<<< SEARCH path/to/newfile.ext
====
新規ファイルの内容
>>>>

3. ファイル削除の場合は、REPLACEブロックを空にする：

<<<< SEARCH path/to/deletefile.ext
削除するファイルの内容
====
>>>>

4. 変更がない説明文は、コードブロックの**外に**記述すること
5. 各SEARCHブロックは、対象ファイル内で**一意に特定できる**十分な文脈を含めること
6. インデント・空白は**正確に**保持すること

## 出力例
ファイル `src/main.py` の関数名を変更する場合：

<<<< SEARCH src/main.py
def old_function_name():
    print("Hello")
====
def new_function_name():
    print("Hello, World!")
>>>>

---
以下はプロジェクトのファイル一覧とその内容です。ユーザーの指示に従って修正を行ってください。
"""

# ==============================================================================
# Utility Functions
# ==============================================================================

def parse_gitignore(project_root: Path) -> list:
    """Parse .gitignore file and return list of patterns."""
    gitignore_path = project_root / '.gitignore'
    patterns = []
    
    if gitignore_path.exists():
        try:
            with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith('#'):
                        patterns.append(line)
        except Exception:
            pass
    
    return patterns


def should_ignore(path: Path, project_root: Path, gitignore_patterns: list) -> bool:
    """Check if a path should be ignored based on .gitignore patterns and defaults."""
    rel_path = path.relative_to(project_root)
    rel_str = str(rel_path).replace('\\', '/')
    
    # Check default excluded directories
    for part in rel_path.parts:
        if part in DEFAULT_EXCLUDED_DIRS:
            return True
        for pattern in DEFAULT_EXCLUDED_DIRS:
            if fnmatch.fnmatch(part, pattern):
                return True
    
    # Check binary extensions
    if path.is_file() and path.suffix.lower() in BINARY_EXTENSIONS:
        return True
    
    # Check .gitignore patterns
    for pattern in gitignore_patterns:
        # Handle negation patterns (not fully implemented)
        if pattern.startswith('!'):
            continue
        
        # Normalize pattern
        p = pattern.rstrip('/')
        
        # Check if pattern matches
        if fnmatch.fnmatch(rel_str, p):
            return True
        if fnmatch.fnmatch(rel_str, p + '/*'):
            return True
        if fnmatch.fnmatch(path.name, p):
            return True
        # Handle directory patterns
        if pattern.endswith('/'):
            if fnmatch.fnmatch(rel_str, p + '*'):
                return True
    
    return False


def is_text_file(file_path: Path) -> bool:
    """Check if a file is a text file by reading first bytes."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(8192)
            # Check for null bytes (common in binary files)
            if b'\x00' in chunk:
                return False
            # Try to decode as UTF-8
            try:
                chunk.decode('utf-8')
                return True
            except UnicodeDecodeError:
                # Try other common encodings
                for encoding in ['latin-1', 'cp1252', 'shift_jis']:
                    try:
                        chunk.decode(encoding)
                        return True
                    except UnicodeDecodeError:
                        continue
                return False
    except Exception:
        return False


def collect_files(project_root: Path) -> list:
    """Collect all text files in the project, respecting .gitignore."""
    files = []
    gitignore_patterns = parse_gitignore(project_root)
    
    for item in project_root.rglob('*'):
        if item.is_file():
            if not should_ignore(item, project_root, gitignore_patterns):
                if is_text_file(item):
                    files.append(item)
    
    # Sort by path
    files.sort(key=lambda x: str(x).lower())
    return files


def read_file_content(file_path: Path) -> str:
    """Read file content with fallback encodings."""
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'shift_jis']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            return f"[Error reading file: {e}]"
    
    return "[Error: Unable to decode file with any known encoding]"


def pack_context_xml(files: list, project_root: Path) -> str:
    """Pack file contents into XML format."""
    xml_parts = []
    
    for file_path in files:
        rel_path = file_path.relative_to(project_root)
        rel_str = str(rel_path).replace('\\', '/')
        content = read_file_content(file_path)
        xml_parts.append(f'<file path="{rel_str}">\n{content}\n</file>')
    
    return '\n\n'.join(xml_parts)


def parse_patches(text: str) -> list:
    """Parse SEARCH/REPLACE blocks from text."""
    # Pattern to match <<<< SEARCH path ... ==== ... >>>>
    pattern = r'<<<<\s*SEARCH\s+([^\n]+)\n(.*?)\n====\n(.*?)\n>>>>'
    
    patches = []
    for match in re.finditer(pattern, text, re.DOTALL):
        file_path = match.group(1).strip()
        search_content = match.group(2)
        replace_content = match.group(3)
        patches.append({
            'file': file_path,
            'search': search_content,
            'replace': replace_content
        })
    
    return patches


def apply_patch(patch: dict, project_root: Path) -> tuple:
    """Apply a single patch to a file. Returns (success, message)."""
    file_path = project_root / patch['file']
    search_content = patch['search']
    replace_content = patch['replace']
    
    # Case 1: New file creation (empty search)
    if not search_content.strip():
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(replace_content)
            return (True, f"✅ Created: {patch['file']}")
        except Exception as e:
            return (False, f"❌ Failed to create {patch['file']}: {e}")
    
    # Case 2: File deletion (empty replace)
    if not replace_content.strip() and search_content.strip():
        try:
            if file_path.exists():
                file_path.unlink()
                return (True, f"🗑️ Deleted: {patch['file']}")
            else:
                return (False, f"⚠️ File not found for deletion: {patch['file']}")
        except Exception as e:
            return (False, f"❌ Failed to delete {patch['file']}: {e}")
    
    # Case 3: File modification
    if not file_path.exists():
        return (False, f"❌ File not found: {patch['file']}")
    
    try:
        content = read_file_content(file_path)
        
        # Try exact match first
        if search_content in content:
            new_content = content.replace(search_content, replace_content, 1)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return (True, f"✅ Modified: {patch['file']}")
        
        # Try with stripped whitespace comparison (line by line)
        content_lines = content.splitlines()
        search_lines = search_content.splitlines()
        
        # Find matching block with flexible whitespace
        for i in range(len(content_lines) - len(search_lines) + 1):
            match = True
            for j, search_line in enumerate(search_lines):
                if content_lines[i + j].strip() != search_line.strip():
                    match = False
                    break
            
            if match:
                # Replace the block
                new_lines = (
                    content_lines[:i] +
                    replace_content.splitlines() +
                    content_lines[i + len(search_lines):]
                )
                new_content = '\n'.join(new_lines)
                
                # Preserve original line ending style
                if '\r\n' in content:
                    new_content = new_content.replace('\n', '\r\n')
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return (True, f"✅ Modified (fuzzy match): {patch['file']}")
        
        return (False, f"❌ Search content not found in: {patch['file']}")
        
    except Exception as e:
        return (False, f"❌ Failed to modify {patch['file']}: {e}")


# ==============================================================================
# GUI Application
# ==============================================================================

class ManualBridgeGUI:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.files = []
        self.file_vars = {}  # CheckVar for each file
        
        self.root = tk.Tk()
        self.root.title(f"Context Bridge - {project_root.name}")
        self.root.geometry("900x650")
        self.root.minsize(700, 500)
        
        # Dark theme colors
        self.bg_color = '#2b2b2b'
        self.fg_color = '#e0e0e0'
        self.entry_bg = '#3c3c3c'
        self.entry_fg = '#ffffff'
        
        # Apply dark theme to root
        self.root.configure(bg=self.bg_color)
        
        # Configure style with dark theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.fg_color)
        self.style.configure('TLabelframe', background=self.bg_color, foreground=self.fg_color)
        self.style.configure('TLabelframe.Label', background=self.bg_color, foreground=self.fg_color)
        self.style.configure('TButton', background='#4a4a4a', foreground=self.fg_color, padding=6)
        self.style.configure('TCheckbutton', background=self.bg_color, foreground=self.fg_color)
        self.style.configure('TPanedwindow', background=self.bg_color)
        self.style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'), background=self.bg_color, foreground='#64b5f6')
        
        # Configure scrollbar for dark theme
        self.style.configure('Vertical.TScrollbar',
                            background='#4a4a4a',
                            darkcolor='#2b2b2b',
                            lightcolor='#4a4a4a',
                            troughcolor='#2b2b2b',
                            bordercolor='#2b2b2b',
                            arrowcolor='#e0e0e0')
        self.style.map('Vertical.TScrollbar',
                      background=[('active', '#5a5a5a'), ('!active', '#4a4a4a')])
        
        # Apply dark title bar on Windows 10/11
        self.root.update_idletasks()  # Ensure window is created
        try:
            import ctypes
            # Get window handle
            hwnd = ctypes.windll.user32.FindWindowW(None, self.root.title())
            if hwnd:
                # Windows 11 dark mode
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                value = ctypes.c_int(2)  # 2 = force dark mode
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
                    ctypes.byref(value), ctypes.sizeof(value)
                )
        except:
            pass  # Silently fail on non-Windows or older Windows
        
        self._create_widgets()
        self._load_files()
    
    def _create_widgets(self):
        """Create all GUI widgets."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create PanedWindow for resizable sections
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # ====== Left Panel: Request ======
        left_frame = ttk.Frame(paned, padding="5")
        paned.add(left_frame, weight=1)
        
        # Header
        ttk.Label(left_frame, text="📤 Request / 往路", style='Header.TLabel').pack(anchor=tk.W)
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        # Instruction input with custom scrollbar
        ttk.Label(left_frame, text="Instruction / 指示:").pack(anchor=tk.W)
        
        instr_frame = ttk.Frame(left_frame)
        instr_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.instruction_text = tk.Text(instr_frame, height=4, wrap=tk.WORD,
                                         bg=self.entry_bg, fg=self.entry_fg,
                                         insertbackground=self.entry_fg, borderwidth=1, relief=tk.SUNKEN)
        instr_scrollbar = ttk.Scrollbar(instr_frame, orient=tk.VERTICAL, command=self.instruction_text.yview)
        self.instruction_text.configure(yscrollcommand=instr_scrollbar.set)
        
        instr_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.instruction_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.instruction_text.insert(tk.END, "Enter your instructions / 以下の変更を行ってください：\n")
        
        # Context options
        context_frame = ttk.LabelFrame(left_frame, text="Context Options / コンテキストオプション", padding="5")
        context_frame.pack(fill=tk.X, pady=5)
        
        self.send_all_var = tk.BooleanVar(value=True)
        self.send_all_check = ttk.Checkbutton(
            context_frame, 
            text="Send ALL Files / すべてのファイルを送信",
            variable=self.send_all_var,
            command=self._on_send_all_toggle
        )
        self.send_all_check.pack(anchor=tk.W)
        
        # File list
        ttk.Label(left_frame, text="Files to Send / 送信ファイル:").pack(anchor=tk.W, pady=(10, 0))
        
        file_list_frame = ttk.Frame(left_frame)
        file_list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Canvas for scrollable file list with checkboxes
        self.file_canvas = tk.Canvas(file_list_frame, borderwidth=1, relief=tk.SUNKEN,
                                      bg=self.entry_bg, highlightthickness=0)
        file_scrollbar = ttk.Scrollbar(file_list_frame, orient=tk.VERTICAL, command=self.file_canvas.yview)
        self.file_inner_frame = ttk.Frame(self.file_canvas)
        
        self.file_canvas.configure(yscrollcommand=file_scrollbar.set)
        
        file_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.file_canvas_window = self.file_canvas.create_window((0, 0), window=self.file_inner_frame, anchor=tk.NW)
        
        self.file_inner_frame.bind("<Configure>", self._on_frame_configure)
        self.file_canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Bind mouse wheel
        self.file_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Stats label
        self.stats_label = ttk.Label(left_frame, text="Files: 0 | Size: 0 KB")
        self.stats_label.pack(anchor=tk.W)
        
        # Copy button
        self.copy_btn = ttk.Button(
            left_frame, 
            text="📋 Copy Prompt / プロンプトをコピー",
            command=self._copy_to_clipboard
        )
        self.copy_btn.pack(fill=tk.X, pady=10)
        
        # ====== Right Panel: Response ======
        right_frame = ttk.Frame(paned, padding="5")
        paned.add(right_frame, weight=1)
        
        # Header
        ttk.Label(right_frame, text="📥 Response / 復路", style='Header.TLabel').pack(anchor=tk.W)
        ttk.Separator(right_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        # Log area with custom scrollbar
        ttk.Label(right_frame, text="Log / ログ:").pack(anchor=tk.W)
        
        log_frame = ttk.Frame(right_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, state=tk.DISABLED,
                                 bg=self.entry_bg, fg=self.entry_fg, borderwidth=1, relief=tk.SUNKEN)
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure log text tags with better colors for dark mode
        self.log_text.tag_configure('success', foreground='#4caf50')  # Brighter green
        self.log_text.tag_configure('error', foreground='#f44336')    # Brighter red
        self.log_text.tag_configure('info', foreground='#64b5f6')     # Light blue
        self.log_text.tag_configure('warning', foreground='#ff9800')  # Orange
        
        # Apply button
        self.apply_btn = ttk.Button(
            right_frame,
            text="🔨 Apply Patch / パッチを適用",
            command=self._apply_from_clipboard
        )
        self.apply_btn.pack(fill=tk.X, pady=10)
        
        # Refresh button
        self.refresh_btn = ttk.Button(
            right_frame,
            text="🔄 Refresh / ファイルリスト更新",
            command=self._load_files
        )
        self.refresh_btn.pack(fill=tk.X)
    
    def _on_frame_configure(self, event):
        """Update scroll region when frame size changes."""
        self.file_canvas.configure(scrollregion=self.file_canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        """Update inner frame width when canvas resizes."""
        self.file_canvas.itemconfig(self.file_canvas_window, width=event.width)
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        self.file_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _load_files(self):
        """Load and display files from project."""
        self.log("Scanning files... / ファイルをスキャン中...", 'info')
        
        # Clear existing checkboxes
        for widget in self.file_inner_frame.winfo_children():
            widget.destroy()
        self.file_vars.clear()
        
        # Collect files
        self.files = collect_files(self.project_root)
        
        # Create checkboxes
        for file_path in self.files:
            rel_path = file_path.relative_to(self.project_root)
            rel_str = str(rel_path).replace('\\', '/')
            
            var = tk.BooleanVar(value=self.send_all_var.get())
            self.file_vars[file_path] = var
            
            cb = ttk.Checkbutton(
                self.file_inner_frame,
                text=rel_str,
                variable=var,
                command=self._update_stats
            )
            cb.pack(anchor=tk.W)
        
        self._update_stats()
        self.log(f"Found {len(self.files)} text files / {len(self.files)}個のテキストファイルを発見", 'success')
    
    def _on_send_all_toggle(self):
        """Handle 'Send ALL Files' checkbox toggle."""
        checked = self.send_all_var.get()
        for var in self.file_vars.values():
            var.set(checked)
        self._update_stats()
    
    def _update_stats(self):
        """Update file count and size statistics."""
        selected_files = [f for f, var in self.file_vars.items() if var.get()]
        total_size = sum(f.stat().st_size for f in selected_files if f.exists())
        
        self.stats_label.config(
            text=f"Files: {len(selected_files)}/{len(self.files)} | Size: {total_size / 1024:.1f} KB"
        )
    
    def _copy_to_clipboard(self):
        """Generate prompt and copy to clipboard."""
        instruction = self.instruction_text.get("1.0", tk.END).strip()
        if not instruction:
            messagebox.showwarning("警告", "指示を入力してください。")
            return
        
        selected_files = [f for f, var in self.file_vars.items() if var.get()]
        if not selected_files:
            messagebox.showwarning("警告", "少なくとも1つのファイルを選択してください。")
            return
        
        self.log("プロンプトを生成中...", 'info')
        
        # Build prompt
        xml_context = pack_context_xml(selected_files, self.project_root)
        
        prompt = f"""{SYSTEM_PROMPT}

{xml_context}

---
## User Instruction
{instruction}
"""
        
        # Copy to clipboard using tkinter
        self.root.clipboard_clear()
        self.root.clipboard_append(prompt)
        self.root.update()  # Required for clipboard to persist
        
        char_count = len(prompt)
        token_estimate = char_count // 4  # Rough estimate
        
        self.log(f"✅ クリップボードにコピーしました！", 'success')
        self.log(f"   文字数: {char_count:,}", 'info')
        self.log(f"   推定トークン数: ~{token_estimate:,}", 'info')
        self.log(f"   含まれるファイル数: {len(selected_files)}", 'info')
        
        messagebox.showinfo(
            "コピー完了",
            f"プロンプトをクリップボードにコピーしました！\n\n"
            f"文字数: {char_count:,}\n"
            f"推定トークン数: ~{token_estimate:,}\n"
            f"ファイル数: {len(selected_files)}\n\n"
            f"Google AI StudioやChatGPTにペーストしてください。"
        )
    
    def _apply_from_clipboard(self):
        """Apply patches from clipboard content."""
        try:
            clipboard_content = self.root.clipboard_get()
        except tk.TclError:
            messagebox.showerror("エラー", "クリップボードが空か、テキスト以外のデータが含まれています。")
            return
        
        if not clipboard_content.strip():
            messagebox.showwarning("警告", "クリップボードが空です。")
            return
        
        self.log("=" * 50, 'info')
        self.log(f"パッチを適用中 ({datetime.now().strftime('%H:%M:%S')})", 'info')
        
        # Parse patches
        patches = parse_patches(clipboard_content)
        
        if not patches:
            self.log("❌ クリップボードに有効なSEARCH/REPLACEブロックが見つかりません。", 'error')
            messagebox.showwarning(
                "パッチが見つかりません",
                "クリップボードに有効な <<<< SEARCH ... ==== ... >>>> ブロックが見つかりません。\n\n"
                "AIの応答が正しい形式になっているか確認してください。"
            )
            return
        
        self.log(f"{len(patches)}個のパッチを検出", 'info')
        
        # Apply each patch
        success_count = 0
        fail_count = 0
        
        for patch in patches:
            success, message = apply_patch(patch, self.project_root)
            if success:
                self.log(message, 'success')
                success_count += 1
            else:
                self.log(message, 'error')
                fail_count += 1
        
        # Summary
        self.log("-" * 30, 'info')
        summary = f"完了: {success_count}件成功, {fail_count}件失敗"
        self.log(summary, 'success' if fail_count == 0 else 'warning')
        
        if fail_count == 0:
            messagebox.showinfo("成功", f"すべてのパッチ（{success_count}件）を正常に適用しました！")
        else:
            messagebox.showwarning("部分的成功", summary)
    
    def log(self, message: str, tag: str = None):
        """Add a message to the log area."""
        self.log_text.config(state=tk.NORMAL)
        if tag:
            self.log_text.insert(tk.END, message + '\n', tag)
        else:
            self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def run(self):
        """Start the GUI main loop."""
        self.root.mainloop()


# ==============================================================================
# Entry Point
# ==============================================================================

def main():
    # Parse command line arguments
    cwd = Path.cwd()
    
    if '--cwd' in sys.argv:
        idx = sys.argv.index('--cwd')
        if idx + 1 < len(sys.argv):
            cwd = Path(sys.argv[idx + 1])
    
    if not cwd.exists():
        print(f"Error: Directory does not exist: {cwd}")
        sys.exit(1)
    
    print(f"Context Bridge")
    print(f"Project: {cwd}")
    print("Starting GUI...")
    
    app = ManualBridgeGUI(cwd)
    app.run()


if __name__ == '__main__':
    main()
