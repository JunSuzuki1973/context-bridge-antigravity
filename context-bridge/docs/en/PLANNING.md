# Context Bridge for Antigravity - Planning Document

**Project Name**: Context Bridge for Antigravity  
**Version**: 1.0.0  
**Created**: 2026-01-17  
**Status**: ✅ Implementation Complete

---

## 📋 Executive Summary

Manual Bridge Mode is a "Human Relay" feature that enables the use of external web chatbots (Google AI Studio, ChatGPT, etc.) as inference engines without API keys. Implemented as an Antigravity skill, it provides a safe and efficient code generation and editing workflow through clipboard-based interaction.

### Key Value Propositions

1. **Zero Cost**: No API consumption, leverages free web chatbots
2. **Large-Scale Support**: Up to 1 million tokens context with Gemini 3.0 Pro
3. **Safety**: Dedicated GUI prevents terminal misoperations
4. **Simplicity**: Works with standard library only, no additional installation required

---

## 🎯 Background and Challenges

### Current Challenges

1. **API Cost Constraints**
   - GPT-4 and Gemini API require pay-per-use
   - Token consumption can be expensive for large projects
   - Burdensome for individual developers and students

2. **Context Limitations**
   - Many API-based AIs have context length restrictions
   - Cannot send entire project code at once

3. **Operational Risks**
   - Accidents from pasting large text directly into terminal
   - Risk of unintended command execution

### Solution

**Manual Bridge Mode** addresses these challenges through:

- Free chatbot usage via web browser
- Safe clipboard operations through dedicated GUI
- Efficiency through structured prompts and auto-patch application

---

## 🚀 Concept

### "ShotGun Code" × "Human Relay"

**ShotGun Code**: Send entire project context to AI at once  
**Human Relay**: Human mediates between AI and local environment via clipboard

This hybrid approach:
- Maximizes AI's reasoning capabilities
- Achieves zero API cost
- Ensures safety through human verification

### Target AI

**Google AI Studio (Gemini 3.0 Pro)** as primary recommendation:
- 1 million token support
- Free (as of January 2026)
- Can send entire project files

### Usage Flow

```
[Project]
     ↓ (Outbound)
  👤 User → 📋 Clipboard
     ↓
  🌐 Web AI (Google AI Studio)
     ↓ (Inbound)
  📋 Clipboard → 👤 User
     ↓
[Project]
```

---

## 🎨 Feature Requirements

### Essential Features

1. **File Collection**
   - Automatic `.gitignore` pattern recognition
   - Automatic binary file exclusion
   - Manual file selection/exclusion

2. **Prompt Generation**
   - File context structured in XML format
   - Automatic strict system prompt attachment
   - User instruction integration

3. **Patch Application**
   - Parse `<<<< SEARCH ... ==== ... >>>>` format
   - Support new file creation
   - Support file deletion
   - Fuzzy matching (whitespace tolerance)

4. **GUI**
   - Cross-platform with tkinter
   - 2-pane layout (outbound/inbound)
   - Real-time log display
   - Statistics (file count, size, token estimate)

### Recommended Features (Future Extensions)

- [ ] History management (record applied patches)
- [ ] Undo/Redo functionality
- [ ] Project presets (frequently used file sets)
- [ ] Multi-AI support (optimization for Claude, GPT-4, etc.)
- [ ] Conflict resolution assistance

---

## 🏗️ Technology Selection

### Python + tkinter

**Selection Rationale**:
- Cross-platform (Windows/macOS/Linux)
- Standard library, no additional installation
- Suitable for simple GUI

**Alternatives Considered**:
- ❌ Electron: Overkill, large distribution size
- ❌ PyQt: License issues, many dependencies
- ✅ tkinter: Simple, lightweight, standard

### Clipboard Operations

Uses `tkinter` standard features:
- `clipboard_clear()`, `clipboard_append()`, `clipboard_get()`
- No external library needed (no `pyperclip`)

---

## 📊 Success Metrics

### Short-term (1 month)

- ✅ Complete basic functionality
- ✅ Verify operation with demo project
- [ ] Acquire 5+ beta testers

### Mid-term (3 months)

- [ ] Used in 100+ projects
- [ ] Collect and fix 10+ bug reports
- [ ] Improve features based on user feedback

### Long-term (6 months)

- [ ] Listed in Antigravity official skill catalog
- [ ] 500 monthly active users
- [ ] Community contributions (5+ pull requests)

---

## 🎯 Target Users

### Primary Persona

**Name**: Taro Tanaka (College Student)  
**Age**: 21  
**Occupation**: Information Science Major  
**Challenges**: 
- Wants to use AI for assignments but has no budget for API keys
- Needs AI help with large project refactoring

**Value of This Skill**:
- Can send all code with free Google AI Studio
- Safe code editing

### Secondary Persona

**Name**: Hanako Sato (Freelance Engineer)  
**Age**: 32  
**Occupation**: Web Application Developer  
**Challenges**:
- Wants to save API costs on client projects
- Wants to use multiple AI services flexibly

**Value of This Skill**:
- Cost reduction with zero API consumption
- Works with Google, OpenAI, Anthropic

---

## 🛣️ Roadmap

### v1.0 (Current) ✅
- [x] Basic GUI implementation
- [x] File collection feature
- [x] Prompt generation
- [x] Patch application
- [x] Demo project
- [x] Documentation

### v1.1 (2026 Q2)
- [ ] History management
- [ ] Preset feature
- [ ] Multi-language support (English UI)

### v2.0 (2026 Q3)
- [ ] Plugin system
- [ ] Custom system prompts
- [ ] Team sharing features

---

## 💡 Differentiation

### Comparison with Similar Tools

| Feature | Manual Bridge | aider | cursor | GitHub Copilot |
|---------|--------------|-------|--------|----------------|
| **No API Required** | ✅ | ❌ | ❌ | ❌ |
| **Large Context** | ✅ (1M) | ⚠️ (Limited) | ⚠️ (Limited) | ❌ (Limited) |
| **GUI Operation** | ✅ | ❌ (CLI) | ✅ | ✅ (IDE Integration) |
| **Setup Cost** | ✅ Free | 💰 API Key Required | 💰 Subscription | 💰 Subscription |
| **Offline** | ❌ | ❌ | ❌ | ❌ |

### Unique Strengths

1. **Completely Free**: No API key, uses web AI
2. **Flexibility**: Works with any chatbot AI
3. **Safety**: Dedicated GUI prevents misoperations
4. **Lightweight**: Standard library only, easy installation

---

## 📝 Notes

### Naming Origin

- **Manual Bridge**: Manually bridges connections
- **Airlock**: Like a spacecraft airlock, safely connects external (Web AI) and internal (local)

### Design Philosophy

**KISS Principle**: Keep It Simple, Stupid
- No complex features added
- User-friendly UI
- Minimal dependencies

**Human-Centered Design**:
- Don't fully automate with AI, human verifies
- Familiar clipboard operations
- Transparent log display

---

## 📞 Contact

Project Owner: [JUN SUZUKI](https://junsuzuki-ai-agency.xyz/)  
Created: 2026-01-17  
Next Review: 2026-02-17
