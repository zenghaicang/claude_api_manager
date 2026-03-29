"""
Claude API Manager - 多语言支持
"""

TRANSLATIONS = {
    "zh": {
        # 窗口标题
        "window_title": "Claude API Manager",
        "app_name": "Claude API Manager",

        # 主界面
        "main_title": "Claude 第三方站点配置管理",
        "main_desc": "管理 ~/.claude/settings.json 的第三方 API 配置",
        "empty_list": "暂无配置，点击「添加配置」创建",
        "empty_list_error": "配置文件格式错误，无法加载配置列表",

        # 按钮
        "btn_add": "+ 添加配置",
        "btn_reset": "⟲ 恢复默认",
        "btn_activate": "▶ 启动",
        "btn_edit": "✎ 编辑",
        "btn_copy": "⎘ 复制",
        "btn_rename": "✎ 改名",
        "btn_delete": "✕ 删除",
        "btn_save": "保存",
        "btn_cancel": "取消",
        "btn_close": "关闭",

        # 状态
        "status_active": "(已启动)",
        "status_inactive": "○",
        "status_active_symbol": "●",

        # 对话框标题
        "dlg_add_config": "添加配置",
        "dlg_edit_config": "编辑配置",
        "dlg_rename": "重命名配置",
        "dlg_confirm_delete": "确认删除",
        "dlg_confirm_reset": "确认恢复默认",
        "dlg_json_error": "配置文件格式错误",
        "dlg_validation_error": "验证错误",

        # 对话框内容
        "msg_confirm_delete": "确定要删除配置 '{}' 吗?\n此操作不可恢复。",
        "msg_confirm_reset": "确定要恢复默认设置吗？\n这将清除当前启动的配置，settings.json 中的 env 字段将被删除。",
        "msg_json_error": "以下配置文件格式错误：\n\n{}\n\n请手动修复或删除该文件后，重新启动软件。",
        "msg_config_exists": "配置 '{}' 已存在",
        "msg_config_not_found": "配置 '{}' 不存在",

        # 表单标签
        "lbl_provider_name": "供应商名称 *:",
        "lbl_api_key": "API Key *:",
        "lbl_base_url": "请求地址 *:",
        "lbl_main_model": "主模型 *:",
        "lbl_reasoning_model": "推理模型:",
        "lbl_opus_model": "Opus 默认模型:",
        "lbl_sonnet_model": "Sonnet 默认模型:",
        "lbl_haiku_model": "Haiku 默认模型:",
        "lbl_new_name": "请输入新的配置名称:",

        # 占位符
        "placeholder_provider": "例如: glm-5",
        "placeholder_required": "请输入{}",

        # 验证错误
        "err_name_empty": "供应商名称不能为空",
        "err_field_empty": "{} 不能为空",

        # 菜单
        "menu_language": "语言 (Language)",
        "lang_zh": "中文",
        "lang_en": "English",
    },
    "en": {
        # Window title
        "window_title": "Claude API Manager",
        "app_name": "Claude API Manager",

        # Main interface
        "main_title": "Claude Third-Party API Configuration",
        "main_desc": "Manage third-party API configurations in ~/.claude/settings.json",
        "empty_list": "No configurations. Click \"Add Config\" to create one.",
        "empty_list_error": "Configuration file format error. Unable to load configuration list.",

        # Buttons
        "btn_add": "+ Add Config",
        "btn_reset": "⟲ Reset to Default",
        "btn_activate": "▶ Activate",
        "btn_edit": "✎ Edit",
        "btn_copy": "⎘ Copy",
        "btn_rename": "✎ Rename",
        "btn_delete": "✕ Delete",
        "btn_save": "Save",
        "btn_cancel": "Cancel",
        "btn_close": "Close",

        # Status
        "status_active": "(Active)",
        "status_inactive": "○",
        "status_active_symbol": "●",

        # Dialog titles
        "dlg_add_config": "Add Configuration",
        "dlg_edit_config": "Edit Configuration",
        "dlg_rename": "Rename Configuration",
        "dlg_confirm_delete": "Confirm Delete",
        "dlg_confirm_reset": "Confirm Reset",
        "dlg_json_error": "Configuration File Format Error",
        "dlg_validation_error": "Validation Error",

        # Dialog messages
        "msg_confirm_delete": "Are you sure you want to delete the configuration '{}'?\nThis action cannot be undone.",
        "msg_confirm_reset": "Are you sure you want to reset to default settings?\nThis will clear the currently active configuration and delete the env field in settings.json.",
        "msg_json_error": "The following configuration file(s) have format errors:\n\n{}\n\nPlease manually fix or delete the file(s), then restart the software.",
        "msg_config_exists": "Configuration '{}' already exists",
        "msg_config_not_found": "Configuration '{}' not found",

        # Form labels
        "lbl_provider_name": "Provider Name *:",
        "lbl_api_key": "API Key *:",
        "lbl_base_url": "Base URL *:",
        "lbl_main_model": "Main Model *:",
        "lbl_reasoning_model": "Reasoning Model:",
        "lbl_opus_model": "Opus Default Model:",
        "lbl_sonnet_model": "Sonnet Default Model:",
        "lbl_haiku_model": "Haiku Default Model:",
        "lbl_new_name": "Please enter a new configuration name:",

        # Placeholders
        "placeholder_provider": "e.g., glm-5",
        "placeholder_required": "Enter {}",

        # Validation errors
        "err_name_empty": "Provider name cannot be empty",
        "err_field_empty": "{} cannot be empty",

        # Menu
        "menu_language": "Language (语言)",
        "lang_zh": "中文",
        "lang_en": "English",
    }
}


class Translator:
    """翻译器类"""

    def __init__(self, language="zh"):
        self.language = language

    def set_language(self, language: str):
        """设置语言"""
        if language in TRANSLATIONS:
            self.language = language

    def get_language(self) -> str:
        """获取当前语言"""
        return self.language

    def t(self, key: str, *args) -> str:
        """
        获取翻译文本
        :param key: 翻译键
        :param args: 格式化参数
        :return: 翻译后的文本
        """
        text = TRANSLATIONS.get(self.language, TRANSLATIONS["zh"]).get(key, key)
        if args:
            try:
                text = text.format(*args)
            except:
                pass
        return text


# 全局翻译器实例
translator = Translator("zh")


def set_language(language: str):
    """设置全局语言"""
    translator.set_language(language)


def get_language() -> str:
    """获取当前语言"""
    return translator.get_language()


def t(key: str, *args) -> str:
    """快捷翻译函数"""
    return translator.t(key, *args)
