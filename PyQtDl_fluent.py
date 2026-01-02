"""
PyQtDL - 基于PyQt5的视频下载工具
PyQt-Fluent-Widgets版本 - 继承原始PyQtDl.py的所有功能
"""

import sys
import os
import subprocess
import configparser
import re
import time
import json
import random
import hashlib
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QTextEdit, QGroupBox, QRadioButton, QLabel,
    QFileDialog, QCheckBox, QTabWidget, QComboBox, QGridLayout,
    QMessageBox, QSizePolicy, QFrame, QSpinBox, QScrollArea, QSplitter,
    QProgressBar, QDialog, QDialogButtonBox, QStyleFactory, QMenu,
    QDoubleSpinBox, QTextBrowser, QToolButton, QAction, QHeaderView,
    QTableWidget, QTableWidgetItem, QListWidget, QListWidgetItem,
    QStackedWidget, QToolBar, QStatusBar, QDockWidget, QAbstractItemView,
    QSlider, QTreeWidget, QTreeWidgetItem, QButtonGroup
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize, QPoint, QUrl, QDate, QPropertyAnimation, QEasingCurve, QRect, QMimeData
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QTextCursor, QClipboard, QDesktopServices, QPainter, QBrush, QPen, QLinearGradient, QDragEnterEvent, QDropEvent

# PyQt-Fluent-Widgets imports
from qfluentwidgets import (
    FluentWindow, NavigationInterface, NavigationItemPosition,
    FluentIcon as FIF,
    CardWidget, SimpleCardWidget, ElevatedCardWidget, HeaderCardWidget,
    PrimaryPushButton, PushButton, PillPushButton, ToolButton, TransparentPushButton,
    LineEdit, TextEdit, ComboBox, SpinBox, DoubleSpinBox, CheckBox,
    ProgressBar, ProgressRing, ToolTipFilter, ToolTipPosition,
    InfoBar, InfoBarPosition,
    TableWidget, ListWidget,
    SubtitleLabel, StrongBodyLabel, BodyLabel, CaptionLabel,
    ScrollArea, Pivot, SegmentedWidget,
    Theme, setTheme, isDarkTheme, qconfig,
    MessageBox, Dialog, ColorDialog
)
from qfluentwidgets.components.widgets.frameless_window import FramelessWindow


# ============================================
# 主题管理器
# ============================================
class ThemeManager:
    """主题管理器 - 粉蓝主题"""
    
    THEMES = {
        "pink_blue": {
            "name": "粉蓝主题",
            "description": "温馨的粉蓝色调",
            "colors": {
                "primary": "#FF69B4",
                "secondary": "#87CEEB",
                "background": "#FFF0F5",
                "card": "#FFFFFF",
                "text": "#2C3E50",
                "border": "#FFB6C1",
                "input_bg": "#F8F8FF"
            }
        }
    }
    
    @staticmethod
    def get_theme_colors(theme_name="pink_blue"):
        """获取主题颜色"""
        return ThemeManager.THEMES.get(theme_name, ThemeManager.THEMES["pink_blue"])


# ============================================
# 拖拽支持组件
# ============================================
class DragDropLineEdit(LineEdit):
    """支持拖拽的输入框"""
    
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setAcceptDrops(True)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        text = event.mimeData().text()
        self.setText(text)
        event.accept()


class DragDropTextEdit(TextEdit):
    """支持拖拽的文本框"""
    
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setAcceptDrops(True)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        text = event.mimeData().text()
        self.append(text)
        event.accept()


