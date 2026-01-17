# Context Bridge for Antigravity

**[日本語版 README はこちら](README.ja.md)** | **[Japanese README is here](README.ja.md)**

External Web AI (Google AI Studio, ChatGPT, etc.) as an inference engine without API keys using a "Human Relay" approach.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

## 🎯 Features

- **Zero API Consumption**: Clipboard-based interaction means no API keys or token usage
- **Large Context Support**: Up to 1 million tokens with Gemini 1.5 Pro
- **Safe Operation**: Dedicated GUI prevents accidental paste into terminal
- **Auto Patch Application**: Automatically detects and applies changes from AI responses
- **Standard Library Only**: No additional installations required (uses Python's built-in `tkinter`)

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- Antigravity (Google Deepmind AI Agent)

### Setup Instructions

#### Method 1: Let Antigravity Install Automatically (Recommended) ⚡

Simply instruct Antigravity in chat, and it will install automatically:

```
Please install this skill (Manual Bridge Mode) to the appropriate location.
```

Or:

```
Install the ContextBridge folder to the skills directory
```

Antigravity will automatically:
1. Read and understand this README
2. Create the appropriate directory structure
3. Copy necessary files
4. Recognize the skill

#### Method 2: Manual Installation

1. **Copy the skill folder**

   Copy this folder to your Antigravity skills directory:
   
   ```bash
   # Windows
   xcopy /E /I ContextBridge "%USERPROFILE%\.agent\skills\manual_bridge"
   
   # macOS/Linux
   cp -r ContextBridge ~/.agent/skills/manual_bridge
   ```

2. **Verify file structure**

   Ensure the following files are in place:
   
   ```
   ~/.agent/skills/manual_bridge/
   ├── tools/
   │   └── bridge_gui.py          # Main GUI application
   ├── skills/
   │   └── manual_bridge.md       # Skill definition file
   ├── .agent/
   │   └── workflows/
   │       └── open-airlock.md    # Antigravity workflow
   ├── docs/
   │   ├── en/                    # English documentation
   │   │   ├── README.md
   │   │   ├── PLANNING.md
   │   │   └── SPECIFICATION.md
   │   └── ja/                    # Japanese documentation
   │       ├── README.md
   │       ├── PLANNING.md
   │       └── SPECIFICATION.md
   ├── demo/                      # Demo project (can be deleted)
   │   ├── index.html
   │   ├── style.css
   │   └── game.js
   └── LICENSE                    # License information
   ```

3. **Activate in Antigravity**

   Restart Antigravity or run:
   
   ```
   reload skills
   ```

## 🚀 Usage

### 1. Launch GUI

In Antigravity chat, enter:

```
/open-airlock
```

Or use natural language:
```
Launch Context Bridge
```

### 2. Outbound (Project → Web AI)

1. **Enter instruction**: Type your task in the "Instruction" field
   ```
   Double the ball speed and randomize block colors
   ```

2. **Select files**: All files are selected by default (adjust as needed)

3. **Copy**: Click "📋 Copy Prompt to Clipboard" button

4. **Paste to Web AI**: 
   - Open [Google AI Studio](https://aistudio.google.com/)
   - Paste with Ctrl+V and send

### 3. Inbound (Web AI → Project)

1. **Copy AI response**: Ctrl+A → Ctrl+C

2. **Apply**: Return to GUI and click "🔨 Apply Patch" button

3. **Verify**: Check the log area for results

## 🎨 Demo Project

A simple block breaker game is included in the `demo/` folder.

**Test method**:
```bash
python tools/bridge_gui.py --cwd demo
```

Example instructions:
- "Double the ball speed"
- "Make the paddle larger"
- "Add gradient colors to blocks"

## 📖 Recommended Web AI

| AI | Context Length | Recommendation | URL |
|----|---------------|----------------|-----|
| **Google AI Studio (Gemini 1.5 Pro)** | 1M tokens | ⭐⭐⭐ | https://aistudio.google.com/ |
| ChatGPT (GPT-4) | 128K tokens | ⭐⭐ | https://chat.openai.com/ |
| Claude.ai | 200K tokens | ⭐⭐ | https://claude.ai/ |

## 🔧 Troubleshooting

### Patches Not Applying

**Cause**: AI output format is incorrect

**Solution**: 
- Verify `<<<< SEARCH ... ==== ... >>>>` blocks exist in AI response
- Ensure system prompt was correctly transmitted (usually auto-inserted)

### File Not Found

**Cause**: Incorrect path specification

**Solution**:
- Verify paths use `/` separators
- Check paths are relative to project root

### Character Encoding Issues

**Cause**: Encoding problems

**Solution**:
- Save files as UTF-8
- Add `# -*- coding: utf-8 -*-` at top of files with non-ASCII characters

### GUI Won't Start

**Cause**: tkinter not installed

**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (with Homebrew)
brew install python-tk

# Windows
# Usually pre-installed. Reinstall Python if needed
```

## 🤝 Contributing

Bug reports and feature requests are welcome:
- Issues: Project GitHub repository
- Pull Requests: Always welcome!

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🔗 Related Links

- [Antigravity](https://deepmind.google/technologies/gemini/antigravity/)
- [Google AI Studio](https://aistudio.google.com/)
- [Technical Specification](docs/en/SPECIFICATION.md)
- [Planning Document](docs/en/PLANNING.md)

## 📞 Support

If you have questions or issues:
1. First check [Troubleshooting](#-troubleshooting)
2. Review [Technical Specification](docs/en/SPECIFICATION.md) for details
3. If still unresolved, create an Issue

---

**Developer**: [JUN SUZUKI](https://junsuzuki-ai-agency.xyz/)  
**Version**: 1.0.0  
**Last Updated**: 2026-01-17
