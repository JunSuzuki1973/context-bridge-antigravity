# Context Bridge for Antigravity - Development Repository

This is the **development repository** for Context Bridge, an Antigravity skill.

## 📂 Repository Structure

```
ContextBridge/                      ← Development project root
├── .agent/                         ← Development workflows (not distributed)
│   └── workflows/
│       └── open-airlock.md        ← For testing during development
│
├── context-bridge/                 ← ★ THE SKILL (distribute this folder)
│   ├── SKILL.md                    ← Skill definition (required)
│   ├── workflows/                  ← User-facing workflows
│   │   └── open-airlock.md         ← /open-airlock command
│   ├── tools/
│   │   └── bridge_gui.py           ← Main GUI application
│   ├── docs/
│   │   ├── gui_screenshot.png
│   │   ├── en/                     ← English documentation
│   │   └── ja/                     ← Japanese documentation
│   ├── README.md                   ← English README
│   ├── README.ja.md                ← Japanese README
│   └── LICENSE                     ← MIT License
│
├── demo/                           ← Demo project (block breaker game)
│   ├── index.html
│   ├── style.css
│   └── game.js
│
└── GITHUB_UPLOAD.md                ← Development notes
```

## 🎯 For Users

**Download the skill**: [GitHub Releases](https://github.com/JunSuzuki1973/context-bridge-antigravity/releases)

**Installation**:
1. Download and extract ZIP
2. Copy `context-bridge/` folder to `~/.agent/skills/`
3. Restart Antigravity

**Documentation**: See [context-bridge/README.md](context-bridge/README.md)

## 👨‍💻 For Developers

### Development Setup

1. Clone this repository
2. The `context-bridge/` folder is the actual skill
3. Test changes by copying to `~/.agent/skills/`

### Project Layout

- **`context-bridge/`** - The distributable skill package
- **`.agent/`** - Development-only workflows
- **`demo/`** - Test project for the GUI

### Making Changes

1. Edit files in `context-bridge/`
2. Test by installing to `~/.agent/skills/`
3. Commit and push changes
4. Create new release when ready

### Creating a Release

1. Update version in `context-bridge/SKILL.md`
2. Commit changes
3. Create GitHub release with tag (e.g., `v1.1.0`)
4. GitHub automatically packages `context-bridge/` in the ZIP

## 📄 License

MIT License - See [context-bridge/LICENSE](context-bridge/LICENSE)

## 🔗 Links

- **GitHub Repository**: https://github.com/JunSuzuki1973/context-bridge-antigravity
- **Developer**: [JUN SUZUKI](https://junsuzuki-ai-agency.xyz/)