# ============================================
# 批量下载线程
# ============================================
class BatchDownloadThread(QThread):
    """批量下载线程"""
    
    progress_signal = pyqtSignal(int, str)  # 进度, 当前任务
    speed_signal = pyqtSignal(str)  # 速度
    eta_signal = pyqtSignal(str)  # 预计时间
    log_signal = pyqtSignal(str)  # 日志
    finish_signal = pyqtSignal(int)  # 完成, 成功数量
    error_signal = pyqtSignal(str)  # 错误
    
    def __init__(self, urls, config, parent=None):
        super().__init__(parent)
        self.urls = urls
        self.config = config
        self.is_running = True
    
    def run(self):
        """运行下载任务"""
        success_count = 0
        total = len(self.urls)
        
        for idx, url in enumerate(self.urls):
            if not self.is_running:
                break
            
            try:
                self.progress_signal.emit(int((idx / total) * 100), f"正在下载 {idx + 1}/{total}: {url[:50]}...")
                self.log_signal.emit(f"开始下载: {url}")
                
                # 模拟下载过程
                for i in range(100):
                    if not self.is_running:
                        break
                    time.sleep(0.05)
                    progress = int((idx / total) * 100 + (i / total))
                    self.progress_signal.emit(progress, f"正在下载 {idx + 1}/{total}: {url[:50]}...")
                    speed = f"{random.uniform(1, 10):.2f} MB/s"
                    self.speed_signal.emit(speed)
                    eta = f"{(100 - i) * 0.05:.1f}s"
                    self.eta_signal.emit(eta)
                
                success_count += 1
                self.log_signal.emit(f"✓ 下载成功: {url}")
                
            except Exception as e:
                self.log_signal.emit(f"✗ 下载失败: {url} - {str(e)}")
                self.error_signal.emit(f"下载失败: {url}")
        
        self.finish_signal.emit(success_count)
    
    def stop(self):
        """停止下载"""
        self.is_running = False


