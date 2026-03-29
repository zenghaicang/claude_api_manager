"""
Claude API Manager - 配置文件读写模块
"""
import json
import os
from pathlib import Path
from typing import Dict, Optional, Any, Tuple


class JSONFormatError(Exception):
    """JSON 格式错误异常"""
    pass


class ConfigManager:
    """管理 Claude 配置文件"""

    # 配置字段模板
    CONFIG_FIELDS = [
        "ANTHROPIC_AUTH_TOKEN",
        "ANTHROPIC_BASE_URL",
        "ANTHROPIC_MODEL",
        "ANTHROPIC_REASONING_MODEL",
        "ANTHROPIC_DEFAULT_OPUS_MODEL",
        "ANTHROPIC_DEFAULT_SONNET_MODEL",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL",
    ]

    def __init__(self):
        self.claude_dir = self._get_claude_dir()
        self.settings_file = self.claude_dir / "settings.json"
        self.my_settings_file = self.claude_dir / "my_settings.json"

    def _get_claude_dir(self) -> Path:
        """获取 Claude 配置目录（跨平台）"""
        home = Path.home()
        return home / ".claude"

    def ensure_files_exist(self):
        """确保配置文件存在，不存在则创建"""
        self.claude_dir.mkdir(parents=True, exist_ok=True)

        if not self.settings_file.exists():
            self._save_json(self.settings_file, {})

        if not self.my_settings_file.exists():
            self._save_json(self.my_settings_file, {})

    def _load_json(self, file_path: Path, validate: bool = False) -> Dict:
        """
        加载 JSON 文件
        validate: 如果为 True，格式错误时抛出 JSONFormatError 异常
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content.strip():
                    return {}
                return json.loads(content)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            if validate:
                raise JSONFormatError(f"文件 '{file_path}' JSON 格式错误: {e}")
            return {}

    def validate_json_files(self) -> Tuple[bool, str]:
        """
        验证所有 JSON 文件格式
        返回: (是否全部有效, 错误信息)
        """
        files_to_check = [
            ("设置文件", self.settings_file),
            ("配置文件", self.my_settings_file),
        ]

        errors = []
        for file_desc, file_path in files_to_check:
            if not file_path.exists():
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():
                        json.loads(content)
            except json.JSONDecodeError as e:
                errors.append(f"{file_desc} ({file_path.name}): {e}")

        if errors:
            return False, "\n".join(errors)
        return True, ""

    def _save_json(self, file_path: Path, data: Dict):
        """保存 JSON 文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_all_configs(self, validate: bool = False) -> Dict[str, Dict[str, str]]:
        """获取所有配置（从 my_settings.json）"""
        return self._load_json(self.my_settings_file, validate=validate)

    def get_active_config_name(self) -> Optional[str]:
        """
        获取当前启用的配置名称
        通过比较 settings.json 的 env 与 my_settings.json 中的配置
        """
        settings = self._load_json(self.settings_file)
        env = settings.get("env", {})

        if not env:
            return None

        all_configs = self.get_all_configs()

        for name, config in all_configs.items():
            # 比较配置内容是否匹配（至少比较关键字段）
            if self._config_matches(env, config):
                return name

        return None

    def _config_matches(self, env: Dict, config: Dict) -> bool:
        """检查 env 是否与 config 匹配"""
        # 比较关键字段
        key_fields = ["ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL", "ANTHROPIC_MODEL"]
        for field in key_fields:
            if env.get(field) != config.get(field):
                return False
        return True

    def save_config(self, name: str, config: Dict[str, str]):
        """
        保存配置到 my_settings.json
        如果该配置当前是启动状态，同时更新 settings.json
        """
        all_configs = self.get_all_configs()
        all_configs[name] = config
        self._save_json(self.my_settings_file, all_configs)

        # 如果这是当前启用的配置，同时更新 settings.json
        if self.get_active_config_name() == name:
            self.activate_config(name)

    def delete_config(self, name: str):
        """删除配置"""
        all_configs = self.get_all_configs()
        if name in all_configs:
            del all_configs[name]
            self._save_json(self.my_settings_file, all_configs)

        # 如果删除的是当前启用的配置，清空 settings.json 的 env
        if self.get_active_config_name() == name:
            settings = self._load_json(self.settings_file)
            if "env" in settings:
                del settings["env"]
            self._save_json(self.settings_file, settings)

    def rename_config(self, old_name: str, new_name: str):
        """重命名配置"""
        all_configs = self.get_all_configs()
        if old_name in all_configs:
            all_configs[new_name] = all_configs.pop(old_name)
            self._save_json(self.my_settings_file, all_configs)

        # 如果重命名的是当前启用的配置，需要更新 settings.json
        if self.get_active_config_name() == old_name:
            self.activate_config(new_name)

    def duplicate_config(self, name: str) -> str:
        """复制配置，返回新名称"""
        all_configs = self.get_all_configs()
        if name not in all_configs:
            raise ValueError(f"配置 '{name}' 不存在")

        # 生成新名称
        new_name = f"{name}-copy"
        counter = 1
        while new_name in all_configs:
            new_name = f"{name}-copy{counter}"
            counter += 1

        all_configs[new_name] = all_configs[name].copy()
        self._save_json(self.my_settings_file, all_configs)
        return new_name

    def activate_config(self, name: str):
        """
        激活配置：将 my_settings.json 中的配置复制到 settings.json 的 env
        """
        all_configs = self.get_all_configs()
        if name not in all_configs:
            raise ValueError(f"配置 '{name}' 不存在")

        settings = self._load_json(self.settings_file)
        settings["env"] = all_configs[name].copy()
        self._save_json(self.settings_file, settings)

    def deactivate_current_config(self):
        """停用当前配置"""
        settings = self._load_json(self.settings_file)
        if "env" in settings:
            del settings["env"]
        self._save_json(self.settings_file, settings)

    def create_empty_config(self) -> Dict[str, str]:
        """创建空配置模板"""
        return {field: "" for field in self.CONFIG_FIELDS}
