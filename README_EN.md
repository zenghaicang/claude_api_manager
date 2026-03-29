# Claude API Manager

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.8+-green.svg)](https://pypi.org/project/PySide6/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

English | [中文](README.md)

A desktop GUI tool for managing Claude Code third-party API configurations.

## Why Develop This Tool?

 `cc switch` command in Claude Code is too heavy . I just want to quickly switch between different third-party API providers without all that complexity.

This tool is designed with the philosophy: **Simple, Lightweight, Local, Secure**.

## Security Statement

> **Local Operations, Completely Safe**
>
> - Only modifies local configuration files `~/.claude/settings.json` and `~/.claude/my_settings.json`
> - Does not upload any data to remote servers
> - Does not modify system files or other applications
> - Fully open-source code, auditable

## Features

- 🚀 **Configuration Management** - Add, edit, copy, rename, and delete third-party API configurations
- 🔄 **Quick Switching** - One-click switching between different API providers
- 📁 **Automatic Management** - Automatically manages `~/.claude/settings.json` and `~/.claude/my_settings.json`
- 🔍 **Format Checking** - Automatically checks JSON file format on startup to prevent configuration errors
- 🎨 **User-Friendly Interface** - Modern GUI built with PySide6
- 🌐 **Multi-Language Support** - Supports Chinese and English interfaces, switchable anytime
- 💻 **Cross-Platform** - Supports Windows 11 and Ubuntu
- 🔒 **Local Security** - Only operates on local files, no data upload

## Supported Configuration Fields

| Configuration | Environment Variable | Description |
|--------------|---------------------|-------------|
| Provider Name | - | Unique identifier for the configuration |
| API Key | `ANTHROPIC_AUTH_TOKEN` | API authentication key |
| Base URL | `ANTHROPIC_BASE_URL` | API base URL |
| Main Model | `ANTHROPIC_MODEL` | Default model to use |
| Reasoning Model | `ANTHROPIC_REASONING_MODEL` | Model for reasoning tasks |
| Opus Default Model | `ANTHROPIC_DEFAULT_OPUS_MODEL` | Default Opus series model |
| Sonnet Default Model | `ANTHROPIC_DEFAULT_SONNET_MODEL` | Default Sonnet series model |
| Haiku Default Model | `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Default Haiku series model |

## Quick Start

### Option 1: Download Pre-built Version (Recommended)

1. Go to the [Releases](https://github.com/yourusername/claude_api_manager/releases) page
2. Download the latest `ClaudeAPIManager.exe` (Windows)
3. Double-click to run, no Python installation required

### Option 2: Run from Source

#### Requirements

- Python 3.9 or higher
- Windows 11 or Ubuntu 20.04+

#### Installation Steps

1. Clone the repository

```bash
git clone https://github.com/yourusername/claude_api_manager.git
cd claude_api_manager
```

2. Create virtual environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the program

```bash
python main.py
```

### Option 3: Build Executable Yourself

#### Windows

```bash
# Install PyInstaller
pip install pyinstaller

# Build single-file executable
pyinstaller --name="ClaudeAPIManager" --windowed --onefile --icon=app-icon.ico --add-data="app-icon.png:." --add-data="app-icon.ico:." main.py

# Output file located at dist/ClaudeAPIManager.exe
```

#### Linux

```bash
# Install PyInstaller
pip install pyinstaller

# Build
pyinstaller --name="ClaudeAPIManager" --windowed --onefile --icon=app-icon.png main.py

# Output file located at dist/ClaudeAPIManager
```

## Usage Guide

### First Run

The program automatically checks configuration files in `~/.claude/` directory on startup:
- `settings.json` - Claude Code's main configuration file
- `my_settings.json` - Custom file for storing all third-party configurations

If files don't exist, the program will create empty files automatically.

### Add Configuration

1. Click the **"+ Add Config"** button in the top-left
2. Fill in configuration details:
   - **Provider Name** - Name your configuration (e.g., glm-5, openai-compatible)
   - **API Key** - Your API key
   - **Base URL** - API base URL
   - **Main Model** - Default model name
   - Other optional fields (reasoning model, Opus/Sonnet/Haiku default models)
3. Click **"Save"**

### Activate Configuration

1. Select the configuration you want to use from the list
2. Click the **"▶ Activate"** button
3. The configuration will be written to the `env` field in `settings.json`, and Claude Code will use this configuration

**Note**: Only one configuration can be active at a time.

### Edit Configuration

1. Select the configuration you want to modify
2. Click the **"✎ Edit"** button
3. Modify the configuration details
4. Click **"Save"**

### Copy Configuration

1. Select the configuration you want to copy
2. Click the **"⎘ Copy"** button
3. A new configuration named `original-name-copy` will be created automatically

### Rename Configuration

1. Select the configuration you want to rename
2. Click the **"✎ Rename"** button
3. Enter the new name
4. Confirm

### Delete Configuration

1. Select the configuration you want to delete
2. Click the **"✕ Delete"** button
3. Confirm the deletion

**Note**: If you delete the currently active configuration, the `env` field in `settings.json` will also be cleared.

### Reset to Default

Click the **"⟲ Reset to Default"** button to clear the currently active configuration:
- Deletes the `env` field in `settings.json`
- All configurations become inactive (gray)
- Claude Code will use default configuration

### JSON Format Error Handling

If a JSON format error is detected on startup:
1. An empty list will be displayed, all buttons disabled
2. An error dialog will show which file has the problem
3. Please manually fix or delete the file, then restart the software

### Switch Language

Click the **"Language (语言)"** menu in the menu bar, select **"中文"** or **"English"** to switch the interface language. The change takes effect immediately without restarting.

## Configuration Files

### my_settings.json

Stores all third-party configurations:

```json
{
  "glm-5": {
    "ANTHROPIC_AUTH_TOKEN": "your-api-key",
    "ANTHROPIC_BASE_URL": "https://api.example.com/v1",
    "ANTHROPIC_MODEL": "glm-5",
    "ANTHROPIC_REASONING_MODEL": "glm-5-reasoning",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-5-opus",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-5-sonnet",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "glm-5-haiku"
  },
  "openai-compatible": {
    ...
  }
}
```

### settings.json

Claude Code's main configuration file, the program only modifies the `env` field:

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your-api-key",
    "ANTHROPIC_BASE_URL": "https://api.example.com/v1",
    "ANTHROPIC_MODEL": "glm-5",
    ...
  },
  "enabledPlugins": {
    ...
  }
}
```

## FAQ

### Q: Is this software safe?

**A: Completely safe.** This software only operates on local configuration files (`~/.claude/settings.json` and `~/.claude/my_settings.json`), does not upload any data to remote servers, and does not modify system files. The source code is fully open-source and can be audited with confidence.

### Q: Claude Code doesn't use the new configuration after activation?

A: Please ensure:
1. The configuration is saved correctly
2. You clicked the **"▶ Activate"** button
3. Restart Claude Code or reload the configuration

### Q: How to backup configurations?

A: Simply backup the `~/.claude/my_settings.json` file.

### Q: Where are the configuration files?

A:
- Windows: `%USERPROFILE%\.claude\`
- Linux/macOS: `~/.claude/`

### Q: Program won't start, shows JSON format error?

A: Please check if the JSON format in `~/.claude/settings.json` and `~/.claude/my_settings.json` is correct. You can use tools like [JSONLint](https://jsonlint.com/) to validate JSON format.

### Q: What's the difference between this tool and `cc switch`?

A: `cc switch` is Claude Code's official complete configuration switching tool with heavier functionality. This tool focuses on:
- Quickly switching third-party API configurations
- Lightweight local configuration management
- No need to re-download Claude Code

## Project Structure

```
claude_api_manager/
├── main.py                 # Program entry
├── main_window.py          # Main window
├── edit_dialog.py          # Edit configuration dialog
├── config_manager.py       # Configuration file management
├── translations.py         # Multi-language support
├── app-icon.png           # Application icon
├── app-icon.ico           # Windows icon
├── requirements.txt       # Dependencies list
└── README.md             # Documentation
```

## Tech Stack

- [Python 3.9+](https://www.python.org/)
- [PySide6](https://pypi.org/project/PySide6/) - Qt6 Python bindings
- [PyInstaller](https://pyinstaller.org/) - Packaging tool

## Contributing

Issues and Pull Requests are welcome!

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open-sourced under the [MIT](LICENSE) License.

## Acknowledgments

- [Claude Code](https://claude.ai/code) - Anthropic's official CLI tool
- [Qt](https://www.qt.io/) - Cross-platform GUI framework
- [PySide6](https://wiki.qt.io/Qt_for_Python) - Qt Python bindings

---

If this project helps you, please give it a ⭐ Star!