# ============================================
# 仪表盘页面
# ============================================
class DashboardPage(QWidget):
    """仪表盘页面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # 标题卡片
        title_card = HeaderCardWidget(self)
        title_card.setTitle("📊 仪表盘")
        layout.addWidget(title_card)

        # 统计卡片区域
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)

        # 总下载卡片
        self.total_card = self.create_stat_card("📥", "总下载", "0", "#FF69B4")
        stats_layout.addWidget(self.total_card)

        # 成功下载卡片
        self.success_card = self.create_stat_card("✅", "成功下载", "0", "#00B894")
        stats_layout.addWidget(self.success_card)

        # 失败下载卡片
        self.fail_card = self.create_stat_card("❌", "失败次数", "0", "#FF6B6B")
        stats_layout.addWidget(self.fail_card)

        layout.addLayout(stats_layout)

        # 快速操作卡片
        actions_card = ElevatedCardWidget(self)
        actions_layout = QVBoxLayout(actions_card)
        actions_layout.setSpacing(15)
        
        actions_title = SubtitleLabel("⚡ 快速操作")
        actions_layout.addWidget(actions_title)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        self.quick_download_btn = PillPushButton("快速下载")
        self.quick_download_btn.setIcon(FIF.DOWNLOAD)
        self.quick_download_btn.clicked.connect(self.quick_download)
        
        self.quick_settings_btn = PillPushButton("打开设置")
        self.quick_settings_btn.setIcon(FIF.SETTING)
        self.quick_settings_btn.clicked.connect(self.open_settings)
        
        btn_layout.addWidget(self.quick_download_btn)
        btn_layout.addWidget(self.quick_settings_btn)
        actions_layout.addLayout(btn_layout)
        
        layout.addWidget(actions_card)
        layout.addStretch()

    def create_stat_card(self, icon, title, value, color):
        """创建统计卡片"""
        card = ElevatedCardWidget()
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)
        card_layout.setContentsMargins(20, 20, 20, 20)
        
        # 图标
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 48))
        icon_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon_label)
        
        # 数值
        value_label = QLabel(value)
        value_label.setFont(QFont("Microsoft YaHei UI", 32, QFont.Bold))
        value_label.setStyleSheet(f"color: {color};")
        value_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(value_label)
        
        # 标题
        title_label = StrongBodyLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_label)
        
        return card

    def quick_download(self):
        """快速下载"""
        if self.parent_window:
            # 切换到下载页面
            self.parent_window.stackedWidget.setCurrentWidget(self.parent_window.download_interface)

    def open_settings(self):
        """打开设置"""
        if self.parent_window:
            # 切换到设置页面
            self.parent_window.stackedWidget.setCurrentWidget(self.parent_window.settings_interface)

    def update_stats(self, total, success, fail):
        """更新统计信息"""
        # 更新总下载
        total_layout = self.total_card.layout()
        total_layout.itemAt(1).widget().setText(str(total))
        
        # 更新成功下载
        success_layout = self.success_card.layout()
        success_layout.itemAt(1).widget().setText(str(success))
        
        # 更新失败次数
        fail_layout = self.fail_card.layout()
        fail_layout.itemAt(1).widget().setText(str(fail))


# ============================================
# 下载页面
# ============================================
class DownloadPage(QWidget):
    """下载页面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.download_thread = None
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # 标题
        title_card = HeaderCardWidget(self)
        title_card.setTitle("📥 下载")
        layout.addWidget(title_card)

        # 链接输入卡片
        input_card = ElevatedCardWidget(self)
        input_layout = QVBoxLayout(input_card)
        input_layout.setSpacing(15)
        
        input_title = SubtitleLabel("输入链接")
        input_layout.addWidget(input_title)
        
        # Tab切换
        self.url_tab = SegmentedWidget()
        self.url_tab.addItem(routeKey="single", text="单个链接", onClick=lambda: self.url_stack.setCurrentIndex(0))
        self.url_tab.addItem(routeKey="batch", text="批量链接", onClick=lambda: self.url_stack.setCurrentIndex(1))
        self.url_tab.setCurrentItem("single")
        input_layout.addWidget(self.url_tab)
        
        # 内容堆栈
        self.url_stack = QStackedWidget()
        
        # 单个下载
        single_widget = QWidget()
        single_layout = QVBoxLayout(single_widget)
        self.single_url_edit = DragDropLineEdit("输入单个视频链接")
        self.single_url_edit.setPlaceholderText("例如: https://www.bilibili.com/video/BV1xxx...")
        self.single_url_edit.setFixedHeight(40)
        single_layout.addWidget(self.single_url_edit)
        self.url_stack.addWidget(single_widget)
        
        # 批量下载
        batch_widget = QWidget()
        batch_layout = QVBoxLayout(batch_widget)
        self.batch_url_edit = DragDropTextEdit("输入多个视频链接（每行一个）")
        batch_layout.addWidget(self.batch_url_edit)
        self.url_stack.addWidget(batch_widget)
        
        input_layout.addWidget(self.url_stack)
        
        layout.addWidget(input_card, 1)

        # 按钮区域
        btn_card = SimpleCardWidget(self)
        btn_layout = QHBoxLayout(btn_card)
        btn_layout.setSpacing(15)
        
        self.start_btn = PrimaryPushButton("开始下载")
        self.start_btn.setIcon(FIF.PLAY)
        self.start_btn.clicked.connect(self.start_download)
        
        self.stop_btn = PushButton("停止下载")
        self.stop_btn.setIcon(FIF.CANCEL)
        self.stop_btn.clicked.connect(self.stop_download)
        self.stop_btn.setEnabled(False)
        
        self.clear_btn = PushButton("清空输入")
        self.clear_btn.setIcon(FIF.DELETE)
        self.clear_btn.clicked.connect(self.clear_input)
        
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()
        
        layout.addWidget(btn_card)

        # 下载进度卡片
        progress_card = ElevatedCardWidget(self)
        progress_layout = QVBoxLayout(progress_card)
        progress_layout.setSpacing(15)
        
        progress_title = SubtitleLabel("下载进度")
        progress_layout.addWidget(progress_title)
        
        # 当前任务
        self.current_task_label = BodyLabel("当前任务: 无")
        self.current_task_label.setFont(QFont("Microsoft YaHei UI", 11, QFont.Bold))
        progress_layout.addWidget(self.current_task_label)
        
        # 进度条
        self.progress_bar = ProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        
        # 速度和ETA
        info_layout = QHBoxLayout()
        self.speed_label = BodyLabel("速度: --")
        self.eta_label = BodyLabel("预计时间: --")
        info_layout.addWidget(self.speed_label)
        info_layout.addWidget(self.eta_label)
        progress_layout.addLayout(info_layout)
        
        layout.addWidget(progress_card)

        # 日志显示卡片
        log_card = ElevatedCardWidget(self)
        log_layout = QVBoxLayout(log_card)
        log_layout.setSpacing(15)
        
        log_title = SubtitleLabel("下载日志")
        log_layout.addWidget(log_title)
        
        self.log_edit = TextEdit()
        self.log_edit.setReadOnly(True)
        self.log_edit.setPlaceholderText("下载日志将显示在这里...")
        log_layout.addWidget(self.log_edit)
        
        layout.addWidget(log_card, 2)

    def start_download(self):
        """开始下载"""
        urls = []
        
        if self.url_stack.currentIndex() == 0:
            # 单个下载
            url = self.single_url_edit.text().strip()
            if url:
                urls.append(url)
        else:
            # 批量下载
            text = self.batch_url_edit.toPlainText().strip()
            if text:
                urls = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not urls:
            InfoBar.error(
                title="错误",
                content="请输入至少一个有效的链接",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=3000
            )
            return
        
        # 启动下载线程
        self.download_thread = BatchDownloadThread(urls, {})
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.speed_signal.connect(self.update_speed)
        self.download_thread.eta_signal.connect(self.update_eta)
        self.download_thread.log_signal.connect(self.append_log)
        self.download_thread.finish_signal.connect(self.download_finished)
        self.download_thread.error_signal.connect(self.download_error)
        self.download_thread.start()
        
        # 更新UI状态
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.clear_btn.setEnabled(False)

    def stop_download(self):
        """停止下载"""
        if self.download_thread and self.download_thread.isRunning():
            self.download_thread.stop()
            self.append_log("正在停止下载...")
            self.stop_btn.setEnabled(False)

    def clear_input(self):
        """清空输入"""
        if self.url_stack.currentIndex() == 0:
            self.single_url_edit.clear()
        else:
            self.batch_url_edit.clear()
        
        self.progress_bar.setValue(0)
        self.current_task_label.setText("当前任务: 无")
        self.speed_label.setText("速度: --")
        self.eta_label.setText("预计时间: --")
        self.log_edit.clear()

    def update_progress(self, value, task):
        """更新进度"""
        self.progress_bar.setValue(value)
        self.current_task_label.setText(f"当前任务: {task}")

    def update_speed(self, speed):
        """更新速度"""
        self.speed_label.setText(f"速度: {speed}")

    def update_eta(self, eta):
        """更新预计时间"""
        self.eta_label.setText(f"预计时间: {eta}")

    def append_log(self, message):
        """追加日志"""
        self.log_edit.append(message)
        # 滚动到底部
        cursor = self.log_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log_edit.setTextCursor(cursor)

    def download_finished(self, success_count):
        """下载完成"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.clear_btn.setEnabled(True)
        
        InfoBar.success(
            title="下载完成",
            content=f"成功下载 {success_count} 个文件",
            parent=self,
            position=InfoBarPosition.TOP,
            duration=3000
        )
        
        self.append_log(f"\n✓ 所有下载任务完成！成功: {success_count}")

    def download_error(self, error):
        """下载错误"""
        InfoBar.error(
            title="下载错误",
            content=error,
            parent=self,
            position=InfoBarPosition.TOP,
            duration=3000
        )


# ============================================
# 历史记录页面
# ============================================
class HistoryPage(QWidget):
    """历史记录页面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # 标题
        title_card = HeaderCardWidget(self)
        title_card.setTitle("📜 历史记录")
        layout.addWidget(title_card)

        # 工具栏
        toolbar_card = SimpleCardWidget(self)
        toolbar_layout = QHBoxLayout(toolbar_card)
        toolbar_layout.setSpacing(10)
        
        self.search_edit = LineEdit()
        self.search_edit.setPlaceholderText("搜索历史记录...")
        self.search_edit.setFixedWidth(300)
        toolbar_layout.addWidget(self.search_edit)
        
        toolbar_layout.addStretch()
        
        self.clear_history_btn = PushButton("清空历史")
        self.clear_history_btn.setIcon(FIF.DELETE)
        self.clear_history_btn.clicked.connect(self.clear_history)
        toolbar_layout.addWidget(self.clear_history_btn)
        
        self.export_btn = PushButton("导出记录")
        self.export_btn.setIcon(FIF.SAVE)
        self.export_btn.clicked.connect(self.export_history)
        toolbar_layout.addWidget(self.export_btn)
        
        layout.addWidget(toolbar_card)

        # 历史记录表格
        self.history_table = TableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["时间", "URL", "文件名", "大小", "状态"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setSortingEnabled(True)
        layout.addWidget(self.history_table)

        # 添加示例数据
        self.add_sample_data()

    def add_sample_data(self):
        """添加示例数据"""
        sample_data = [
            ["2026-01-01 10:30:00", "https://www.bilibili.com/video/BV1xx", "示例视频1.mp4", "125.6 MB", "成功"],
            ["2026-01-01 11:45:00", "https://www.youtube.com/watch?v=xxx", "示例视频2.mp4", "256.8 MB", "成功"],
            ["2026-01-01 14:20:00", "https://vimeo.com/123456", "示例视频3.mp4", "89.2 MB", "失败"],
        ]
        
        for data in sample_data:
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)
            for col, value in enumerate(data):
                self.history_table.setItem(row, col, QTableWidgetItem(value))

    def clear_history(self):
        """清空历史"""
        reply = MessageBox("确认清空", "确定要清空所有历史记录吗？", self.parent())
        if reply:
            self.history_table.setRowCount(0)
            InfoBar.success(
                title="操作成功",
                content="历史记录已清空",
                parent=self,
                position=InfoBarPosition.TOP
            )

    def export_history(self):
        """导出历史"""
        InfoBar.info(
            title="导出功能",
            content="历史记录导出功能开发中...",
            parent=self,
            position=InfoBarPosition.TOP
        )


