"""
Claude API Manager - 主窗口
"""
import sys
import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QLabel,
    QMessageBox, QInputDialog, QAbstractItemView, QApplication,
    QMenuBar, QMenu
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon

from config_manager import ConfigManager, JSONFormatError
from edit_dialog import EditDialog
from translations import t, set_language, get_language


class ConfigItemWidget(QWidget):
    """自定义配置项控件"""

    def __init__(self, name: str, is_active: bool = False, parent=None):
        super().__init__(parent)
        self.name = name
        self.is_active = is_active
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        # 状态标签
        self.status_label = QLabel("●" if self.is_active else "○")
        self.status_label.setStyleSheet(
            f"color: {'#4CAF50' if self.is_active else '#999'}; font-size: 14px;"
        )
        layout.addWidget(self.status_label)

        # 名称标签
        self.name_label = QLabel(self.name)
        font = QFont()
        font.setPointSize(11)
        if self.is_active:
            font.setBold(True)
        self.name_label.setFont(font)
        self.name_label.setStyleSheet(
            f"color: {'#333' if self.is_active else '#666'};"
        )
        layout.addWidget(self.name_label, stretch=1)

        # 状态文字
        if self.is_active:
            active_label = QLabel(t("status_active"))
            active_label.setStyleSheet("color: #4CAF50; font-size: 11px;")
            layout.addWidget(active_label)

        self.setStyleSheet("""
            ConfigItemWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
            }
            ConfigItemWidget:hover {
                background-color: #f5f5f5;
                border-color: #4CAF50;
            }
        """)


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Claude API Manager")
        self.setMinimumSize(700, 500)

        # 设置窗口图标（在初始化 config_manager 之前）
        self._set_window_icon_only()

        self.config_manager = ConfigManager()
        self.config_manager.ensure_files_exist()

        # 创建菜单栏
        self.create_menu_bar()

        # 检查 JSON 文件格式
        is_valid, error_files = self.check_json_files()
        if not is_valid:
            self.setup_ui_error_state(error_files)
            return

        self.setup_ui()
        self.refresh_config_list()

    def _set_window_icon_only(self):
        """仅设置窗口图标"""
        icon_paths = [
            "app-icon.png",
            "app-icon.ico",
            "../app-icon.png",
            "../app-icon.ico",
        ]

        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
                break

    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 语言菜单
        lang_menu = menubar.addMenu(t("menu_language"))

        # 中文选项
        zh_action = lang_menu.addAction(t("lang_zh"))
        zh_action.triggered.connect(lambda: self.change_language("zh"))
        if get_language() == "zh":
            zh_action.setCheckable(True)
            zh_action.setChecked(True)

        # 英文选项
        en_action = lang_menu.addAction(t("lang_en"))
        en_action.triggered.connect(lambda: self.change_language("en"))
        if get_language() == "en":
            en_action.setCheckable(True)
            en_action.setChecked(True)

    def change_language(self, language: str):
        """切换语言"""
        if get_language() == language:
            return

        set_language(language)

        # 重新创建界面
        # 清除中央部件
        old_central = self.centralWidget()
        if old_central:
            old_central.deleteLater()

        # 重新设置窗口标题
        self.setWindowTitle(t("window_title"))

        # 重新创建菜单栏
        self.menuBar().clear()
        self.create_menu_bar()

        # 重新加载界面
        if hasattr(self, 'config_manager'):
            is_valid, error_files = self.check_json_files()
            if not is_valid:
                self.setup_ui_error_state(error_files)
            else:
                self.setup_ui()
                self.refresh_config_list()

    def check_json_files(self) -> tuple:
        """
        检查 JSON 文件格式
        返回: (是否有效, 错误文件列表)
        """
        is_valid, error_msg = self.config_manager.validate_json_files()
        if not is_valid:
            # 解析错误信息，提取文件名
            error_files = []
            for line in error_msg.split('\n'):
                if '(' in line and ')' in line:
                    filename = line.split('(')[1].split(')')[0]
                    error_files.append(filename)
            return False, error_files
        return True, []

    def setup_ui(self):
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title_label = QLabel(t("main_title"))
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #333; margin-bottom: 10px;")
        main_layout.addWidget(title_label)

        # 说明文字
        desc_label = QLabel(t("main_desc"))
        desc_label.setStyleSheet("color: #666; margin-bottom: 10px;")
        main_layout.addWidget(desc_label)

        # 配置列表
        self.config_list = QListWidget()
        self.config_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.config_list.setSpacing(8)
        self.config_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #fafafa;
                padding: 10px;
            }
            QListWidget::item {
                border: none;
                background: transparent;
            }
            QListWidget::item:selected {
                background: transparent;
            }
        """)
        main_layout.addWidget(self.config_list)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # 左侧按钮
        left_layout = QHBoxLayout()
        self.add_btn = QPushButton(t("btn_add"))
        self.reset_btn = QPushButton(t("btn_reset"))
        self.add_btn.setStyleSheet(self._get_primary_button_style())
        self.reset_btn.setStyleSheet(self._get_warning_button_style())
        left_layout.addWidget(self.add_btn)
        left_layout.addWidget(self.reset_btn)
        left_layout.addStretch()

        # 右侧按钮
        right_layout = QHBoxLayout()
        self.activate_btn = QPushButton(t("btn_activate"))
        self.edit_btn = QPushButton(t("btn_edit"))
        self.copy_btn = QPushButton(t("btn_copy"))
        self.rename_btn = QPushButton(t("btn_rename"))
        self.delete_btn = QPushButton(t("btn_delete"))

        self.activate_btn.setStyleSheet(self._get_success_button_style())
        self.edit_btn.setStyleSheet(self._get_default_button_style())
        self.copy_btn.setStyleSheet(self._get_default_button_style())
        self.rename_btn.setStyleSheet(self._get_default_button_style())
        self.delete_btn.setStyleSheet(self._get_danger_button_style())

        right_layout.addWidget(self.activate_btn)
        right_layout.addWidget(self.edit_btn)
        right_layout.addWidget(self.copy_btn)
        right_layout.addWidget(self.rename_btn)
        right_layout.addWidget(self.delete_btn)

        button_layout.addLayout(left_layout)
        button_layout.addStretch()
        button_layout.addLayout(right_layout)

        main_layout.addLayout(button_layout)

        # 信号连接
        self.add_btn.clicked.connect(self.on_add)
        self.reset_btn.clicked.connect(self.on_reset)
        self.activate_btn.clicked.connect(self.on_activate)
        self.edit_btn.clicked.connect(self.on_edit)
        self.copy_btn.clicked.connect(self.on_copy)
        self.rename_btn.clicked.connect(self.on_rename)
        self.delete_btn.clicked.connect(self.on_delete)

        self.config_list.itemClicked.connect(self.on_item_selected)

        # 更新按钮状态
        self.update_button_states()

    def setup_ui_error_state(self, error_files: list):
        """JSON 错误状态下的 UI - 显示空列表，禁用所有按钮"""
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title_label = QLabel(t("main_title"))
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #333; margin-bottom: 10px;")
        main_layout.addWidget(title_label)

        # 说明文字
        desc_label = QLabel(t("main_desc"))
        desc_label.setStyleSheet("color: #666; margin-bottom: 10px;")
        main_layout.addWidget(desc_label)

        # 配置列表 - 显示空状态
        self.config_list = QListWidget()
        self.config_list.setSelectionMode(QAbstractItemView.NoSelection)
        self.config_list.setSpacing(8)
        self.config_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #fafafa;
                padding: 10px;
            }
            QListWidget::item {
                border: none;
                background: transparent;
            }
        """)

        # 添加空状态提示
        empty_item = QListWidgetItem(t("empty_list_error"))
        empty_item.setFlags(Qt.NoItemFlags)
        empty_item.setTextAlignment(Qt.AlignCenter)
        empty_item.setForeground(Qt.red)
        self.config_list.addItem(empty_item)
        main_layout.addWidget(self.config_list)

        # 创建按钮但禁用
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # 左侧按钮
        left_layout = QHBoxLayout()
        self.add_btn = QPushButton(t("btn_add"))
        self.reset_btn = QPushButton(t("btn_reset"))
        self.add_btn.setEnabled(False)
        self.reset_btn.setEnabled(False)
        self.add_btn.setStyleSheet(self._get_disabled_button_style())
        self.reset_btn.setStyleSheet(self._get_disabled_button_style())
        left_layout.addWidget(self.add_btn)
        left_layout.addWidget(self.reset_btn)
        left_layout.addStretch()

        # 右侧按钮
        right_layout = QHBoxLayout()
        self.activate_btn = QPushButton(t("btn_activate"))
        self.edit_btn = QPushButton(t("btn_edit"))
        self.copy_btn = QPushButton(t("btn_copy"))
        self.rename_btn = QPushButton(t("btn_rename"))
        self.delete_btn = QPushButton(t("btn_delete"))

        for btn in [self.activate_btn, self.edit_btn, self.copy_btn, self.rename_btn, self.delete_btn]:
            btn.setEnabled(False)
            btn.setStyleSheet(self._get_disabled_button_style())

        right_layout.addWidget(self.activate_btn)
        right_layout.addWidget(self.edit_btn)
        right_layout.addWidget(self.copy_btn)
        right_layout.addWidget(self.rename_btn)
        right_layout.addWidget(self.delete_btn)

        button_layout.addLayout(left_layout)
        button_layout.addStretch()
        button_layout.addLayout(right_layout)

        main_layout.addLayout(button_layout)

        # 显示错误弹窗
        self.show_json_error_dialog(error_files)

    def _get_disabled_button_style(self) -> str:
        """禁用状态的按钮样式"""
        return """
            QPushButton {
                background-color: #e0e0e0;
                color: #999;
                padding: 8px 16px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        """

    def show_json_error_dialog(self, error_files: list):
        """显示 JSON 错误弹窗"""
        files_text = "\n".join([f"  • {f}" for f in error_files])

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(t("dlg_json_error"))
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(t("msg_json_error", files_text))
        msg_box.setStandardButtons(QMessageBox.Close)

        # 设置样式
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: #333;
                font-size: 12px;
            }
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px 24px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)

        msg_box.exec()

    def _get_primary_button_style(self) -> str:
        return """
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """

    def _get_success_button_style(self) -> str:
        return """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #2E7D32;
            }
            QPushButton:disabled {
                background-color: #c8e6c9;
                color: #666;
            }
        """

    def _get_default_button_style(self) -> str:
        return """
            QPushButton {
                background-color: #f0f0f0;
                color: #333;
                padding: 8px 16px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
            QPushButton:disabled {
                background-color: #f5f5f5;
                color: #999;
            }
        """

    def _get_danger_button_style(self) -> str:
        return """
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #b71c1c;
            }
            QPushButton:disabled {
                background-color: #ffcdd2;
                color: #666;
            }
        """

    def _get_warning_button_style(self) -> str:
        return """
            QPushButton {
                background-color: #FF9800;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:pressed {
                background-color: #E65100;
            }
            QPushButton:disabled {
                background-color: #FFE0B2;
                color: #666;
            }
        """

    def refresh_config_list(self):
        """刷新配置列表"""
        self.config_list.clear()

        configs = self.config_manager.get_all_configs()
        active_name = self.config_manager.get_active_config_name()

        if not configs:
            # 显示空状态
            empty_item = QListWidgetItem(t("empty_list"))
            empty_item.setFlags(Qt.NoItemFlags)
            empty_item.setTextAlignment(Qt.AlignCenter)
            empty_item.setForeground(Qt.gray)
            self.config_list.addItem(empty_item)
            return

        for name in sorted(configs.keys()):
            is_active = (name == active_name)

            # 创建列表项
            item = QListWidgetItem()
            item.setData(Qt.UserRole, name)
            item.setSizeHint(QSize(0, 50))

            # 创建自定义控件
            widget = ConfigItemWidget(name, is_active)

            self.config_list.addItem(item)
            self.config_list.setItemWidget(item, widget)

    def get_selected_config_name(self) -> str:
        """获取选中的配置名称"""
        item = self.config_list.currentItem()
        if item:
            return item.data(Qt.UserRole) or ""
        return ""

    def on_item_selected(self):
        """列表项选中事件"""
        self.update_button_states()

    def update_button_states(self):
        """更新按钮状态"""
        has_selection = bool(self.get_selected_config_name())
        self.activate_btn.setEnabled(has_selection)
        self.edit_btn.setEnabled(has_selection)
        self.copy_btn.setEnabled(has_selection)
        self.rename_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)

    def on_add(self):
        """添加配置"""
        dialog = EditDialog(self)
        if dialog.exec() == EditDialog.Accepted:
            name, config = dialog.get_result()

            # 检查名称是否已存在
            all_configs = self.config_manager.get_all_configs()
            if name in all_configs:
                QMessageBox.warning(self, t("dlg_validation_error"), t("msg_config_exists", name))
                return

            self.config_manager.save_config(name, config)
            self.refresh_config_list()

            # 选中新添加的配置
            self.select_config_by_name(name)

    def on_edit(self):
        """编辑配置"""
        name = self.get_selected_config_name()
        if not name:
            return

        all_configs = self.config_manager.get_all_configs()
        if name not in all_configs:
            return

        dialog = EditDialog(self, name, all_configs[name])
        if dialog.exec() == EditDialog.Accepted:
            new_name, config = dialog.get_result()

            # 如果名称改变了，检查是否冲突
            if new_name != name and new_name in all_configs:
                QMessageBox.warning(self, t("dlg_validation_error"), t("msg_config_exists", new_name))
                return

            # 如果名称改变了，先删除旧的
            if new_name != name:
                self.config_manager.delete_config(name)

            self.config_manager.save_config(new_name, config)
            self.refresh_config_list()
            self.select_config_by_name(new_name)

    def on_copy(self):
        """复制配置"""
        name = self.get_selected_config_name()
        if not name:
            return

        try:
            new_name = self.config_manager.duplicate_config(name)
            self.refresh_config_list()
            self.select_config_by_name(new_name)
        except ValueError as e:
            QMessageBox.warning(self, t("dlg_validation_error"), str(e))

    def on_rename(self):
        """重命名配置"""
        name = self.get_selected_config_name()
        if not name:
            return

        new_name, ok = QInputDialog.getText(
            self, t("dlg_rename"), t("lbl_new_name"),
            text=name
        )

        if ok and new_name and new_name != name:
            all_configs = self.config_manager.get_all_configs()
            if new_name in all_configs:
                QMessageBox.warning(self, t("dlg_validation_error"), t("msg_config_exists", new_name))
                return

            self.config_manager.rename_config(name, new_name)
            self.refresh_config_list()
            self.select_config_by_name(new_name)

    def on_delete(self):
        """删除配置"""
        name = self.get_selected_config_name()
        if not name:
            return

        reply = QMessageBox.question(
            self, t("dlg_confirm_delete"),
            t("msg_confirm_delete", name),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.config_manager.delete_config(name)
            self.refresh_config_list()
            self.update_button_states()

    def on_activate(self):
        """启动配置"""
        name = self.get_selected_config_name()
        if not name:
            return

        try:
            self.config_manager.activate_config(name)
            self.refresh_config_list()
        except ValueError as e:
            QMessageBox.warning(self, t("dlg_validation_error"), str(e))

    def on_reset(self):
        """恢复默认 - 清除启动状态"""
        reply = QMessageBox.question(
            self, t("dlg_confirm_reset"),
            t("msg_confirm_reset"),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.config_manager.deactivate_current_config()
            self.refresh_config_list()

    def select_config_by_name(self, name: str):
        """根据名称选中配置"""
        for i in range(self.config_list.count()):
            item = self.config_list.item(i)
            if item.data(Qt.UserRole) == name:
                self.config_list.setCurrentItem(item)
                self.update_button_states()
                break


def main():
    app = QApplication(sys.argv)

    # 设置应用样式
    app.setStyle('Fusion')

    # 设置全局字体
    font = QFont("Microsoft YaHei" if sys.platform == "win32" else "Noto Sans CJK SC", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
