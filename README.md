# Claude API Manager

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.8+-green.svg)](https://pypi.org/project/PySide6/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](README_EN.md) | 中文

一个用于管理 Claude Code 第三方 API 配置的桌面 GUI 工具。

## 为什么开发这个工具？

 `cc switch` 功能太多。而我只是想在不同的第三方 API 提供商之间快速切换，不需要那么复杂的功能。

这个工具的设计理念是：**简单、轻量、本地、安全**。

## 安全性说明

> **本地操作，完全安全**
>
> - 只修改本地配置文件 `~/.claude/settings.json` 和 `~/.claude/my_settings.json`
> - 不会上传任何数据到远程服务器
> - 不会修改系统文件或其他应用程序
> - 源代码完全开源，可审计

## 功能特性

- 🚀 **配置管理** - 添加、编辑、复制、重命名、删除第三方 API 配置
- 🔄 **快速切换** - 一键切换不同的 API 提供商配置
- 📁 **自动管理** - 自动管理 `~/.claude/settings.json` 和 `~/.claude/my_settings.json`
- 🔍 **格式检查** - 启动时自动检查 JSON 文件格式，防止配置错误
- 🎨 **友好界面** - 使用 PySide6 构建的现代化 GUI 界面
- 🌐 **多语言支持** - 支持中文和英文界面，可随时切换
- 💻 **跨平台** - 支持 Windows 11 和 Ubuntu
- 🔒 **本地安全** - 只操作本地文件，不上传任何数据

## 支持的配置字段

| 配置项 | 环境变量名 | 说明 |
|--------|-----------|------|
| 供应商名称 | - | 配置的唯一标识名称 |
| API Key | `ANTHROPIC_AUTH_TOKEN` | API 认证密钥 |
| 请求地址 | `ANTHROPIC_BASE_URL` | API 基础 URL |
| 主模型 | `ANTHROPIC_MODEL` | 默认使用的模型 |
| 推理模型 | `ANTHROPIC_REASONING_MODEL` | 推理专用模型 |
| Opus 默认模型 | `ANTHROPIC_DEFAULT_OPUS_MODEL` | Opus 系列默认模型 |
| Sonnet 默认模型 | `ANTHROPIC_DEFAULT_SONNET_MODEL` | Sonnet 系列默认模型 |
| Haiku 默认模型 | `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Haiku 系列默认模型 |

## 快速开始

### 方式一：下载预编译版本（推荐）

1. 前往 [Releases](https://github.com/yourusername/claude_api_manager/releases) 页面
2. 下载最新版本的 `ClaudeAPIManager.exe`（Windows）
3. 双击运行即可，无需安装 Python

### 方式二：从源码运行

#### 环境要求

- Python 3.9 或更高版本
- Windows 11 或 Ubuntu 20.04+

#### 安装步骤

1. 克隆仓库

```bash
git clone https://github.com/yourusername/claude_api_manager.git
cd claude_api_manager
```

2. 创建虚拟环境（推荐）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 运行程序

```bash
python main.py
```

### 方式三：自行打包可执行文件

#### Windows

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包为单文件可执行程序
pyinstaller --name="ClaudeAPIManager" --windowed --onefile --icon=app-icon.ico --add-data="app-icon.png:." --add-data="app-icon.ico:." main.py

# 输出文件位于 dist/ClaudeAPIManager.exe
```

#### Linux

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包
pyinstaller --name="ClaudeAPIManager" --windowed --onefile --icon=app-icon.png main.py

# 输出文件位于 dist/ClaudeAPIManager
```

## 使用说明

### 首次运行

程序启动时会自动检查 `~/.claude/` 目录下的配置文件：
- `settings.json` - Claude Code 的主配置文件
- `my_settings.json` - 存储所有第三方配置的自定义文件

如果文件不存在，程序会自动创建空文件。

### 添加配置

1. 点击左上角的 **"+ 添加配置"** 按钮
2. 填写配置信息：
   - **供应商名称** - 给配置起个名字（如：glm-5、openai-compatible）
   - **API Key** - 你的 API 密钥
   - **请求地址** - API 的基础 URL
   - **主模型** - 默认使用的模型名称
   - 其他可选字段（推理模型、Opus/Sonnet/Haiku 默认模型）
3. 点击 **"保存"**

### 启动配置

1. 在列表中选中要使用的配置
2. 点击 **"▶ 启动"** 按钮
3. 该配置会被写入 `settings.json` 的 `env` 字段，Claude Code 会使用此配置

**注意**：同时只能有一个配置处于启动状态。

### 编辑配置

1. 选中要修改的配置
2. 点击 **"✎ 编辑"** 按钮
3. 修改配置信息
4. 点击 **"保存"**

### 复制配置

1. 选中要复制的配置
2. 点击 **"⎘ 复制"** 按钮
3. 会自动创建一个名为 `原名称-copy` 的新配置

### 重命名配置

1. 选中要重命名的配置
2. 点击 **"✎ 改名"** 按钮
3. 输入新名称
4. 确认即可

### 删除配置

1. 选中要删除的配置
2. 点击 **"✕ 删除"** 按钮
3. 确认删除操作

**注意**：如果删除的是当前启动的配置，`settings.json` 中的 `env` 字段也会被清除。

### 恢复默认

点击 **"⟲ 恢复默认"** 按钮可以清除当前启动的配置：
- 删除 `settings.json` 中的 `env` 字段
- 所有配置项变为未启动状态（灰色）
- Claude Code 将使用默认配置

### JSON 格式错误处理

如果启动时检测到 JSON 文件格式错误：
1. 会显示空列表，所有按钮被禁用
2. 弹出错误提示，告知具体哪个文件有问题
3. 请手动修复或删除该文件后，重新启动软件

### 切换语言

点击菜单栏的 **"语言 (Language)"** 菜单，选择 **"中文"** 或 **"English"** 即可切换界面语言。切换后会立即生效，无需重启软件。

## 配置文件说明

### my_settings.json

存储所有第三方配置：

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

Claude Code 的主配置文件，程序只修改其中的 `env` 字段：

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

## 常见问题

### Q: 这个软件安全吗？

**A: 完全安全。** 这个软件只操作本地配置文件（`~/.claude/settings.json` 和 `~/.claude/my_settings.json`），不会上传任何数据到远程服务器，也不会修改系统文件。源代码完全开源，可以放心使用。

### Q: 启动配置后 Claude Code 没有使用新配置？

A: 请确保：
1. 配置已正确保存
2. 点击了 **"▶ 启动"** 按钮
3. 重启 Claude Code 或重新加载配置

### Q: 如何备份配置？

A: 直接备份 `~/.claude/my_settings.json` 文件即可。

### Q: 配置文件在哪里？

A:
- Windows: `%USERPROFILE%\.claude\`
- Linux/macOS: `~/.claude/`

### Q: 程序无法启动，提示 JSON 格式错误？

A: 请检查 `~/.claude/settings.json` 和 `~/.claude/my_settings.json` 文件格式是否正确。可以使用 [JSONLint](https://jsonlint.com/) 等工具验证 JSON 格式。

### Q: 这个工具和 `cc switch` 有什么区别？

A: `cc switch` 是 Claude Code 官方的完整配置切换工具，功能较重。这个工具专注于：
- 快速切换第三方 API 配置
- 轻量级管理本地配置
- 无需重新下载 Claude Code

## 项目结构

```
claude_api_manager/
├── main.py                 # 程序入口
├── main_window.py          # 主窗口
├── edit_dialog.py          # 编辑配置对话框
├── config_manager.py       # 配置文件管理
├── translations.py         # 多语言支持
├── app-icon.png           # 应用图标
├── app-icon.ico           # Windows 图标
├── requirements.txt       # 依赖列表
└── README.md             # 说明文档
```

## 技术栈

- [Python 3.9+](https://www.python.org/)
- [PySide6](https://pypi.org/project/PySide6/) - Qt6 的 Python 绑定
- [PyInstaller](https://pyinstaller.org/) - 打包工具

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 许可证

本项目采用 [MIT](LICENSE) 许可证开源。

## 致谢

- [Claude Code](https://claude.ai/code) - Anthropic 的官方 CLI 工具
- [Qt](https://www.qt.io/) - 跨平台 GUI 框架
- [PySide6](https://wiki.qt.io/Qt_for_Python) - Qt 的 Python 绑定

---

如果这个项目对你有帮助，请给个 ⭐ Star 支持一下！
