"""
Claude API Manager - 入口文件
"""
import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QIcon
from main_window import MainWindow


def get_resource_path(relative_path):
    """获取资源文件路径（支持开发和打包后的环境）"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后的临时目录
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Claude API Manager")
    app.setApplicationVersion("1.0.0")

    # 设置应用图标
    icon_paths = ["app-icon.png", "app-icon.ico"]
    for icon_path in icon_paths:
        full_path = get_resource_path(icon_path)
        if os.path.exists(full_path):
            app.setWindowIcon(QIcon(full_path))
            break

    # 设置应用样式
    app.setStyle('Fusion')

    # 根据平台设置合适的字体
    if sys.platform == "win32":
        font = QFont("Microsoft YaHei", 10)
    elif sys.platform == "darwin":
        font = QFont("PingFang SC", 10)
    else:  # Linux
        font = QFont("Noto Sans CJK SC", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