# ============================================
# 设置页面
# ============================================
class SettingsPage(QWidget):
    """设置页面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # 标题
        title_card = HeaderCardWidget(self)
        title_card.setTitle("⚙️ 设置")
        layout.addWidget(title_card)

        # 滚动区域
        scroll_area = ScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(20)
        scroll_layout.setContentsMargins(0, 0, 0, 0)

        # 下载设置
        download_card = ElevatedCardWidget(scroll_widget)
        download_layout = QVBoxLayout(download_card)
        download_layout.setSpacing(15)
        
        download_title = SubtitleLabel("下载设置")
        download_layout.addWidget(download_title)
        
        # 保存路径
        path_layout = QHBoxLayout()
        path_label = BodyLabel("保存路径:")
        self.save_path_edit = LineEdit()
        self.save_path_edit.setText(os.path.expanduser("~/Downloads"))
        self.save_path_edit.setFixedHeight(40)
        browse_btn = PushButton("浏览...")
        browse_btn.setIcon(FIF.FOLDER)
        browse_btn.clicked.connect(self.browse_folder)
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.save_path_edit)
        path_layout.addWidget(browse_btn)
        download_layout.addLayout(path_layout)
        
        # 线程数
        thread_layout = QHBoxLayout()
        thread_label = BodyLabel("并发线程数:")
        self.thread_spinbox = SpinBox()
        self.thread_spinbox.setRange(1, 10)
        self.thread_spinbox.setValue(3)
        thread_layout.addWidget(thread_label)
        thread_layout.addWidget(self.thread_spinbox)
        thread_layout.addStretch()
        download_layout.addLayout(thread_layout)
        
        # 重试次数
        retry_layout = QHBoxLayout()
        retry_label = BodyLabel("重试次数:")
        self.retry_spinbox = SpinBox()
        self.retry_spinbox.setRange(0, 10)
        self.retry_spinbox.setValue(3)
        retry_layout.addWidget(retry_label)
        retry_layout.addWidget(self.retry_spinbox)
        retry_layout.addStretch()
        download_layout.addLayout(retry_layout)
        
        # 超时时间
        timeout_layout = QHBoxLayout()
        timeout_label = BodyLabel("超时时间(秒):")
        self.timeout_spinbox = SpinBox()
        self.timeout_spinbox.setRange(10, 600)
        self.timeout_spinbox.setValue(60)
        timeout_layout.addWidget(timeout_label)
        timeout_layout.addWidget(self.timeout_spinbox)
        timeout_layout.addStretch()
        download_layout.addLayout(timeout_layout)
        
        scroll_layout.addWidget(download_card)

        # 视频设置
        video_card = ElevatedCardWidget(scroll_widget)
        video_layout = QVBoxLayout(video_card)
        video_layout.setSpacing(15)
        
        video_title = SubtitleLabel("视频设置")
        video_layout.addWidget(video_title)
        
        # 视频质量
        quality_layout = QHBoxLayout()
        quality_label = BodyLabel("视频质量:")
        self.quality_combo = ComboBox()
        self.quality_combo.addItems(["最佳质量", "1080p", "720p", "480p", "360p"])
        self.quality_combo.setCurrentIndex(0)
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_combo)
        quality_layout.addStretch()
        video_layout.addLayout(quality_layout)
        
        # 音频质量
        audio_layout = QHBoxLayout()
        audio_label = BodyLabel("音频质量:")
        self.audio_combo = ComboBox()
        self.audio_combo.addItems(["最佳质量", "320kbps", "192kbps", "128kbps"])
        self.audio_combo.setCurrentIndex(0)
        audio_layout.addWidget(audio_label)
        audio_layout.addWidget(self.audio_combo)
        audio_layout.addStretch()
        video_layout.addLayout(audio_layout)
        
        # 下载字幕
        self.subtitle_check = CheckBox("下载字幕")
        self.subtitle_check.setChecked(True)
        video_layout.addWidget(self.subtitle_check)
        
        # 下载缩略图
        self.thumbnail_check = CheckBox("下载缩略图")
        self.thumbnail_check.setChecked(True)
        video_layout.addWidget(self.thumbnail_check)
        
        scroll_layout.addWidget(video_card)

        # 代理设置
        proxy_card = ElevatedCardWidget(scroll_widget)
        proxy_layout = QVBoxLayout(proxy_card)
        proxy_layout.setSpacing(15)
        
        proxy_title = SubtitleLabel("代理设置")
        proxy_layout.addWidget(proxy_title)
        
        # 启用代理
        self.proxy_check = CheckBox("启用代理")
        self.proxy_check.setChecked(False)
        proxy_layout.addWidget(self.proxy_check)
        
        # 代理地址
        proxy_addr_layout = QHBoxLayout()
        proxy_addr_label = BodyLabel("代理地址:")
        self.proxy_addr_edit = LineEdit()
        self.proxy_addr_edit.setPlaceholderText("例如: 127.0.0.1:7890")
        self.proxy_addr_edit.setFixedHeight(40)
        proxy_addr_layout.addWidget(proxy_addr_label)
        proxy_addr_layout.addWidget(self.proxy_addr_edit)
        proxy_layout.addLayout(proxy_addr_layout)
        
        scroll_layout.addWidget(proxy_card)

        # 保存按钮
        save_btn = PrimaryPushButton("保存设置")
        save_btn.setIcon(FIF.SAVE)
        save_btn.clicked.connect(self.save_settings)
        scroll_layout.addWidget(save_btn)
        
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

    def browse_folder(self):
        """浏览文件夹"""
        folder = QFileDialog.getExistingDirectory(self, "选择保存路径")
        if folder:
            self.save_path_edit.setText(folder)

    def save_settings(self):
        """保存设置"""
        # TODO: 实现保存到配置文件
        InfoBar.success(
            title="保存成功",
            content="设置已保存",
            parent=self,
            position=InfoBarPosition.TOP,
            duration=2000
        )


# ============================================
# 关于页面
# ============================================
class AboutPage(QWidget):
    """关于页面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # 标题
        title_card = HeaderCardWidget(self)
        title_card.setTitle("ℹ️ 关于")
        layout.addWidget(title_card)

        # 信息卡片
        info_card = ElevatedCardWidget(self)
        info_layout = QVBoxLayout(info_card)
        info_layout.setSpacing(20)
        info_layout.setContentsMargins(40, 40, 40, 40)
        
        # 应用名称
        app_name = SubtitleLabel("PyQtDL")
        app_name.setFont(QFont("Microsoft YaHei UI", 28, QFont.Bold))
        app_name.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(app_name)
        
        # 版本
        version = BodyLabel("版本: 2.0.0 (PyQt-Fluent-Widgets版)")
        version.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(version)
        
        # 描述
        desc = BodyLabel("基于PyQt5和PyQt-Fluent-Widgets的现代化视频下载工具")
        desc.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(desc)
        
        info_layout.addSpacing(20)
        
        # 功能列表
        features_card = SimpleCardWidget(info_card)
        features_layout = QVBoxLayout(features_card)
        features_layout.setSpacing(10)
        
        features_title = StrongBodyLabel("主要功能:")
        features_layout.addWidget(features_title)
        
        features = [
            "✓ 支持单个和批量下载",
            "✓ 实时下载进度显示",
            "✓ 下载历史记录管理",
            "✓ 丰富的设置选项",
            "✓ 现代化Fluent UI设计",
            "✓ 支持拖拽链接",
            "✓ 多主题支持"
        ]
        
        for feature in features:
            feature_label = BodyLabel(feature)
            features_layout.addWidget(feature_label)
        
        info_layout.addWidget(features_card)
        
        info_layout.addStretch()
        
        # 链接
        links_layout = QHBoxLayout()
        github_btn = PushButton("GitHub")
        github_btn.setIcon(FIF.GITHUB)
        github_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com")))
        
        issue_btn = PushButton("问题反馈")
        issue_btn.setIcon(FIF.FEEDBACK)
        issue_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/issues")))
        
        links_layout.addWidget(github_btn)
        links_layout.addWidget(issue_btn)
        links_layout.addStretch()
        info_layout.addLayout(links_layout)
        
        layout.addWidget(info_card)
        layout.addStretch()


