"""
Claude API Manager - 编辑配置对话框
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt
from typing import Dict, Optional

from translations import t


class EditDialog(QDialog):
    """添加/编辑配置对话框"""

    def __init__(self, parent=None, config_name: str = "", config_data: Optional[Dict[str, str]] = None):
        super().__init__(parent)
        self.setWindowTitle(t("dlg_add_config") if not config_name else t("dlg_edit_config"))
        self.setMinimumWidth(500)
        self.config_data = config_data or {}
        self.original_name = config_name
        self.result_name = ""
        self.result_config = {}

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # 表单布局
        form_layout = QFormLayout()

        # 供应商名称
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(t("placeholder_provider"))
        form_layout.addRow(t("lbl_provider_name"), self.name_input)

        # 配置字段
        self.field_inputs = {}
        field_labels = {
            "ANTHROPIC_AUTH_TOKEN": t("lbl_api_key"),
            "ANTHROPIC_BASE_URL": t("lbl_base_url"),
            "ANTHROPIC_MODEL": t("lbl_main_model"),
            "ANTHROPIC_REASONING_MODEL": t("lbl_reasoning_model"),
            "ANTHROPIC_DEFAULT_OPUS_MODEL": t("lbl_opus_model"),
            "ANTHROPIC_DEFAULT_SONNET_MODEL": t("lbl_sonnet_model"),
            "ANTHROPIC_DEFAULT_HAIKU_MODEL": t("lbl_haiku_model"),
        }

        for field, label in field_labels.items():
            input_widget = QLineEdit()
            placeholder = label.replace(' *:', '').replace(':', '')
            input_widget.setPlaceholderText(t("placeholder_required", placeholder))
            self.field_inputs[field] = input_widget
            form_layout.addRow(label, input_widget)

        layout.addLayout(form_layout)

        # 按钮
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton(t("btn_save"))
        self.cancel_btn = QPushButton(t("btn_cancel"))

        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                padding: 8px 20px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.save_btn)
        layout.addLayout(button_layout)

        # 信号连接
        self.save_btn.clicked.connect(self.on_save)
        self.cancel_btn.clicked.connect(self.reject)

    def load_data(self):
        """加载现有数据"""
        if self.original_name:
            self.name_input.setText(self.original_name)

        for field, input_widget in self.field_inputs.items():
            value = self.config_data.get(field, "")
            input_widget.setText(value)

    def on_save(self):
        """保存按钮点击"""
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(self, t("dlg_validation_error"), t("err_name_empty"))
            return

        # 收集配置数据
        config = {}
        for field, input_widget in self.field_inputs.items():
            config[field] = input_widget.text().strip()

        # 验证必填字段
        required_fields = ["ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL", "ANTHROPIC_MODEL"]
        for field in required_fields:
            if not config.get(field):
                QMessageBox.warning(self, t("dlg_validation_error"), t("err_field_empty", field))
                return

        self.result_name = name
        self.result_config = config
        self.accept()

    def get_result(self) -> tuple:
        """返回编辑结果 (name, config)"""
        return self.result_name, self.result_config