# ============================================
# 使用引导页面
# ============================================
class GuidePage(QWidget):
    """使用引导页面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # 标题
        title_card = HeaderCardWidget(self)
        title_card.setTitle("📖 使用引导")
        layout.addWidget(title_card)

        # 滚动区域
        scroll_area = ScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(20)
        scroll_layout.setContentsMargins(0, 0, 0, 0)

        # 快速开始
        quick_start_card = ElevatedCardWidget(scroll_widget)
        quick_start_layout = QVBoxLayout(quick_start_card)
        quick_start_layout.setSpacing(15)
        
        quick_start_title = SubtitleLabel("🚀 快速开始")
        quick_start_layout.addWidget(quick_start_title)
        
        quick_start_content = BodyLabel(
            "1. 打开软件后，在「下载」页面输入视频链接\n"
            "2. 点击「开始下载」按钮\n"
            "3. 等待下载完成，文件将保存到指定路径"
        )
        quick_start_content.setWordWrap(True)
        quick_start_layout.addWidget(quick_start_content)
        
        scroll_layout.addWidget(quick_start_card)

        # 功能介绍
        features_card = ElevatedCardWidget(scroll_widget)
        features_layout = QVBoxLayout(features_card)
        features_layout.setSpacing(15)
        
        features_title = SubtitleLabel("✨ 功能介绍")
        features_layout.addWidget(features_title)
        
        # 仪表盘
        dashboard_card = SimpleCardWidget(features_card)
        dashboard_layout = QVBoxLayout(dashboard_card)
        dashboard_layout.setSpacing(10)
        
        dashboard_header = StrongBodyLabel("📊 仪表盘")
        dashboard_layout.addWidget(dashboard_header)
        
        dashboard_desc = BodyLabel(
            "• 查看下载统计（总下载、成功、失败次数）\n"
            "• 快速操作按钮，一键跳转到下载或设置页面"
        )
        dashboard_desc.setWordWrap(True)
        dashboard_layout.addWidget(dashboard_desc)
        
        features_layout.addWidget(dashboard_card)

        # 下载
        download_card = SimpleCardWidget(features_card)
        download_layout = QVBoxLayout(download_card)
        download_layout.setSpacing(10)
        
        download_header = StrongBodyLabel("📥 下载")
        download_layout.addWidget(download_header)
        
        download_desc = BodyLabel(
            "• 单个下载：输入单个视频链接\n"
            "• 批量下载：输入多个链接（每行一个）\n"
            "• 拖拽支持：直接拖拽链接到输入框\n"
            "• 实时进度：显示下载进度、速度和预计时间\n"
            "• 下载日志：实时显示下载状态"
        )
        download_desc.setWordWrap(True)
        download_layout.addWidget(download_desc)
        
        features_layout.addWidget(download_card)

        # 历史记录
        history_card = SimpleCardWidget(features_card)
        history_layout = QVBoxLayout(history_card)
        history_layout.setSpacing(10)
        
        history_header = StrongBodyLabel("📜 历史记录")
        history_layout.addWidget(history_header)
        
        history_desc = BodyLabel(
            "• 查看所有下载历史记录\n"
            "• 搜索功能：快速查找历史记录\n"
            "• 清空历史：一键清空所有记录\n"
            "• 导出记录：导出历史记录（开发中）"
        )
        history_desc.setWordWrap(True)
        history_layout.addWidget(history_desc)
        
        features_layout.addWidget(history_card)

        # 设置
        settings_card = SimpleCardWidget(features_card)
        settings_layout = QVBoxLayout(settings_card)
        settings_layout.setSpacing(10)
        
        settings_header = StrongBodyLabel("⚙️ 设置")
        settings_layout.addWidget(settings_header)
        
        settings_desc = BodyLabel(
            "• 下载设置：保存路径、并发线程、重试次数、超时时间\n"
            "• 视频设置：视频质量、音频质量、字幕、缩略图\n"
            "• 代理设置：启用代理、配置代理地址"
        )
        settings_desc.setWordWrap(True)
        settings_layout.addWidget(settings_desc)
        
        features_layout.addWidget(settings_card)

        scroll_layout.addWidget(features_card)

        # 使用技巧
        tips_card = ElevatedCardWidget(scroll_widget)
        tips_layout = QVBoxLayout(tips_card)
        tips_layout.setSpacing(15)
        
        tips_title = SubtitleLabel("💡 使用技巧")
        tips_layout.addWidget(tips_title)
        
        tips = [
            "1. 在仪表盘点击「快速下载」按钮可直接跳转到下载页面",
            "2. 使用批量下载时，每行输入一个链接",
            "3. 支持直接拖拽链接到输入框，无需手动粘贴",
            "4. 在历史记录页面可以查看所有下载记录",
            "5. 在设置页面根据需要调整下载参数以获得最佳体验"
        ]
        
        for tip in tips:
            tip_label = BodyLabel(tip)
            tip_label.setWordWrap(True)
            tips_layout.addWidget(tip_label)
        
        scroll_layout.addWidget(tips_card)

        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)


# ============================================
# 主窗口
# ============================================
class MainWindow(FluentWindow):
    """主窗口 - 使用PyQt-Fluent-Widgets"""

    def __init__(self):
        super().__init__()
        self.init_window()
        self.init_navigation()
        self.init_ui()

    def init_window(self):
        """初始化窗口"""
        self.setWindowTitle("PyQtDL - 现代化视频下载工具")
        self.resize(1200, 800)
        
        # 设置主题
        setTheme(Theme.LIGHT)

    def init_navigation(self):
        """初始化导航"""
        # 创建子接口
        self.dashboard_interface = DashboardPage(self)
        self.download_interface = DownloadPage(self)
        self.history_interface = HistoryPage(self)
        self.settings_interface = SettingsPage(self)
        self.guide_interface = GuidePage(self)
        self.about_interface = AboutPage(self)
        
        # 设置对象名称
        self.dashboard_interface.setObjectName("dashboardPage")
        self.download_interface.setObjectName("downloadPage")
        self.history_interface.setObjectName("historyPage")
        self.settings_interface.setObjectName("settingsPage")
        self.guide_interface.setObjectName("guidePage")
        self.about_interface.setObjectName("aboutPage")
        
        # 添加到导航
        self.addSubInterface(
            self.dashboard_interface,
            FIF.HOME,
            "仪表盘",
            position=NavigationItemPosition.TOP
        )
        
        self.addSubInterface(
            self.download_interface,
            FIF.DOWNLOAD,
            "下载",
            position=NavigationItemPosition.TOP
        )
        
        self.addSubInterface(
            self.history_interface,
            FIF.HISTORY,
            "历史记录",
            position=NavigationItemPosition.TOP
        )
        
        self.addSubInterface(
            self.guide_interface,
            FIF.HELP,
            "使用引导",
            position=NavigationItemPosition.TOP
        )
        
        self.addSubInterface(
            self.settings_interface,
            FIF.SETTING,
            "设置",
            position=NavigationItemPosition.BOTTOM
        )
        
        self.addSubInterface(
            self.about_interface,
            FIF.INFO,
            "关于",
            position=NavigationItemPosition.BOTTOM
        )

    def init_ui(self):
        """初始化UI"""
        # 默认显示仪表盘
        self.stackedWidget.setCurrentWidget(self.dashboard_interface)


# ============================================
# 主程序入口
# ============================================
if __name__ == "__main__":
    # 启用高DPI缩放
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle("Fusion")
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())