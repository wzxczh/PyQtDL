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
    QTableWidget, QTableWidgetItem, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize, QPoint, QUrl, QDate
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QTextCursor, QClipboard, QDesktopServices


# ============================================
# 彩蛋系统 - Easter Eggs 🥚
# ============================================
class EasterEggs:
    """有趣的小彩蛋系统，不影响主要功能"""

    @staticmethod
    def get_funny_progress_message(progress):
        """获取有趣的进度消息"""
        messages = [
            "正在召唤下载精灵... ✨",
            "编织下载魔法中... 🧙",
            "给视频穿上小马甲... 👕",
            "和服务器玩捉迷藏... 🕵️",
            "给视频做马杀鸡... 💆",
            "在数字海洋中捕鱼... 🎣",
            "给比特们排队... 👮",
            "施展视频召唤术... 🔮",
            "正在贿赂服务器... 💸",
            "给数据做瑜伽... 🧘"
        ]
        return random.choice(messages) if progress < 100 else "任务完成！🎉"

    @staticmethod
    def get_secret_logo():
        """根据日期获取特殊logo"""
        today = QDate.currentDate()

        # 特殊节日彩蛋
        if today.month() == 10 and today.day() == 31:
            return "🎃 万圣节特别版"
        elif today.month() == 12 and today.day() == 25:
            return "🎄 圣诞特别版"
        elif today.month() == 2 and today.day() == 14:
            return "💝 情人节特别版"
        elif today.month() == 4 and today.day() == 1:
            return "🎭 愚人节特别版"
        elif today.month() == 1 and today.day() == 1:
            return "🎊 新年特别版"

        # 彩蛋：根据星期几改变图标
        weekday = today.dayOfWeek()
        week_icons = ["☕", "📚", "🐪", "🎸", "🎯", "🎮", "🛌"]
        return f"{week_icons[weekday - 1]} PyQtDL"

    @staticmethod
    def secret_key_sequence():
        """秘密按键序列检测"""
        sequence = []
        secret_codes = {
            "上上下下左右左右BA": "🎮 科乐美秘籍激活！",
            "1337": "💻 你是精英！",
            "007": "🕶️ 欢迎，邦德先生",
            "404": "🔍 页面未找到（开玩笑的）",
            "80085": "📞 老式彩蛋",
            "5318008": "📟 经典计算器彩蛋",
            "zzh":"你个贱人"
        }

        def check_sequence():
            if len(sequence) >= 10:
                seq_str = "".join(sequence[-10:])
                for code, message in secret_codes.items():
                    if code in seq_str:
                        return message
            return None

        return sequence, check_sequence

    @staticmethod
    def get_funny_error_message():
        """获取有趣的错误消息"""
        return random.choice([
            "哎呀，服务器打了个喷嚏 🤧",
            "网络信号被猫吃掉了 🐱",
            "数据在传送中迷路了 🗺️",
            "服务器在喝咖啡休息中 ☕",
            "比特们需要一点鼓励 💪",
            "网络管道有点堵 🚰",
            "数据包去度假了 🏖️",
            "服务器在思考人生 🤔",
            "连接被外星人劫持了 👽",
            "网络在玩躲猫猫 🙈"
        ])

    @staticmethod
    def hidden_feature_enabled():
        """根据特定条件启用隐藏功能"""
        today = QDate.currentDate()
        return today.day() == 20  # 软件诞生的日子


# ============================================
# 智能重命名系统
# ============================================
class SmartRenamer:
    """智能重命名器 - 自动识别并生成有意义的文件名"""

    def __init__(self, config):
        self.config = config
        self.meaningful_patterns = [
            r'[\u4e00-\u9fff]+',  # 包含中文字符
            r'[A-Za-z]{3,}.*[A-Za-z]{3,}',  # 包含有意义的英文单词
            r'.*[\.\!\?。！？].*',  # 包含标点符号
            r'第[一二三四五六七八九十\d]+[集章节]',  # 包含章节信息
            r'.*[\(（].*[\)）].*',  # 包含括号内容
            r'^[\u4e00-\u9fff].*[\u4e00-\u9fff]$',  # 以中文开头和结尾
        ]

        self.useless_patterns = [
            r'^[0-9a-f]{16,}$',  # 纯哈希值
            r'^[0-9]{10,}$',  # 纯数字ID
            r'^[a-z0-9]{32,}$',  # MD5类型
            r'^[A-Z0-9]{10,}$',  # 大写的ID
            r'^vid_[0-9]+$',  # vid_12345类型
            r'^video_[0-9]+$',  # video_12345类型
            r'^[0-9]+_[0-9]+$',  # 123_456类型
            r'^[0-9]+[xp][0-9]+$',  # 分辨率格式（1920x1080）
            r'^[a-z0-9]{8}-[a-z0-9]{4}-',  # UUID格式
            r'^temp_',  # 临时文件
            r'^tmp_',  # 临时文件
            r'^untitled',  # 未命名
        ]

        # 常见无用词（中英文）
        self.stop_words = {
            '的', '了', '和', '与', '及', '或', '在', '是', '有', '就', '都', '而', '且', '但', '啊', '吧', '呢', '吗',
            'the', 'and', 'or', 'in', 'on', 'at', 'for', 'with', 'by', 'a', 'an', 'to', 'of', 'as'
        }

        # 平台特定关键词映射
        self.platform_keywords = {
            'bilibili': ['B站', '哔哩哔哩', 'bilibili', 'BILIBILI'],
            'youtube': ['油管', 'YouTube', 'YOUTUBE'],
            'douyin': ['抖音', 'DOUYIN'],
            'tiktok': ['TikTok', '抖音国际版'],
            'twitter': ['推特', 'Twitter'],
            'instagram': ['INS', 'Instagram']
        }

    def is_meaningful_filename(self, filename):
        """判断文件名是否有意义"""
        if not filename:
            return False

        # 移除扩展名
        name_without_ext = os.path.splitext(filename)[0]

        # 检查最小长度
        min_length = int(self.config["Rename"]["min_meaningful_length"])
        if len(name_without_ext) < min_length:
            return False

        # 检查是否是无意义的模式
        for pattern in self.useless_patterns:
            if re.match(pattern, name_without_ext, re.IGNORECASE):
                return False

        # 检查是否包含有意义的模式
        for pattern in self.meaningful_patterns:
            if re.search(pattern, name_without_ext):
                return True

        # 如果包含空格、短横线、下划线等分隔符，可能是有意义的
        if re.search(r'[ _\-]+', name_without_ext):
            words = re.split(r'[ _\-]+', name_without_ext)
            meaningful_words = [w for w in words if len(w) >= 2]
            if len(meaningful_words) >= 2:
                return True

        return False

    def extract_keywords(self, text, max_words=5):
        """从文本中提取关键词"""
        if not text:
            return []

        # 分割成单词/词语
        words = []

        # 先按常见分隔符分割
        parts = re.split(r'[，,。！!？?；;\s\-_—|/\\]+', text)

        for part in parts:
            if not part:
                continue

            # 如果是中英文混合，进一步处理
            if re.search(r'[\u4e00-\u9fff]', part) and re.search(r'[a-zA-Z]', part):
                # 中英文混合，尝试分离
                chinese_parts = re.findall(r'[\u4e00-\u9fff]+', part)
                english_parts = re.findall(r'[a-zA-Z]{2,}', part)
                words.extend(chinese_parts)
                words.extend(english_parts)
            elif re.search(r'[\u4e00-\u9fff]', part):
                # 纯中文，按字符分割（但保持常用词组合）
                chinese_words = []
                current_word = ""
                for char in part:
                    if char in self.stop_words:
                        if current_word:
                            chinese_words.append(current_word)
                            current_word = ""
                    else:
                        current_word += char
                if current_word:
                    chinese_words.append(current_word)
                words.extend(chinese_words)
            else:
                # 英文，按单词分割
                english_words = re.findall(r'[a-zA-Z]{2,}', part)
                words.extend(english_words)

        # 过滤无用词
        filtered_words = []
        for word in words:
            word_lower = word.lower()
            if (word not in self.stop_words and
                    word_lower not in self.stop_words and
                    len(word) >= 2 and  # 至少2个字符
                    not word.isdigit() and  # 不是纯数字
                    not re.match(r'^[0-9]+$', word)):  # 不是数字
                filtered_words.append(word)

        # 去重但保持顺序
        seen = set()
        unique_words = []
        for word in filtered_words:
            if word not in seen:
                seen.add(word)
                unique_words.append(word)

        # 取前几个词
        return unique_words[:max_words]

    def evaluate_title_quality(self, title):
        """评估标题质量（0-1分）"""
        if not title:
            return 0.0

        score = 0.0

        # 1. 长度得分（适中最好）
        length = len(title)
        if 10 <= length <= 80:
            score += 0.3
        elif 5 <= length < 10:
            score += 0.1
        else:
            score -= 0.1

        # 2. 中文字符得分
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', title))
        if chinese_chars >= 3:
            score += 0.3
        elif chinese_chars > 0:
            score += 0.1

        # 3. 标点符号得分（表明是完整的句子/短语）
        if re.search(r'[。！？；，,\.\!\?;:]', title):
            score += 0.2

        # 4. 多样性得分（包含不同类型的字符）
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', title))
        has_english = bool(re.search(r'[a-zA-Z]', title))
        has_digit = bool(re.search(r'\d', title))
        has_punctuation = bool(re.search(r'[^\w\s]', title))

        char_types = sum([has_chinese, has_english, has_digit, has_punctuation])
        if char_types >= 2:
            score += 0.2

        # 5. 检查是否包含常见无意义模式
        for pattern in self.useless_patterns:
            if re.match(pattern, title):
                score -= 0.5
                break

        return min(max(score, 0.0), 1.0)

    def build_smart_filename(self, video_info, original_filename=""):
        """构建智能文件名"""
        if not video_info:
            return self.clean_filename(original_filename or "视频文件")

        title = video_info.get('title', '').strip()
        uploader = video_info.get('uploader', '').strip()
        extractor = video_info.get('extractor', '').strip()
        resolution = video_info.get('height', '')
        upload_date = video_info.get('upload_date', '')
        duration = video_info.get('duration', 0)

        # 获取配置
        strategy = self.config["Rename"]["rename_strategy"]
        use_smart = self.config["Rename"].getboolean("smart_rename")

        # 如果未启用智能重命名，使用模板方式
        if not use_smart:
            return self.build_template_filename(video_info)

        # 策略1：检查原文件名是否已有意义
        original_name_only = os.path.splitext(original_filename)[0] if original_filename else ""
        if (self.config["Rename"].getboolean("keep_original_if_good") and
                original_name_only and
                self.is_meaningful_filename(original_name_only)):
            # 彩蛋：在特殊日子里，给保留的原文件名添加表情
            if EasterEggs.hidden_feature_enabled():
                emoji = random.choice(["✨", "⭐", "🌟", "💫"])
                return self.clean_filename(f"{original_name_only}{emoji}")
            return self.clean_filename(original_name_only)

        # 根据策略选择命名方式
        if strategy == "auto":
            return self._auto_strategy(title, uploader, extractor, original_name_only)
        elif strategy == "smart":
            return self._smart_strategy(title, uploader)
        elif strategy == "title":
            return self._title_strategy(title)
        elif strategy == "combined":
            return self._combined_strategy(title, uploader)
        elif strategy == "compact":
            return self._compact_strategy(title, uploader, duration)
        else:  # template
            return self.build_template_filename(video_info)

    def _auto_strategy(self, title, uploader, extractor, original_name):
        """自动策略：智能选择最佳命名方案"""
        title_quality = self.evaluate_title_quality(title)

        # 高质量标题：直接使用
        if title_quality >= 0.7:
            final_name = title

        # 中等质量标题：提取关键词
        elif title_quality >= 0.4:
            keywords = self.extract_keywords(title, 4)
            if keywords:
                final_name = " ".join(keywords)
            else:
                final_name = title or "视频"

        # 低质量标题：尝试其他方案
        else:
            # 首先尝试从上传者信息构建
            if uploader:
                # 检查上传者是否平台名称
                is_platform = False
                for platform, keywords in self.platform_keywords.items():
                    if any(keyword.lower() in uploader.lower() for keyword in keywords):
                        is_platform = True
                        break

                if not is_platform:
                    final_name = f"{uploader}的视频"
                else:
                    final_name = "视频内容"
            else:
                # 尝试从原文件名提取信息
                if original_name:
                    # 移除常见无意义部分
                    clean_name = re.sub(r'^[0-9]+[ _\-]*', '', original_name)
                    clean_name = re.sub(r'^(vid|video|file|clip)[ _\-]*', '', clean_name, flags=re.IGNORECASE)
                    if clean_name and len(clean_name) >= 5:
                        final_name = clean_name
                    else:
                        final_name = "视频文件"
                else:
                    final_name = "视频文件"

        return final_name

    def _smart_strategy(self, title, uploader):
        """智能策略：提取核心信息"""
        keywords = self.extract_keywords(title, 3)

        if keywords:
            # 彩蛋：偶尔添加有趣的后缀
            if random.random() < 0.1:  # 10%概率
                funny_suffix = random.choice(["精选", "精华", "必看", "推荐", "超清"])
                return f"{' '.join(keywords)}-{funny_suffix}"
            return " ".join(keywords)
        elif uploader:
            return f"{uploader}的内容"
        else:
            return "视频"

    def _title_strategy(self, title):
        """标题策略：直接使用原标题"""
        if title:
            return title
        return "未命名视频"

    def _combined_strategy(self, title, uploader):
        """组合策略：上传者 + 标题"""
        if uploader and title:
            return f"{uploader} - {title}"
        elif uploader:
            return f"{uploader}的视频"
        elif title:
            return title
        else:
            return "视频文件"

    def _compact_strategy(self, title, uploader, duration):
        """紧凑策略：简洁命名，适合短内容"""
        keywords = self.extract_keywords(title, 2)

        if keywords:
            name = "".join(keywords[:2])
        elif title:
            # 截取标题前部分
            name = title[:15]
        else:
            name = "视频"

        # 添加时长信息（如果较短）
        if duration and duration < 300:  # 5分钟以内
            minutes = duration // 60
            seconds = duration % 60
            name = f"{name}_{minutes}分{seconds}秒"

        return name

    def build_template_filename(self, video_info):
        """使用模板构建文件名"""
        template = self.config["Rename"]["rename_template"]

        replacements = {
            '%(title)s': video_info.get('title', ''),
            '%(uploader)s': video_info.get('uploader', ''),
            '%(extractor)s': video_info.get('extractor', ''),
            '%(resolution)s': f"{video_info.get('height', '')}p" if video_info.get('height') else '',
            '%(upload_date)s': video_info.get('upload_date', ''),
            '%(id)s': video_info.get('id', ''),
            '%(playlist_title)s': video_info.get('playlist_title', ''),
            '%(playlist_index)s': str(video_info.get('playlist_index', '')).zfill(2),
            '%(duration)s': str(video_info.get('duration', 0)),
            '%(ext)s': video_info.get('ext', 'mp4'),
        }

        result = template
        for key, value in replacements.items():
            result = result.replace(key, str(value))

        return result

    def clean_filename(self, filename):
        """清理文件名，确保安全可用"""
        if not filename:
            return "视频文件"

        # 移除首尾空白
        filename = filename.strip()

        # 替换非法字符
        if self.config["Rename"].getboolean("replace_illegal_chars"):
            illegal_chars = r'[\\/*?:"<>|]'
            filename = re.sub(illegal_chars, "_", filename)

        # Windows文件名兼容性
        if self.config["Rename"].getboolean("windows_filenames"):
            # 移除Windows保留名称
            windows_reserved = ['CON', 'PRN', 'AUX', 'NUL',
                                'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                                'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
            name_upper = filename.upper()
            for reserved in windows_reserved:
                if name_upper == reserved or name_upper.startswith(reserved + '.'):
                    filename = "_" + filename

        # 限制长度
        max_length = int(self.config["Rename"]["max_char_length"])
        if max_length > 0 and len(filename) > max_length:
            # 智能截断：尽量在单词边界处截断
            truncated = filename
            separators = [' ', '-', '_', '.', '，', '。', ',', ';', ':', '、']

            for sep in separators:
                if sep in filename:
                    parts = filename.split(sep)
                    current = parts[0]
                    for part in parts[1:]:
                        if len(current + sep + part) <= max_length:
                            current += sep + part
                        else:
                            break
                    if current and len(current) <= max_length:
                        truncated = current
                        break

            # 如果仍然太长，硬截断但保留扩展名
            if len(truncated) > max_length:
                # 模拟扩展名处理（实际文件名构建时会添加扩展名）
                if '.' in truncated:
                    name_part, ext_part = truncated.rsplit('.', 1)
                    if len(ext_part) <= 10:  # 合理的扩展名长度
                        name_part = name_part[:max_length - len(ext_part) - 1]
                        truncated = f"{name_part}.{ext_part}"
                    else:
                        truncated = truncated[:max_length]
                else:
                    truncated = truncated[:max_length]

            filename = truncated

        # 确保文件名不为空
        if not filename or filename.isspace():
            # 彩蛋：生成有趣的默认文件名
            funny_names = ["精彩视频", "重要内容", "值得收藏", "必看片段", "精选集锦"]
            filename = random.choice(funny_names)

        return filename


# ============================================
# 配置处理函数
# ============================================
def get_resource_path(relative_path):
    """获取资源文件路径 - 修复打包后路径问题"""
    try:
        # Nuitka 打包后的临时目录（单文件模式）
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller 风格的临时目录
            base_path = sys._MEIPASS
        elif os.environ.get('NUITKA_ONEFILE_TEMP'):
            # Nuitka 单文件模式临时目录
            base_path = os.environ.get('NUITKA_ONEFILE_TEMP')
        else:
            base_path = os.path.dirname(sys.executable)
    except:
        # 开发环境
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    
    # 先检查临时目录
    temp_path = os.path.join(base_path, relative_path)
    if os.path.exists(temp_path):
        return temp_path
    
    # 检查当前执行文件所在目录
    exe_dir = os.path.dirname(sys.executable)
    exe_path = os.path.join(exe_dir, relative_path)
    if os.path.exists(exe_path):
        return exe_path
    
    # 检查当前工作目录（调试时）
    current_path = os.path.join(os.getcwd(), relative_path)
    if os.path.exists(current_path):
        return current_path
    
    # 如果都找不到，尝试在父目录中查找（Nuitka打包结构）
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file == os.path.basename(relative_path):
                return os.path.join(root, file)
    
    # 最后的手段：返回相对路径
    return relative_path


def load_config():
    """读取配置"""
    config = configparser.RawConfigParser()
    config_path = os.path.join(os.getcwd(), "downloader_config.ini")

    # 默认配置 - 扩展支持所有yt-dlp参数
    default_config = {
        "Basic": {
            "resolution": "最高分辨率",
            "output_format": "mp4",
            "embed_cover": "True",
            "embed_metadata": "True",
            "skip_existing": "True",
            "extract_audio": "False",
            "audio_format": "best",
            "audio_quality": "5"
        },
        "Advanced": {
            "no_check_certificate": "True",
            "no_warnings": "False",
            "retries": "3",
            "fragment_retries": "10",
            "timeout": "60",
            "socket_timeout": "60",
            "concurrent_fragments": "5",
            "limit_rate": "",
            "throttled_rate": "",
            "proxy": "",
            "source_address": "",
            "impersonate": "",
            "force_ipv4": "False",
            "force_ipv6": "False",
            "allow_dynamic_mpd": "True",
            "hls_split_discontinuity": "False",
            "extractor_retries": "3"
        },
        "Path": {
            "download_path": os.path.expanduser("~/Downloads"),
            "cookie_path": "",
            "auto_open_folder": "True",
            "cache_dir": "",
            "ffmpeg_location": ""
        },
        "Batch": {
            "auto_recognize_batch": "True",
            "playlist_items": "",
            "max_downloads": "",
            "playlist_random": "False",
            "playlist_reverse": "False",
            "lazy_playlist": "False"
        },
        "Selection": {
            "min_filesize": "",
            "max_filesize": "",
            "date": "",
            "datebefore": "",
            "dateafter": "",
            "match_filters": "",
            "age_limit": "",
            "download_archive": ""
        },
        "Classification": {
            "classify_rule": "不分类",
            "date_format": "YYYY/MM/DD"
        },
        "Rename": {
            "rename_template": "%(title)s",
            "max_char_length": "100",
            "replace_illegal_chars": "True",
            "windows_filenames": "False",
            "trim_filenames": "",
            # 新增智能重命名选项
            "smart_rename": "True",
            "rename_strategy": "auto",
            "min_meaningful_length": "10",
            "use_uploader_as_fallback": "True",
            "include_resolution": "False",
            "include_date": "False",
            "keep_original_if_good": "True"
        },
        "Subtitles": {
            "write_subs": "False",
            "write_auto_subs": "False",
            "sub_format": "best",
            "sub_langs": "all",
            "embed_subs": "False",
            "convert_subs": "none"
        },
        "SponsorBlock": {
            "sponsorblock_mark": "",
            "sponsorblock_remove": "",
            "sponsorblock_chapter_title": "[SponsorBlock]: %(category_names)l",
            "sponsorblock_api": "https://sponsor.ajay.app"
        },
        "PostProcessing": {
            "remux_video": "",
            "recode_video": "",
            "keep_video": "False",
            "post_overwrites": "True",
            "embed_chapters": "False",
            "embed_info_json": "False",
            "split_chapters": "False",
            "remove_chapters": "",
            "force_keyframes_at_cuts": "False",
            "concat_playlist": "multi_video",
            "fixup": "detect_or_warn",
            "exec_cmd": ""
        },
        "UI": {
            "theme": "light",
            "font_size": "10",
            "window_width": "1200",
            "window_height": "800",
            "show_advanced": "False"
        },
        "EasterEggs": {  # 新增彩蛋配置
            "enable_funny_messages": "True",
            "enable_secret_logos": "True",
            "enable_hidden_features": "True"
        }
    }

    # 首次运行生成配置文件
    if not os.path.exists(config_path):
        config.read_dict(default_config)
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                config.write(f)
        except Exception as e:
            print(f"创建配置文件失败: {e}")
    else:
        try:
            config.read(config_path, encoding="utf-8")
        except Exception as e:
            print(f"读取配置文件失败: {e}")
            config.read_dict(default_config)

        # 兼容旧配置文件，新增缺失的配置项
        for section, options in default_config.items():
            if not config.has_section(section):
                config.add_section(section)
            for key, value in options.items():
                if not config.has_option(section, key):
                    config.set(section, key, value)

    return config, config_path


def save_config(config, config_path):
    """保存配置"""
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            config.write(f)
        return True
    except Exception as e:
        print(f"保存配置失败: {e}")
        return False


# ============================================
# 工具函数
# ============================================
def sanitize_filename(filename, max_length=100, replace_illegal=True):
    """清理文件名，确保安全"""
    if not filename:
        return "untitled"

    # 替换非法字符
    if replace_illegal:
        illegal_chars = r'[\\/*?:"<>|]'
        filename = re.sub(illegal_chars, "_", filename)

    # 限制长度
    if len(filename) > max_length and max_length > 0:
        name, ext = os.path.splitext(filename)
        # 保留扩展名
        if len(ext) > 10:  # 扩展名异常长的情况
            ext = ""
        filename = name[:max_length - len(ext)] + ext

    return filename


def check_disk_space(path, required_space_mb=100):
    """检测磁盘剩余空间"""
    try:
        if os.name == 'nt':
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(path),
                None,
                None,
                ctypes.pointer(free_bytes)
            )
            free_space_mb = free_bytes.value / (1024 * 1024)
        else:
            statvfs = os.statvfs(path)
            free_space_mb = (statvfs.f_bfree * statvfs.f_frsize) / (1024 * 1024)
        return free_space_mb >= required_space_mb, round(free_space_mb, 2)
    except Exception as e:
        print(f"检测磁盘空间失败: {e}")
        return False, 0


# ============================================
# 拖放组件
# ============================================
class DragDropLineEdit(QLineEdit):
    """支持拖放的文件/路径输入框"""

    def __init__(self, placeholder_text="", is_file=True, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder_text)
        self.setAcceptDrops(True)
        self.is_file = is_file

        # 修复：移除box-shadow，使用边框阴影效果
        self.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #d1d1d1;
                border-radius: 8px;
                background-color: #ffffff;
                font-size: 10pt;
                color: #333333;
            }
            QLineEdit:focus {
                border: 2px solid #0078d4;
                background-color: #f8f9fa;
                outline: none;
            }
            QLineEdit:disabled {
                background-color: #f0f0f0;
                color: #999999;
            }
        """)
        self.setMinimumHeight(38)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if (self.is_file and os.path.isfile(path)) or (not self.is_file and os.path.isdir(path)):
                self.setText(path)
                self.setStyleSheet("""
                    QLineEdit {
                        padding: 8px;
                        border: 2px solid #4CAF50;
                        border-radius: 8px;
                        background-color: #f1f8e9;
                        font-size: 10pt;
                        color: #333333;
                    }
                """)
                QTimer.singleShot(800, lambda: self.setStyleSheet("""
                    QLineEdit {
                        padding: 8px;
                        border: 2px solid #d1d1d1;
                        border-radius: 8px;
                        background-color: #ffffff;
                        font-size: 10pt;
                        color: #333333;
                    }
                """))
            else:
                self.setStyleSheet("""
                    QLineEdit {
                        padding: 8px;
                        border: 2px solid #f44336;
                        border-radius: 8px;
                        background-color: #ffebee;
                        font-size: 10pt;
                        color: #333333;
                    }
                """)
                QTimer.singleShot(1000, lambda: self.setStyleSheet("""
                    QLineEdit {
                        padding: 8px;
                        border: 2px solid #d1d1d1;
                        border-radius: 8px;
                        background-color: #ffffff;
                        font-size: 10pt;
                        color: #333333;
                    }
                """))


class DragDropTextEdit(QTextEdit):
    """支持拖放的文本框"""

    def __init__(self, placeholder_text="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder_text)
        self.setAcceptDrops(True)

        # 修复：移除box-shadow
        self.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                border: 2px solid #d1d1d1;
                border-radius: 8px;
                background-color: #ffffff;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 10pt;
                color: #333333;
            }
            QTextEdit:focus {
                border: 2px solid #0078d4;
                background-color: #f8f9fa;
                outline: none;
            }
            QTextEdit:disabled {
                background-color: #f0f0f0;
                color: #999999;
            }
        """)
        self.setMinimumHeight(120)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if os.path.isfile(path) and path.lower().endswith('.txt'):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.setText(content)
                    self.setStyleSheet("""
                        QTextEdit {
                            padding: 8px;
                            border: 2px solid #4CAF50;
                            border-radius: 8px;
                            background-color: #f1f8e9;
                            font-family: 'Consolas', 'Courier New', monospace;
                            font-size: 10pt;
                        }
                    """)
                    QTimer.singleShot(800, lambda: self.setStyleSheet("""
                        QTextEdit {
                            padding: 8px;
                            border: 2px solid #d1d1d1;
                            border-radius: 8px;
                            background-color: #ffffff;
                            font-family: 'Consolas', 'Courier New', monospace;
                            font-size: 10pt;
                        }
                    """))
                except Exception as e:
                    self.setStyleSheet("""
                        QTextEdit {
                            padding: 8px;
                            border: 2px solid #f44336;
                            border-radius: 8px;
                            background-color: #ffebee;
                            font-family: 'Consolas', 'Courier New', monospace;
                            font-size: 10pt;
                        }
                    """)
                    QTimer.singleShot(1000, lambda: self.setStyleSheet("""
                        QTextEdit {
                            padding: 8px;
                            border: 2px solid #d1d1d1;
                            border-radius: 8px;
                            background-color: #ffffff;
                            font-family: 'Consolas', 'Courier New', monospace;
                            font-size: 10pt;
                        }
                    """))
            else:
                # 拖入单个链接
                self.append(path.strip())
                self.setStyleSheet("""
                    QTextEdit {
                        padding: 8px;
                        border: 2px solid #0078d4;
                        border-radius: 8px;
                        background-color: #e3f2fd;
                        font-family: 'Consolas', 'Courier New', monospace;
                        font-size: 10pt;
                    }
                """)
                QTimer.singleShot(800, lambda: self.setStyleSheet("""
                    QTextEdit {
                        padding: 8px;
                        border: 2px solid #d1d1d1;
                        border-radius: 8px;
                        background-color: #ffffff;
                        font-family: 'Consolas', 'Courier New', monospace;
                        font-size: 10pt;
                    }
                """))


# ============================================
# 下载线程
# ============================================
class BatchDownloadThread(QThread):
    """批量下载线程"""
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int, int)
    finish_signal = pyqtSignal(bool, str)
    info_signal = pyqtSignal(dict)

    def __init__(self, url_list, config):
        super().__init__()
        self.url_list = [url.strip() for url in url_list if url.strip()]
        self.config = config
        self.total_count = len(self.url_list)
        self.current_index = 0
        self.success_count = 0
        self.fail_count = 0

        # 初始化智能重命名器
        self.renamer = SmartRenamer(config)

        # 获取工具路径
        self.yt_dlp_path = get_resource_path("yt-dlp.exe")
        self.ffmpeg_path = get_resource_path("ffmpeg.exe")

        # 检查工具是否存在
        self.tools_ok = self.check_tools()

        self.auto_open_folder = config["Path"].getboolean("auto_open_folder")

        # 彩蛋：初始化有趣消息计数器
        self.funny_message_count = 0
        self.last_funny_message_time = 0

    def check_tools(self):
        """检查必要工具是否存在"""
        if not os.path.exists(self.yt_dlp_path):
            self.log_signal.emit(f"【错误】yt-dlp.exe 不存在于: {self.yt_dlp_path}")
            return False

        if not os.path.exists(self.ffmpeg_path):
            self.log_signal.emit(f"【警告】ffmpeg.exe 不存在，可能影响视频合并和后处理")

        return True

    def get_video_info(self, url):
        """获取视频信息"""
        try:
            cmd = [
                self.yt_dlp_path,
                "--dump-json",
                "--no-playlist" if not self.config["Batch"].getboolean("auto_recognize_batch") else "",
                url
            ]
            # 过滤空参数
            cmd = [c for c in cmd if c]

            # 添加证书验证选项
            if self.config["Advanced"].getboolean("no_check_certificate"):
                cmd.append("--no-check-certificate")

            if self.config["Advanced"]["proxy"]:
                cmd.extend(["--proxy", self.config["Advanced"]["proxy"]])

            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='ignore',
                timeout=int(self.config["Advanced"]["timeout"]),
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            if result.returncode == 0:
                try:
                    info = json.loads(result.stdout)
                    return info
                except json.JSONDecodeError as e:
                    self.log_signal.emit(f"【警告】解析视频信息失败: {e}")
                    # 尝试从输出中提取JSON
                    for line in result.stdout.split('\n'):
                        if line.strip().startswith('{'):
                            try:
                                return json.loads(line)
                            except:
                                continue
            else:
                self.log_signal.emit(f"【警告】获取信息失败: {result.stderr[:200]}")

            return None
        except subprocess.TimeoutExpired:
            self.log_signal.emit("【超时】获取视频信息超时")
            return None
        except Exception as e:
            self.log_signal.emit(f"【错误】获取视频信息异常: {str(e)}")
            return None

    def build_download_command(self, url, video_info=None):
        """构建下载命令，支持所有yt-dlp参数"""
        params = [self.yt_dlp_path]

        # 基础参数
        params.extend(["--newline"])

        # 彩蛋：偶尔添加有趣参数（不影响功能）
        if EasterEggs.hidden_feature_enabled() and random.random() < 0.3:
            funny_params = ["--verbose", "--print-json", "--force-ipv4"]
            params.append(random.choice(funny_params))

        # 添加忽略错误参数（解决101错误问题）
        params.extend(["--ignore-errors", "--no-abort-on-error"])

        # 证书和警告设置
        if self.config["Advanced"].getboolean("no_check_certificate"):
            params.append("--no-check-certificate")

        if self.config["Advanced"].getboolean("no_warnings"):
            params.append("--no-warnings")

        # 重试和超时设置
        params.extend(["--retries", self.config["Advanced"]["retries"]])
        params.extend(["--fragment-retries", self.config["Advanced"]["fragment_retries"]])
        params.extend(["--socket-timeout", self.config["Advanced"]["socket_timeout"]])
        params.extend(["--concurrent-fragments", self.config["Advanced"]["concurrent_fragments"]])

        # 速率限制
        if self.config["Advanced"]["limit_rate"]:
            params.extend(["--limit-rate", self.config["Advanced"]["limit_rate"]])

        if self.config["Advanced"]["throttled_rate"]:
            params.extend(["--throttled-rate", self.config["Advanced"]["throttled_rate"]])

        # 网络设置
        if self.config["Advanced"]["proxy"]:
            params.extend(["--proxy", self.config["Advanced"]["proxy"]])

        if self.config["Advanced"]["source_address"]:
            params.extend(["--source-address", self.config["Advanced"]["source_address"]])

        if self.config["Advanced"]["impersonate"]:
            params.extend(["--impersonate", self.config["Advanced"]["impersonate"]])

        if self.config["Advanced"].getboolean("force_ipv4"):
            params.append("-4")

        if self.config["Advanced"].getboolean("force_ipv6"):
            params.append("-6")

        # 提取器设置
        if not self.config["Advanced"].getboolean("allow_dynamic_mpd"):
            params.append("--ignore-dynamic-mpd")

        if self.config["Advanced"].getboolean("hls_split_discontinuity"):
            params.append("--hls-split-discontinuity")

        params.extend(["--extractor-retries", self.config["Advanced"]["extractor_retries"]])

        # Cookie设置
        cookie_path = self.config["Path"]["cookie_path"]
        if cookie_path and os.path.exists(cookie_path):
            params.extend(["--cookies", cookie_path])

        # 缓存设置
        if self.config["Path"]["cache_dir"]:
            params.extend(["--cache-dir", self.config["Path"]["cache_dir"]])
        else:
            params.append("--no-cache-dir")

        # 批量下载设置
        if self.config["Batch"]["playlist_items"]:
            params.extend(["--playlist-items", self.config["Batch"]["playlist_items"]])

        if self.config["Batch"]["max_downloads"]:
            params.extend(["--max-downloads", self.config["Batch"]["max_downloads"]])

        if self.config["Batch"].getboolean("playlist_random"):
            params.append("--playlist-random")

        if self.config["Batch"].getboolean("lazy_playlist"):
            params.append("--lazy-playlist")

        # 视频选择设置
        if self.config["Selection"]["min_filesize"]:
            params.extend(["--min-filesize", self.config["Selection"]["min_filesize"]])

        if self.config["Selection"]["max_filesize"]:
            params.extend(["--max-filesize", self.config["Selection"]["max_filesize"]])

        if self.config["Selection"]["date"]:
            params.extend(["--date", self.config["Selection"]["date"]])

        if self.config["Selection"]["datebefore"]:
            params.extend(["--datebefore", self.config["Selection"]["datebefore"]])

        if self.config["Selection"]["dateafter"]:
            params.extend(["--dateafter", self.config["Selection"]["dateafter"]])

        if self.config["Selection"]["match_filters"]:
            params.extend(["--match-filters", self.config["Selection"]["match_filters"]])

        if self.config["Selection"]["age_limit"]:
            params.extend(["--age_limit", self.config["Selection"]["age_limit"]])

        if self.config["Selection"]["download_archive"]:
            params.extend(["--download-archive", self.config["Selection"]["download_archive"]])

        # 分辨率和格式选择
        resolution = self.config["Basic"]["resolution"]
        if resolution == "最高分辨率":
            format_spec = "bestvideo+bestaudio/best"
        elif resolution == "1080p":
            format_spec = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
        elif resolution == "720p":
            format_spec = "bestvideo[height<=720]+bestaudio/best[height<=720]"
        elif resolution == "480p":
            format_spec = "bestvideo[height<=480]+bestaudio/best[height<=480]"
        elif resolution == "360p":
            format_spec = "bestvideo[height<=360]+bestaudio/best[height<=360]"
        else:
            format_spec = "bestvideo+bestaudio/best"

        # 音频提取设置
        if self.config["Basic"].getboolean("extract_audio"):
            params.append("-x")
            params.extend(["--audio-format", self.config["Basic"]["audio_format"]])
            params.extend(["--audio-quality", self.config["Basic"]["audio_quality"]])
            format_spec = "ba/b"  # 最佳音频

        params.extend(["-f", format_spec])

        # 输出格式和合并设置
        output_format = self.config["Basic"]["output_format"]
        params.extend(["--merge-output-format", output_format])

        # 字幕设置
        if self.config["Subtitles"].getboolean("write_subs"):
            params.append("--write-subs")

        if self.config["Subtitles"].getboolean("write_auto_subs"):
            params.append("--write-auto-subs")

        if self.config["Subtitles"]["sub_format"]:
            params.extend(["--sub-format", self.config["Subtitles"]["sub_format"]])

        if self.config["Subtitles"]["sub_langs"]:
            params.extend(["--sub-langs", self.config["Subtitles"]["sub_langs"]])

        if self.config["Subtitles"].getboolean("embed_subs"):
            params.append("--embed-subs")

        if self.config["Subtitles"]["convert_subs"] and self.config["Subtitles"]["convert_subs"] != "none":
            params.extend(["--convert-subs", self.config["Subtitles"]["convert_subs"]])

        # 元数据和封面设置
        if self.config["Basic"].getboolean("embed_cover"):
            params.append("--embed-thumbnail")

        if self.config["Basic"].getboolean("embed_metadata"):
            params.append("--add-metadata")  # 使用--add-metadata而不是--embed-metadata

        if self.config["PostProcessing"].getboolean("embed_chapters"):
            params.append("--embed-chapters")

        if self.config["PostProcessing"].getboolean("embed_info_json"):
            params.append("--embed-info-json")

        # 覆盖和续传设置
        if self.config["Basic"].getboolean("skip_existing"):
            params.append("--no-overwrites")
            params.append("--continue")
        else:
            params.append("--force-overwrites")

        # 批量识别播放列表
        if self.config["Batch"].getboolean("auto_recognize_batch"):
            params.append("--yes-playlist")
        else:
            params.append("--no-playlist")

        # 后处理设置
        if self.config["PostProcessing"]["remux_video"]:
            params.extend(["--remux-video", self.config["PostProcessing"]["remux_video"]])

        if self.config["PostProcessing"]["recode_video"]:
            params.extend(["--recode-video", self.config["PostProcessing"]["recode_video"]])

        if self.config["PostProcessing"].getboolean("keep_video"):
            params.append("--keep-video")

        if not self.config["PostProcessing"].getboolean("post_overwrites"):
            params.append("--no-post-overwrites")

        if self.config["PostProcessing"].getboolean("split_chapters"):
            params.append("--split-chapters")

        if self.config["PostProcessing"]["remove_chapters"]:
            params.extend(["--remove-chapters", self.config["PostProcessing"]["remove_chapters"]])

        if self.config["PostProcessing"].getboolean("force_keyframes_at_cuts"):
            params.append("--force-keyframes-at-cuts")

        params.extend(["--concat-playlist", self.config["PostProcessing"]["concat_playlist"]])
        params.extend(["--fixup", self.config["PostProcessing"]["fixup"]])

        # SponsorBlock设置
        if self.config["SponsorBlock"]["sponsorblock_mark"]:
            params.extend(["--sponsorblock-mark", self.config["SponsorBlock"]["sponsorblock_mark"]])

        if self.config["SponsorBlock"]["sponsorblock_remove"]:
            params.extend(["--sponsorblock-remove", self.config["SponsorBlock"]["sponsorblock_remove"]])

        if self.config["SponsorBlock"]["sponsorblock_chapter_title"]:
            params.extend(["--sponsorblock-chapter-title", self.config["SponsorBlock"]["sponsorblock_chapter_title"]])

        if self.config["SponsorBlock"]["sponsorblock_api"]:
            params.extend(["--sponsorblock-api", self.config["SponsorBlock"]["sponsorblock_api"]])

        # 执行命令设置
        if self.config["PostProcessing"]["exec_cmd"]:
            params.extend(["--exec", self.config["PostProcessing"]["exec_cmd"]])

        # ffmpeg路径设置
        ffmpeg_path = self.config["Path"]["ffmpeg_location"] or self.ffmpeg_path
        if ffmpeg_path and os.path.exists(ffmpeg_path):
            ffmpeg_dir = os.path.dirname(ffmpeg_path)
            params.extend(["--ffmpeg-location", ffmpeg_dir])

        # 输出路径和文件名处理
        download_path = self.config["Path"]["download_path"]
        if not os.path.exists(download_path):
            os.makedirs(download_path, exist_ok=True)

        # 分类规则
        classify_rule = self.config["Classification"]["classify_rule"]
        if classify_rule != "不分类":
            if classify_rule == "按平台" and video_info:
                folder = video_info.get("extractor", "未知平台")
                # 平台名称映射
                platform_map = {
                    "Bilibili": "B站",
                    "Youtube": "YouTube",
                    "Douyin": "抖音",
                    "TikTok": "TikTok"
                }
                folder = platform_map.get(folder, folder)
            elif classify_rule == "按作者" and video_info:
                folder = video_info.get("uploader", "未知作者")
            elif classify_rule == "按番剧" and video_info:
                folder = video_info.get("playlist_title", video_info.get("series", "未知番剧"))
            elif classify_rule == "按日期":
                date_format = self.config["Classification"]["date_format"]
                upload_date = video_info.get("upload_date", "") if video_info else ""
                if upload_date and len(upload_date) == 8:
                    year = upload_date[:4]
                    month = upload_date[4:6]
                    day = upload_date[6:8]
                    folder = date_format.replace("YYYY", year).replace("MM", month).replace("DD", day)
                else:
                    folder = time.strftime("%Y/%m/%d")
            else:
                folder = ""

            if folder:
                # 清理文件夹名
                folder = self.renamer.clean_filename(folder)
                download_path = os.path.join(download_path, folder)
                os.makedirs(download_path, exist_ok=True)

        # 构建输出模板 - 简化模板，后续智能重命名
        output_template = os.path.join(download_path, "%(title)s.%(ext)s")

        # 添加输出参数
        params.extend(["-o", output_template])

        # 文件名设置
        if self.config["Rename"].getboolean("replace_illegal_chars"):
            params.append("--restrict-filenames")

        if self.config["Rename"].getboolean("windows_filenames"):
            params.append("--windows-filenames")

        if self.config["Rename"]["trim_filenames"]:
            params.extend(["--trim-filenames", self.config["Rename"]["trim_filenames"]])

        # 添加URL
        params.append(url)

        return params, download_path

    def run(self):
        if not self.tools_ok:
            self.finish_signal.emit(False, "必要工具缺失，请检查yt-dlp.exe是否存在")
            return

        fail_urls = []
        last_save_path = ""

        # 彩蛋：随机发送有趣的开场消息
        if self.config["EasterEggs"].getboolean("enable_funny_messages") and random.random() < 0.3:
            funny_start = random.choice([
                "🎬 视频下载大冒险开始！",
                "🚀 发射下载火箭！",
                "🦸 超级下载模式启动！",
                "🎪 下载马戏团开演啦！"
            ])
            self.log_signal.emit(f"✨ {funny_start}")

        try:
            # 检查磁盘空间
            disk_ok, free_space = check_disk_space(self.config["Path"]["download_path"])
            if not disk_ok:
                self.log_signal.emit(f"【错误】磁盘空间不足！剩余: {free_space}MB，需要至少100MB")
                self.finish_signal.emit(False, f"磁盘空间不足 ({free_space}MB)")
                return

            self.log_signal.emit(f"【开始】批量下载任务: {self.total_count}个，磁盘剩余: {free_space:.1f}MB")

            for idx, url in enumerate(self.url_list, 1):
                self.current_index = idx
                self.progress_signal.emit(idx, self.total_count)

                self.log_signal.emit(f"\n{'=' * 60}")
                self.log_signal.emit(f"任务 {idx}/{self.total_count}: {url}")

                # 获取视频信息
                self.log_signal.emit("获取视频信息中...")
                video_info = self.get_video_info(url)

                if video_info:
                    self.info_signal.emit(video_info)
                    title = video_info.get('title', '未知标题')
                    self.log_signal.emit(f"视频标题: {title}")

                    # 彩蛋：有趣的标题评论
                    if self.config["EasterEggs"].getboolean("enable_funny_messages") and random.random() < 0.2:
                        comments = ["听起来不错！", "有点意思~", "期待内容！", "标题很吸引人！", "马上开始下载！"]
                        self.log_signal.emit(f"💬 {random.choice(comments)}")
                else:
                    self.log_signal.emit("【警告】无法获取视频详细信息，使用默认设置")
                    video_info = {}

                # 构建命令
                cmd_params, save_path = self.build_download_command(url, video_info)
                last_save_path = save_path

                self.log_signal.emit(f"保存路径: {save_path}")
                self.log_signal.emit(f"下载命令: {' '.join(cmd_params[:10])}...")  # 只显示前10个参数

                # 执行下载
                try:
                    process = subprocess.Popen(
                        cmd_params,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        bufsize=1,
                        universal_newlines=True,
                        encoding='utf-8',
                        errors='ignore',
                        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                    )

                    # 实时读取输出
                    for line in iter(process.stdout.readline, ''):
                        line = line.strip()
                        if line:
                            # 过滤掉一些过于详细的日志
                            if not any(x in line.lower() for x in ['fragment', 'download', 'merging']):
                                self.log_signal.emit(line)

                                # 彩蛋：偶尔添加有趣的进度消息
                                current_time = time.time()
                                if (self.config["EasterEggs"].getboolean("enable_funny_messages") and
                                        current_time - self.last_funny_message_time > 30 and
                                        random.random() < 0.1):
                                    self.log_signal.emit(
                                        f"💡 {EasterEggs.get_funny_progress_message(self.current_index / self.total_count * 100)}")
                                    self.last_funny_message_time = current_time

                    process.wait()

                    # 智能错误处理：将101等警告性错误码视为成功
                    if process.returncode == 0:
                        self.success_count += 1
                        self.log_signal.emit(f"✅ 任务 {idx} 完成")

                        # 尝试智能重命名文件
                        if self.config["Rename"].getboolean("smart_rename") and video_info:
                            self.smart_rename_file(save_path, video_info)

                    elif process.returncode == 101:  # 警告性错误，但功能完成
                        self.success_count += 1
                        self.log_signal.emit(f"⚠️ 任务 {idx} 完成但有警告（视频可能已成功下载）")

                        # 尝试智能重命名文件
                        if self.config["Rename"].getboolean("smart_rename") and video_info:
                            self.smart_rename_file(save_path, video_info)

                        # 彩蛋：有趣的错误消息
                        if self.config["EasterEggs"].getboolean("enable_funny_messages"):
                            self.log_signal.emit(f"😅 {EasterEggs.get_funny_error_message()}")
                    else:
                        self.fail_count += 1
                        fail_urls.append(url)
                        self.log_signal.emit(f"❌ 任务 {idx} 错误码: {process.returncode}")

                except Exception as e:
                    self.fail_count += 1
                    fail_urls.append(url)
                    self.log_signal.emit(f"❌ 任务 {idx} 异常: {str(e)}")

                    # 彩蛋：有趣的异常消息
                    if self.config["EasterEggs"].getboolean("enable_funny_messages") and random.random() < 0.5:
                        self.log_signal.emit("🆘 需要帮助吗？检查网络连接或稍后重试。")

            # 汇总结果
            success_rate = self.success_count / self.total_count if self.total_count > 0 else 0

            # 彩蛋：根据成功率发送不同消息
            if self.config["EasterEggs"].getboolean("enable_funny_messages"):
                if success_rate == 1.0:
                    summary = random.choice([
                        f"🎉 完美！全部 {self.success_count} 个任务都成功了！",
                        f"🏆 全胜！{self.success_count}/{self.total_count} 任务完成！",
                        f"🌟 太棒了！{self.success_count} 个视频已就绪！"
                    ])
                elif success_rate >= 0.7:
                    summary = f"👍 不错！成功: {self.success_count}, 失败: {self.fail_count}"
                else:
                    summary = f"📊 结果：成功: {self.success_count}, 失败: {self.fail_count}"
            else:
                summary = f"批量下载完成！成功: {self.success_count}, 失败: {self.fail_count}"

            if fail_urls:
                summary += f"\n失败链接:\n" + "\n".join(fail_urls)

            # 自动打开文件夹
            if self.auto_open_folder and self.success_count > 0 and last_save_path and os.path.exists(last_save_path):
                try:
                    if os.name == 'nt':
                        os.startfile(last_save_path)
                    else:
                        subprocess.Popen(['xdg-open', last_save_path])
                    self.log_signal.emit(f"📂 已打开文件夹: {last_save_path}")
                except Exception as e:
                    self.log_signal.emit(f"⚠️ 打开文件夹失败: {str(e)}")

            # 发送完成信号（如果只有101警告，仍然认为是成功的）
            if self.fail_count == 0:
                self.finish_signal.emit(True, summary)
            else:
                self.finish_signal.emit(False, summary)

        except Exception as e:
            error_msg = f"批量下载异常: {str(e)}"
            self.log_signal.emit(f"❌ {error_msg}")
            self.finish_signal.emit(False, error_msg)

    def smart_rename_file(self, save_path, video_info):
        """智能重命名下载的文件"""
        try:
            # 查找视频文件
            video_extensions = ['.mp4', '.mkv', '.webm', '.avi', '.mov', '.flv']
            files = [f for f in os.listdir(save_path)
                     if os.path.isfile(os.path.join(save_path, f)) and
                     os.path.splitext(f)[1].lower() in video_extensions]

            if not files:
                return

            # 找到最新的视频文件（按修改时间）
            files_with_time = [(f, os.path.getmtime(os.path.join(save_path, f))) for f in files]
            latest_file = max(files_with_time, key=lambda x: x[1])[0]

            old_path = os.path.join(save_path, latest_file)
            old_name, old_ext = os.path.splitext(latest_file)

            # 构建新文件名
            new_name = self.renamer.build_smart_filename(video_info, old_name)
            new_filename = f"{new_name}{old_ext}"
            new_path = os.path.join(save_path, new_filename)

            # 避免文件名冲突
            counter = 1
            while os.path.exists(new_path):
                new_filename = f"{new_name}_{counter}{old_ext}"
                new_path = os.path.join(save_path, new_filename)
                counter += 1

            # 重命名文件
            if old_path != new_path:
                os.rename(old_path, new_path)
                self.log_signal.emit(f"📝 智能重命名: {latest_file} → {new_filename}")

                # 彩蛋：偶尔添加有趣的注释
                if self.config["EasterEggs"].getboolean("enable_funny_messages") and random.random() < 0.15:
                    comments = ["新名字更直观吧？", "文件名更友好了！", "这样更容易找到！", "智能命名完成！"]
                    self.log_signal.emit(f"💡 {random.choice(comments)}")

        except Exception as e:
            self.log_signal.emit(f"⚠️ 智能重命名失败: {str(e)}")


# ============================================
# 设置窗口
# ============================================
class SettingsWindow(QDialog):
    """设置窗口 - 支持所有yt-dlp参数的可视化配置"""

    def __init__(self, parent, config, config_path):
        super().__init__(parent)
        self.config = config
        self.config_path = config_path
        self.setWindowTitle("设置")
        self.setModal(True)
        self.init_ui()
        self.load_settings()

        # 彩蛋：秘密按键序列检测
        self.secret_sequence, self.check_secret = EasterEggs.secret_key_sequence()
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        """事件过滤器，用于检测秘密按键序列"""
        if event.type() == event.KeyPress:
            key = event.key()
            # 记录按键（转换为字符）
            if Qt.Key_A <= key <= Qt.Key_Z:
                char = chr(key).upper()
                self.secret_sequence.append(char)
            elif Qt.Key_0 <= key <= Qt.Key_9:
                char = chr(key)
                self.secret_sequence.append(char)
            elif key in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right]:
                directions = {Qt.Key_Up: '上', Qt.Key_Down: '下',
                              Qt.Key_Left: '左', Qt.Key_Right: '右'}
                self.secret_sequence.append(directions[key])

            # 检查秘密序列
            message = self.check_secret()
            if message:
                QMessageBox.information(self, "彩蛋发现！🥚", message)
                self.secret_sequence.clear()

        return super().eventFilter(obj, event)

    def init_ui(self):
        """初始化UI"""
        self.setMinimumSize(1000, 800)
        self.setGeometry(100, 100, 1000, 800)

        # 设置样式 - 修复：移除所有box-shadow
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f7fa;
            }
            QTabWidget::pane {
                border: 2px solid #dce1e6;
                background-color: white;
                border-radius: 12px;
                margin-top: 4px;
            }
            QTabBar::tab {
                padding: 10px 20px;
                background-color: #f0f3f7;
                border: 2px solid #dce1e6;
                border-bottom-color: #dce1e6;
                border-radius: 8px 8px 0 0;
                margin-right: 4px;
                font-weight: 500;
                color: #5c6770;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-color: #dce1e6;
                border-bottom-color: white;
                font-weight: 600;
                color: #1c2b36;
            }
            QGroupBox {
                border: 2px solid #e8ecef;
                border-radius: 10px;
                margin-top: 15px;
                padding: 18px;
                background-color: white;
                font-weight: 600;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                top: -10px;
                background-color: white;
                padding: 0 8px;
                font-weight: 600;
                color: #2c3e50;
            }
            QLabel {
                color: #34495e;
                font-size: 11pt;
                font-weight: 500;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #0078d4, stop:1 #005a9e);
                color: white;
                border: 2px solid #005a9e;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 11pt;
                font-weight: 600;
                min-height: 36px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #0066b2, stop:1 #004578);
                border: 2px solid #004578;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #005cae, stop:1 #003c6e);
                border: 2px solid #003c6e;
            }
            QPushButton:disabled {
                background-color: #c8d0d8;
                color: #8a9ba8;
                border-color: #a6b3bf;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                padding: 8px 12px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                font-size: 11pt;
                min-height: 36px;
                background-color: #f8fafc;
                color: #2c3e50;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border: 2px solid #0078d4;
                background-color: #ffffff;
                outline: none;
            }
            QCheckBox {
                spacing: 12px;
                font-size: 11pt;
                color: #34495e;
                font-weight: 500;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #c8d0d8;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                background-color: #0078d4;
                border-color: #0078d4;
                image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path fill="white" d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>');
            }
            QTextEdit {
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                padding: 12px;
                font-size: 11pt;
                background-color: #f8fafc;
                color: #2c3e50;
            }
            QTextEdit:focus {
                border: 2px solid #0078d4;
                background-color: #ffffff;
                outline: none;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #f0f3f7;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #c8d0d8;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a6b3bf;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title_label = QLabel("设置")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 22pt;
                font-weight: 700;
                color: #1c2b36;
                padding: 10px 0;
                border-bottom: 3px solid #0078d4;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::tab-bar {
                alignment: center;
            }
        """)
        main_layout.addWidget(self.tab_widget)

        # 创建各个标签页
        self.create_basic_tab()
        self.create_audio_video_tab()
        self.create_network_tab()
        self.create_batch_tab()
        self.create_selection_tab()
        self.create_subtitles_tab()
        self.create_postprocessing_tab()
        self.create_sponsorblock_tab()
        self.create_path_tab()
        self.create_classify_rename_tab()
        self.create_ui_tab()
        self.create_easter_eggs_tab()  # 新增彩蛋设置标签页

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.reset_btn = QPushButton("重置为默认值")
        self.reset_btn.setMinimumWidth(140)
        self.reset_btn.clicked.connect(self.reset_settings)

        self.save_btn = QPushButton("💾 保存设置")
        self.save_btn.setMinimumWidth(140)
        self.save_btn.clicked.connect(self.save_settings)

        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setMinimumWidth(140)
        self.cancel_btn.clicked.connect(self.close)

        button_layout.addWidget(self.reset_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.save_btn)
        main_layout.addLayout(button_layout)

    def create_basic_tab(self):
        """创建基础设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)

        # 添加滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # 分辨率设置
        res_group = QGroupBox("📺 视频质量")
        res_layout = QVBoxLayout(res_group)
        res_layout.setSpacing(15)

        res_combo_layout = QHBoxLayout()
        res_label = QLabel("分辨率:")
        res_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        res_combo_layout.addWidget(res_label)
        self.res_combo = QComboBox()
        self.res_combo.addItems(["最高分辨率", "1080p", "720p", "480p", "360p"])
        res_combo_layout.addWidget(self.res_combo, 1)
        res_combo_layout.addStretch()
        res_layout.addLayout(res_combo_layout)

        format_layout = QHBoxLayout()
        format_label = QLabel("输出格式:")
        format_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        format_layout.addWidget(format_label)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["mp4", "mkv", "webm", "flv", "avi", "mov"])
        format_layout.addWidget(self.format_combo, 1)
        format_layout.addStretch()
        res_layout.addLayout(format_layout)

        content_layout.addWidget(res_group)

        # 其他选项
        option_group = QGroupBox("⚙️ 下载选项")
        option_layout = QVBoxLayout(option_group)
        option_layout.setSpacing(12)

        self.cover_check = QCheckBox("嵌入封面")
        self.metadata_check = QCheckBox("嵌入元数据")
        self.skip_check = QCheckBox("跳过已存在文件")

        option_layout.addWidget(self.cover_check)
        option_layout.addWidget(self.metadata_check)
        option_layout.addWidget(self.skip_check)

        content_layout.addWidget(option_group)

        content_layout.addStretch()
        self.tab_widget.addTab(tab, "📱 基础设置")

    def create_audio_video_tab(self):
        """创建音视频设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)

        # 添加滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # 音频提取设置
        audio_group = QGroupBox("🎵 音频提取")
        audio_layout = QVBoxLayout(audio_group)
        audio_layout.setSpacing(15)

        self.extract_audio_check = QCheckBox("仅提取音频 (忽略视频)")
        self.extract_audio_check.stateChanged.connect(self.on_extract_audio_changed)
        audio_layout.addWidget(self.extract_audio_check)

        audio_format_layout = QHBoxLayout()
        format_label = QLabel("音频格式:")
        format_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        audio_format_layout.addWidget(format_label)
        self.audio_format_combo = QComboBox()
        self.audio_format_combo.addItems(["best", "aac", "alac", "flac", "m4a", "mp3", "opus", "vorbis", "wav"])
        audio_format_layout.addWidget(self.audio_format_combo, 1)
        audio_format_layout.addStretch()
        audio_layout.addLayout(audio_format_layout)

        audio_quality_layout = QHBoxLayout()
        quality_label = QLabel("音频质量 (0-10，0为最佳):")
        quality_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        audio_quality_layout.addWidget(quality_label)
        self.audio_quality_spin = QSpinBox()
        self.audio_quality_spin.setRange(0, 10)
        self.audio_quality_spin.setValue(5)
        audio_quality_layout.addWidget(self.audio_quality_spin)
        audio_quality_layout.addStretch()
        audio_layout.addLayout(audio_quality_layout)

        content_layout.addWidget(audio_group)

        # 视频处理设置
        video_proc_group = QGroupBox("🎬 视频处理")
        video_proc_layout = QVBoxLayout(video_proc_group)
        video_proc_layout.setSpacing(15)

        remux_layout = QHBoxLayout()
        remux_label = QLabel("重封装格式:")
        remux_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        remux_layout.addWidget(remux_label)
        self.remux_combo = QComboBox()
        self.remux_combo.addItems(["", "avi", "flv", "gif", "mkv", "mov", "mp4", "webm"])
        self.remux_combo.setEditable(True)
        remux_layout.addWidget(self.remux_combo, 1)
        remux_layout.addWidget(QLabel("(留空则不重封装)"))
        remux_layout.addStretch()
        video_proc_layout.addLayout(remux_layout)

        recode_layout = QHBoxLayout()
        recode_label = QLabel("重新编码格式:")
        recode_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        recode_layout.addWidget(recode_label)
        self.recode_combo = QComboBox()
        self.recode_combo.addItems(["", "avi", "flv", "gif", "mkv", "mov", "mp4", "webm"])
        self.recode_combo.setEditable(True)
        recode_layout.addWidget(self.recode_combo, 1)
        recode_layout.addWidget(QLabel("(留空则不重新编码)"))
        recode_layout.addStretch()
        video_proc_layout.addLayout(recode_layout)

        content_layout.addWidget(video_proc_group)

        content_layout.addStretch()
        self.tab_widget.addTab(tab, "🎵 音视频设置")

    def on_extract_audio_changed(self, state):
        """音频提取选项变化处理"""
        enabled = state == Qt.Checked
        self.audio_format_combo.setEnabled(enabled)
        self.audio_quality_spin.setEnabled(enabled)

    def create_network_tab(self):
        """创建网络设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)

        # 添加滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # 连接设置
        conn_group = QGroupBox("🌐 连接设置")
        conn_layout = QGridLayout(conn_group)
        conn_layout.setHorizontalSpacing(20)
        conn_layout.setVerticalSpacing(15)

        # 证书验证
        self.cert_check = QCheckBox("不检查SSL证书")
        conn_layout.addWidget(self.cert_check, 0, 0)

        # 警告设置
        self.warn_check = QCheckBox("隐藏警告信息")
        conn_layout.addWidget(self.warn_check, 0, 1)

        # 代理设置
        proxy_label = QLabel("代理服务器:")
        proxy_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        conn_layout.addWidget(proxy_label, 1, 0)
        self.proxy_edit = QLineEdit()
        self.proxy_edit.setPlaceholderText("例如: http://proxy.example.com:8080")
        conn_layout.addWidget(self.proxy_edit, 1, 1)

        # 源地址
        source_label = QLabel("源地址:")
        source_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        conn_layout.addWidget(source_label, 2, 0)
        self.source_addr_edit = QLineEdit()
        self.source_addr_edit.setPlaceholderText("绑定到指定的本地IP地址")
        conn_layout.addWidget(self.source_addr_edit, 2, 1)

        # 伪装头部
        impersonate_label = QLabel("伪装浏览器:")
        impersonate_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        conn_layout.addWidget(impersonate_label, 3, 0)
        self.impersonate_edit = QComboBox()
        self.impersonate_edit.addItems(["", "chrome", "firefox", "safari", "edge"])
        self.impersonate_edit.setEditable(True)
        conn_layout.addWidget(self.impersonate_edit, 3, 1)

        # IP版本强制
        ip_layout = QHBoxLayout()
        self.ipv4_check = QCheckBox("强制IPv4")
        self.ipv6_check = QCheckBox("强制IPv6")
        ip_layout.addWidget(self.ipv4_check)
        ip_layout.addWidget(self.ipv6_check)
        ip_layout.addStretch()
        conn_layout.addLayout(ip_layout, 4, 0, 1, 2)

        content_layout.addWidget(conn_group)

        # 重试和超时设置
        retry_group = QGroupBox("🔄 重试与超时设置")
        retry_layout = QGridLayout(retry_group)
        retry_layout.setHorizontalSpacing(20)
        retry_layout.setVerticalSpacing(15)

        # 重试次数
        retry_label = QLabel("重试次数:")
        retry_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        retry_layout.addWidget(retry_label, 0, 0)
        self.retry_spin = QSpinBox()
        self.retry_spin.setRange(0, 99)
        self.retry_spin.setSpecialValueText("无限")
        retry_layout.addWidget(self.retry_spin, 0, 1)

        # 片段重试
        fragment_label = QLabel("片段重试次数:")
        fragment_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        retry_layout.addWidget(fragment_label, 1, 0)
        self.fragment_retry_spin = QSpinBox()
        self.fragment_retry_spin.setRange(0, 99)
        self.fragment_retry_spin.setSpecialValueText("无限")
        retry_layout.addWidget(self.fragment_retry_spin, 1, 1)

        # 超时设置
        timeout_label = QLabel("超时时间(秒):")
        timeout_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        retry_layout.addWidget(timeout_label, 2, 0)
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(10, 600)
        retry_layout.addWidget(self.timeout_spin, 2, 1)

        # Socket超时
        socket_label = QLabel("Socket超时(秒):")
        socket_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        retry_layout.addWidget(socket_label, 3, 0)
        self.socket_timeout_spin = QSpinBox()
        self.socket_timeout_spin.setRange(10, 600)
        retry_layout.addWidget(self.socket_timeout_spin, 3, 1)

        # 并发片段
        concurrent_label = QLabel("并发片段数:")
        concurrent_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        retry_layout.addWidget(concurrent_label, 4, 0)
        self.concurrent_spin = QSpinBox()
        self.concurrent_spin.setRange(1, 20)
        retry_layout.addWidget(self.concurrent_spin, 4, 1)

        # 提取器重试
        extractor_label = QLabel("提取器重试次数:")
        extractor_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        retry_layout.addWidget(extractor_label, 5, 0)
        self.extractor_retry_spin = QSpinBox()
        self.extractor_retry_spin.setRange(0, 99)
        self.extractor_retry_spin.setSpecialValueText("无限")
        retry_layout.addWidget(self.extractor_retry_spin, 5, 1)

        content_layout.addWidget(retry_group)

        # 速率限制
        rate_group = QGroupBox("🚦 速率限制")
        rate_layout = QGridLayout(rate_group)
        rate_layout.setHorizontalSpacing(20)
        rate_layout.setVerticalSpacing(15)

        # 限速
        limit_label = QLabel("下载限速:")
        limit_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        rate_layout.addWidget(limit_label, 0, 0)
        self.rate_limit_edit = QLineEdit()
        self.rate_limit_edit.setPlaceholderText("例如: 50k 或 2.5M")
        rate_layout.addWidget(self.rate_limit_edit, 0, 1)

        # 节流速率
        throttle_label = QLabel("节流速率:")
        throttle_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        rate_layout.addWidget(throttle_label, 1, 0)
        self.throttled_edit = QLineEdit()
        self.throttled_edit.setPlaceholderText("低于此速率时取消下载")
        rate_layout.addWidget(self.throttled_edit, 1, 1)

        content_layout.addWidget(rate_group)

        # 高级网络选项
        advanced_group = QGroupBox("🔧 高级网络选项")
        advanced_layout = QVBoxLayout(advanced_group)
        advanced_layout.setSpacing(12)

        self.dynamic_mpd_check = QCheckBox("允许动态MPD")
        self.hls_split_check = QCheckBox("HLS分割不连续性")

        advanced_layout.addWidget(self.dynamic_mpd_check)
        advanced_layout.addWidget(self.hls_split_check)

        content_layout.addWidget(advanced_group)

        content_layout.addStretch()
        self.tab_widget.addTab(tab, "🌐 网络设置")

    def create_batch_tab(self):
        """创建批量下载设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)

        # 添加滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # 批量设置
        batch_group = QGroupBox("📚 播放列表设置")
        batch_layout = QVBoxLayout(batch_group)
        batch_layout.setSpacing(15)

        self.batch_check = QCheckBox("自动识别播放列表（下载UP主/番剧所有视频）")

        playlist_items_layout = QHBoxLayout()
        items_label = QLabel("播放列表项:")
        items_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        playlist_items_layout.addWidget(items_label)
        self.playlist_items_edit = QLineEdit()
        self.playlist_items_edit.setPlaceholderText("例如: 1:3,7,-5::2 (下载指定序号的视频)")
        playlist_items_layout.addWidget(self.playlist_items_edit, 1)
        playlist_items_layout.addStretch()

        max_downloads_layout = QHBoxLayout()
        max_label = QLabel("最大下载数量:")
        max_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        max_downloads_layout.addWidget(max_label)
        self.max_downloads_spin = QSpinBox()
        self.max_downloads_spin.setRange(1, 10000)
        self.max_downloads_spin.setSpecialValueText("无限制")
        max_downloads_layout.addWidget(self.max_downloads_spin)
        max_downloads_layout.addStretch()

        options_layout = QHBoxLayout()
        self.playlist_random_check = QCheckBox("随机下载播放列表")
        self.lazy_playlist_check = QCheckBox("延迟处理播放列表")
        options_layout.addWidget(self.playlist_random_check)
        options_layout.addWidget(self.lazy_playlist_check)
        options_layout.addStretch()

        batch_layout.addWidget(self.batch_check)
        batch_layout.addLayout(playlist_items_layout)
        batch_layout.addLayout(max_downloads_layout)
        batch_layout.addLayout(options_layout)

        content_layout.addWidget(batch_group)

        content_layout.addStretch()
        self.tab_widget.addTab(tab, "📚 批量设置")

    def create_selection_tab(self):
        """创建视频选择设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)

        # 添加滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # 文件大小设置
        size_group = QGroupBox("📊 文件大小过滤")
        size_layout = QVBoxLayout(size_group)
        size_layout.setSpacing(15)

        min_size_layout = QHBoxLayout()
        min_label = QLabel("最小文件大小:")
        min_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        min_size_layout.addWidget(min_label)
        self.min_filesize_edit = QLineEdit()
        self.min_filesize_edit.setPlaceholderText("例如: 50k 或 44.6M (留空则无限制)")
        min_size_layout.addWidget(self.min_filesize_edit, 1)
        min_size_layout.addStretch()

        max_size_layout = QHBoxLayout()
        max_label = QLabel("最大文件大小:")
        max_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        max_size_layout.addWidget(max_label)
        self.max_filesize_edit = QLineEdit()
        self.max_filesize_edit.setPlaceholderText("例如: 50k 或 44.6M (留空则无限制)")
        max_size_layout.addWidget(self.max_filesize_edit, 1)
        max_size_layout.addStretch()

        size_layout.addLayout(min_size_layout)
        size_layout.addLayout(max_size_layout)
        content_layout.addWidget(size_group)

        # 日期设置
        date_group = QGroupBox("📅 上传日期过滤")
        date_layout = QVBoxLayout(date_group)
        date_layout.setSpacing(15)

        format_label = QLabel("格式: YYYYMMDD 或 now|today|yesterday[-N[day|week|month|year]]")
        format_label.setStyleSheet("font-size: 10pt; color: #666; font-style: italic;")
        date_layout.addWidget(format_label)

        date_label = QLabel("指定日期:")
        date_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        date_layout.addWidget(date_label)
        self.date_edit = QLineEdit()
        self.date_edit.setPlaceholderText("例如: 20231225 或 today-2weeks")
        date_layout.addWidget(self.date_edit)

        date_before_layout = QHBoxLayout()
        before_label = QLabel("不晚于:")
        before_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        date_before_layout.addWidget(before_label)
        self.datebefore_edit = QLineEdit()
        self.datebefore_edit.setPlaceholderText("例如: 20231225")
        date_before_layout.addWidget(self.datebefore_edit, 1)
        date_before_layout.addStretch()
        date_layout.addLayout(date_before_layout)

        date_after_layout = QHBoxLayout()
        after_label = QLabel("不早于:")
        after_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        date_after_layout.addWidget(after_label)
        self.dateafter_edit = QLineEdit()
        self.dateafter_edit.setPlaceholderText("例如: 20231201")
        date_after_layout.addWidget(self.dateafter_edit, 1)
        date_after_layout.addStretch()
        date_layout.addLayout(date_after_layout)

        content_layout.addWidget(date_group)

        # 其他过滤条件
        filter_group = QGroupBox("🎯 其他过滤条件")
        filter_layout = QVBoxLayout(filter_group)
        filter_layout.setSpacing(15)

        age_limit_layout = QHBoxLayout()
        age_label = QLabel("年龄限制:")
        age_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        age_limit_layout.addWidget(age_label)
        self.age_limit_spin = QSpinBox()
        self.age_limit_spin.setRange(0, 18)
        self.age_limit_spin.setSpecialValueText("无限制")
        age_limit_layout.addWidget(self.age_limit_spin)
        age_limit_layout.addStretch()
        filter_layout.addLayout(age_limit_layout)

        filter_label = QLabel("匹配过滤器:")
        filter_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        filter_layout.addWidget(filter_label)
        self.match_filters_edit = QLineEdit()
        self.match_filters_edit.setPlaceholderText('例如: "like_count>?100 & description~=\'(?i)cats\'"')
        filter_layout.addWidget(self.match_filters_edit)

        archive_layout = QHBoxLayout()
        archive_label = QLabel("下载存档文件:")
        archive_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        archive_layout.addWidget(archive_label)
        self.download_archive_edit = DragDropLineEdit("选择存档文件（仅下载不在存档中的视频）", is_file=True)
        archive_layout.addWidget(self.download_archive_edit, 1)
        browse_archive_btn = QPushButton("浏览")
        browse_archive_btn.clicked.connect(self.browse_archive_file)
        archive_layout.addWidget(browse_archive_btn)
        filter_layout.addLayout(archive_layout)

        content_layout.addWidget(filter_group)

        content_layout.addStretch()
        self.tab_widget.addTab(tab, "🎯 视频选择")

    def browse_archive_file(self):
        """浏览存档文件"""
        path, _ = QFileDialog.getOpenFileName(
            self, "选择下载存档文件", "",
            "文本文件 (*.txt);;所有文件 (*.*)"
        )
        if path:
            self.download_archive_edit.setText(path)

    def create_subtitles_tab(self):
        """创建字幕设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)

        # 添加滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # 字幕下载设置
        subs_group = QGroupBox("📝 字幕下载")
        subs_layout = QVBoxLayout(subs_group)
        subs_layout.setSpacing(15)

        self.write_subs_check = QCheckBox("下载字幕")
        self.write_auto_subs_check = QCheckBox("下载自动生成的字幕")

        sub_format_layout = QHBoxLayout()
        format_label = QLabel("字幕格式:")
        format_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        sub_format_layout.addWidget(format_label)
        self.sub_format_combo = QComboBox()
        self.sub_format_combo.addItems(["best", "srt", "ass", "vtt", "lrc"])
        self.sub_format_combo.setEditable(True)
        sub_format_layout.addWidget(self.sub_format_combo, 1)
        sub_format_layout.addStretch()

        sub_langs_layout = QHBoxLayout()
        langs_label = QLabel("字幕语言:")
        langs_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        sub_langs_layout.addWidget(langs_label)
        self.sub_langs_edit = QLineEdit()
        self.sub_langs_edit.setPlaceholderText('例如: "en,ja" 或 "all,-live_chat"')
        sub_langs_layout.addWidget(self.sub_langs_edit, 1)
        sub_langs_layout.addStretch()

        subs_layout.addWidget(self.write_subs_check)
        subs_layout.addWidget(self.write_auto_subs_check)
        subs_layout.addLayout(sub_format_layout)
        subs_layout.addLayout(sub_langs_layout)
        content_layout.addWidget(subs_group)

        # 字幕处理设置
        subs_proc_group = QGroupBox("🔧 字幕处理")
        subs_proc_layout = QVBoxLayout(subs_proc_group)
        subs_proc_layout.setSpacing(15)

        self.embed_subs_check = QCheckBox("嵌入字幕到视频中")

        convert_subs_layout = QHBoxLayout()
        convert_label = QLabel("转换字幕格式:")
        convert_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        convert_subs_layout.addWidget(convert_label)
        self.convert_subs_combo = QComboBox()
        self.convert_subs_combo.addItems(["none", "srt", "ass", "vtt", "lrc"])
        convert_subs_layout.addWidget(self.convert_subs_combo, 1)
        convert_subs_layout.addStretch()

        subs_proc_layout.addWidget(self.embed_subs_check)
        subs_proc_layout.addLayout(convert_subs_layout)
        content_layout.addWidget(subs_proc_group)

        content_layout.addStretch()
        self.tab_widget.addTab(tab, "📝 字幕设置")

    def create_postprocessing_tab(self):
        """创建后处理设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)

        # 添加滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # 基本后处理
        basic_proc_group = QGroupBox("🔧 基本后处理")
        basic_proc_layout = QVBoxLayout(basic_proc_group)
        basic_proc_layout.setSpacing(15)

        self.keep_video_check = QCheckBox("保留原始视频文件（提取音频后）")
        self.post_overwrites_check = QCheckBox("覆盖后处理文件")
        self.embed_chapters_check = QCheckBox("嵌入章节标记")
        self.embed_info_json_check = QCheckBox("嵌入元数据JSON文件")

        fixup_layout = QHBoxLayout()
        fixup_label = QLabel("自动修复策略:")
        fixup_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        fixup_layout.addWidget(fixup_label)
        self.fixup_combo = QComboBox()
        self.fixup_combo.addItems(["detect_or_warn", "never", "warn", "force"])
        fixup_layout.addWidget(self.fixup_combo, 1)
        fixup_layout.addStretch()

        basic_proc_layout.addWidget(self.keep_video_check)
        basic_proc_layout.addWidget(self.post_overwrites_check)
        basic_proc_layout.addWidget(self.embed_chapters_check)
        basic_proc_layout.addWidget(self.embed_info_json_check)
        basic_proc_layout.addLayout(fixup_layout)
        content_layout.addWidget(basic_proc_group)

        # 章节处理
        chapter_group = QGroupBox("📖 章节处理")
        chapter_layout = QVBoxLayout(chapter_group)
        chapter_layout.setSpacing(15)

        self.split_chapters_check = QCheckBox("按章节分割视频")
        self.force_keyframes_check = QCheckBox("在切割处强制关键帧（可能需要重新编码）")

        remove_chapters_layout = QHBoxLayout()
        remove_label = QLabel("移除章节:")
        remove_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        remove_chapters_layout.addWidget(remove_label)
        self.remove_chapters_edit = QLineEdit()
        self.remove_chapters_edit.setPlaceholderText('例如: "*10:15" 或 "intro,outro"')
        remove_chapters_layout.addWidget(self.remove_chapters_edit, 1)
        remove_chapters_layout.addStretch()

        chapter_layout.addWidget(self.split_chapters_check)
        chapter_layout.addWidget(self.force_keyframes_check)
        chapter_layout.addLayout(remove_chapters_layout)
        content_layout.addWidget(chapter_group)

        # 播放列表合并
        concat_group = QGroupBox("🔗 播放列表合并")
        concat_layout = QVBoxLayout(concat_group)
        concat_layout.setSpacing(15)

        concat_label = QLabel("合并策略:")
        concat_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        concat_layout.addWidget(concat_label)
        self.concat_combo = QComboBox()
        self.concat_combo.addItems(["multi_video", "never", "always"])
        concat_layout.addWidget(self.concat_combo)

        note_label = QLabel("注意：只有相同编码和流数量的视频才能合并")
        note_label.setStyleSheet("font-size: 10pt; color: #f39c12; font-weight: 500;")
        concat_layout.addWidget(note_label)

        content_layout.addWidget(concat_group)

        # 执行命令
        exec_group = QGroupBox("⚡ 下载后执行命令")
        exec_layout = QVBoxLayout(exec_group)
        exec_layout.setSpacing(15)

        self.exec_edit = QLineEdit()
        self.exec_edit.setPlaceholderText('例如: "notepad.exe %(filepath)s" (支持输出模板变量)')
        exec_layout.addWidget(self.exec_edit)

        vars_label = QLabel('可用变量: %(title)s, %(uploader)s, %(filepath)s 等（与文件名模板相同）')
        vars_label.setStyleSheet("font-size: 10pt; color: #666; font-style: italic;")
        exec_layout.addWidget(vars_label)

        content_layout.addWidget(exec_group)

        content_layout.addStretch()
        self.tab_widget.addTab(tab, "🔧 后处理设置")

    def create_sponsorblock_tab(self):
        """创建SponsorBlock设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)

        # 添加滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # SponsorBlock设置
        sb_group = QGroupBox("🎯 SponsorBlock设置（仅YouTube）")
        sb_layout = QVBoxLayout(sb_group)
        sb_layout.setSpacing(15)

        categories_label = QLabel(
            "可用类别: sponsor, intro, outro, selfpromo, preview, filler, interaction, music_offtopic, hook, poi_highlight, chapter")
        categories_label.setStyleSheet("font-size: 10pt; color: #666; font-style: italic;")
        sb_layout.addWidget(categories_label)

        sb_mark_layout = QHBoxLayout()
        mark_label = QLabel("标记为章节:")
        mark_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        sb_mark_layout.addWidget(mark_label)
        self.sb_mark_edit = QLineEdit()
        self.sb_mark_edit.setPlaceholderText('例如: "all,-preview" 或 "sponsor,intro"')
        sb_mark_layout.addWidget(self.sb_mark_edit, 1)
        sb_mark_layout.addStretch()

        sb_remove_layout = QHBoxLayout()
        remove_label = QLabel("从视频中移除:")
        remove_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        sb_remove_layout.addWidget(remove_label)
        self.sb_remove_edit = QLineEdit()
        self.sb_remove_edit.setPlaceholderText('例如: "default" 或 "sponsor,intro"')
        sb_remove_layout.addWidget(self.sb_remove_edit, 1)
        sb_remove_layout.addStretch()

        sb_title_layout = QHBoxLayout()
        title_label = QLabel("章节标题模板:")
        title_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        sb_title_layout.addWidget(title_label)
        self.sb_title_edit = QLineEdit()
        self.sb_title_edit.setPlaceholderText('例如: "[%(category_names)s] %(start_time)s"')
        sb_title_layout.addWidget(self.sb_title_edit, 1)
        sb_title_layout.addStretch()

        sb_api_layout = QHBoxLayout()
        api_label = QLabel("API地址:")
        api_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        sb_api_layout.addWidget(api_label)
        self.sb_api_edit = QLineEdit()
        self.sb_api_edit.setPlaceholderText("SponsorBlock API地址")
        sb_api_layout.addWidget(self.sb_api_edit, 1)
        sb_api_layout.addStretch()

        sb_layout.addLayout(sb_mark_layout)
        sb_layout.addLayout(sb_remove_layout)
        sb_layout.addLayout(sb_title_layout)
        sb_layout.addLayout(sb_api_layout)
        content_layout.addWidget(sb_group)

        content_layout.addStretch()
        self.tab_widget.addTab(tab, "🎯 SponsorBlock")

    def create_path_tab(self):
        """创建路径设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)

        # 添加滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # 下载路径
        download_group = QGroupBox("📁 下载路径")
        download_layout = QVBoxLayout(download_group)
        download_layout.setSpacing(15)

        self.download_edit = DragDropLineEdit("请选择或拖入文件夹", is_file=False)
        download_layout.addWidget(self.download_edit)

        browse_btn = QPushButton("📂 浏览文件夹")
        browse_btn.clicked.connect(self.browse_download_path)
        download_layout.addWidget(browse_btn)

        content_layout.addWidget(download_group)

        # 工具路径
        tools_group = QGroupBox("🔧 工具路径")
        tools_layout = QVBoxLayout(tools_group)
        tools_layout.setSpacing(15)

        self.ffmpeg_edit = DragDropLineEdit("ffmpeg可执行文件路径（留空则自动检测）", is_file=True)
        tools_layout.addWidget(self.ffmpeg_edit)

        ffmpeg_btn_layout = QHBoxLayout()
        browse_ffmpeg_btn = QPushButton("📂 浏览ffmpeg")
        browse_ffmpeg_btn.clicked.connect(self.browse_ffmpeg_file)

        clear_ffmpeg_btn = QPushButton("🗑️ 清除")
        clear_ffmpeg_btn.clicked.connect(lambda: self.ffmpeg_edit.clear())

        ffmpeg_btn_layout.addWidget(browse_ffmpeg_btn)
        ffmpeg_btn_layout.addWidget(clear_ffmpeg_btn)
        ffmpeg_btn_layout.addStretch()
        tools_layout.addLayout(ffmpeg_btn_layout)

        content_layout.addWidget(tools_group)

        # Cookie和缓存
        misc_group = QGroupBox("🍪 Cookie和缓存")
        misc_layout = QVBoxLayout(misc_group)
        misc_layout.setSpacing(15)

        self.cookie_edit = DragDropLineEdit("请选择或拖入Cookie文件（可选）", is_file=True)
        misc_layout.addWidget(self.cookie_edit)

        cookie_btn_layout = QHBoxLayout()
        browse_cookie_btn = QPushButton("📂 浏览Cookie文件")
        browse_cookie_btn.clicked.connect(self.browse_cookie_file)

        clear_cookie_btn = QPushButton("🗑️ 清除")
        clear_cookie_btn.clicked.connect(lambda: self.cookie_edit.clear())

        cookie_btn_layout.addWidget(browse_cookie_btn)
        cookie_btn_layout.addWidget(clear_cookie_btn)
        cookie_btn_layout.addStretch()
        misc_layout.addLayout(cookie_btn_layout)

        cache_layout = QHBoxLayout()
        cache_label = QLabel("缓存目录:")
        cache_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        cache_layout.addWidget(cache_label)
        self.cache_dir_edit = DragDropLineEdit("缓存文件保存目录（留空则禁用缓存）", is_file=False)
        cache_layout.addWidget(self.cache_dir_edit, 1)
        browse_cache_btn = QPushButton("📂 浏览")
        browse_cache_btn.clicked.connect(self.browse_cache_dir)
        cache_layout.addWidget(browse_cache_btn)
        misc_layout.addLayout(cache_layout)

        content_layout.addWidget(misc_group)

        # 其他选项
        self.auto_open_check = QCheckBox("下载完成后自动打开文件夹")
        content_layout.addWidget(self.auto_open_check)

        content_layout.addStretch()
        self.tab_widget.addTab(tab, "📁 路径设置")

    def browse_download_path(self):
        """浏览下载路径"""
        current_path = self.download_edit.text().strip()
        if not os.path.exists(current_path):
            current_path = os.path.expanduser("~/Downloads")

        path = QFileDialog.getExistingDirectory(self, "选择下载文件夹", current_path)
        if path:
            self.download_edit.setText(path)
            self.update_preview()

    def browse_cookie_file(self):
        """浏览Cookie文件"""
        path, _ = QFileDialog.getOpenFileName(
            self, "选择Cookie文件", "",
            "Cookie文件 (*.txt *.sqlite *.json);;所有文件 (*.*)"
        )
        if path:
            self.cookie_edit.setText(path)

    def browse_ffmpeg_file(self):
        """浏览ffmpeg文件"""
        path, _ = QFileDialog.getOpenFileName(
            self, "选择ffmpeg可执行文件", "",
            "可执行文件 (*.exe);;所有文件 (*.*)"
        )
        if path:
            self.ffmpeg_edit.setText(path)

    def browse_cache_dir(self):
        """浏览缓存目录"""
        current_path = self.cache_dir_edit.text().strip()
        if not os.path.exists(current_path):
            current_path = os.path.expanduser("~/Downloads")

        path = QFileDialog.getExistingDirectory(self, "选择缓存目录", current_path)
        if path:
            self.cache_dir_edit.setText(path)

    def create_classify_rename_tab(self):
        """创建分类与重命名标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)

        # 添加滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # 分类设置
        classify_group = QGroupBox("🗂️ 自动分类")
        classify_layout = QVBoxLayout(classify_group)
        classify_layout.setSpacing(15)

        classify_rule_layout = QHBoxLayout()
        rule_label = QLabel("分类规则:")
        rule_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        classify_rule_layout.addWidget(rule_label)
        self.classify_combo = QComboBox()
        self.classify_combo.addItems(["不分类", "按平台", "按作者", "按番剧", "按日期"])
        self.classify_combo.currentTextChanged.connect(self.on_classify_changed)
        classify_rule_layout.addWidget(self.classify_combo, 1)
        classify_rule_layout.addStretch()
        classify_layout.addLayout(classify_rule_layout)

        # 日期格式
        self.date_format_widget = QWidget()
        self.date_format_layout = QHBoxLayout(self.date_format_widget)
        date_label = QLabel("日期格式:")
        date_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        self.date_format_layout.addWidget(date_label)
        self.date_combo = QComboBox()
        self.date_combo.addItems(["YYYY/MM/DD", "YYYY-MM-DD", "YYYY年MM月DD日", "YYYY/MM", "YYYY"])
        self.date_combo.currentTextChanged.connect(self.update_preview)
        self.date_format_layout.addWidget(self.date_combo, 1)
        self.date_format_layout.addStretch()
        self.date_format_widget.setVisible(False)
        classify_layout.addWidget(self.date_format_widget)

        content_layout.addWidget(classify_group)

        # 智能重命名设置
        smart_rename_group = QGroupBox("🤖 智能重命名")
        smart_rename_layout = QVBoxLayout(smart_rename_group)
        smart_rename_layout.setSpacing(15)

        # 启用智能重命名
        self.smart_rename_check = QCheckBox("启用智能重命名")
        self.smart_rename_check.stateChanged.connect(self.on_smart_rename_changed)
        smart_rename_layout.addWidget(self.smart_rename_check)

        # 重命名策略
        strategy_layout = QHBoxLayout()
        strategy_label = QLabel("重命名策略:")
        strategy_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        strategy_layout.addWidget(strategy_label)
        self.strategy_combo = QComboBox()
        self.strategy_combo.addItems([
            "auto - 自动选择最佳方案",
            "smart - 智能提取关键词",
            "title - 仅使用原标题",
            "combined - 组合信息 (上传者 - 标题)",
            "compact - 紧凑命名",
            "template - 使用自定义模板"
        ])
        self.strategy_combo.currentTextChanged.connect(self.update_preview)
        strategy_layout.addWidget(self.strategy_combo, 1)
        strategy_layout.addStretch()
        smart_rename_layout.addLayout(strategy_layout)

        # 高级选项
        advanced_options = QGroupBox("⚙️ 智能重命名高级选项")
        advanced_layout = QVBoxLayout(advanced_options)
        advanced_layout.setSpacing(10)

        min_length_layout = QHBoxLayout()
        min_label = QLabel("有意义最小长度:")
        min_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        min_length_layout.addWidget(min_label)
        self.min_length_spin = QSpinBox()
        self.min_length_spin.setRange(5, 50)
        self.min_length_spin.setValue(10)
        self.min_length_spin.valueChanged.connect(self.update_preview)
        min_length_layout.addWidget(self.min_length_spin)
        min_length_layout.addStretch()
        advanced_layout.addLayout(min_length_layout)

        self.keep_original_check = QCheckBox("原文件名有意义时保留")
        self.keep_original_check.stateChanged.connect(self.update_preview)
        self.uploader_fallback_check = QCheckBox("使用上传者作为备选")
        self.include_res_check = QCheckBox("包含分辨率")
        self.include_date_check = QCheckBox("包含上传日期")

        advanced_layout.addWidget(self.keep_original_check)
        advanced_layout.addWidget(self.uploader_fallback_check)
        advanced_layout.addWidget(self.include_res_check)
        advanced_layout.addWidget(self.include_date_check)

        smart_rename_layout.addWidget(advanced_options)
        content_layout.addWidget(smart_rename_group)

        # 传统重命名设置（当智能重名禁用时显示）
        self.traditional_rename_group = QGroupBox("✏️ 文件重命名（传统）")
        traditional_rename_layout = QVBoxLayout(self.traditional_rename_group)
        traditional_rename_layout.setSpacing(15)

        # 模板选择
        template_layout = QHBoxLayout()
        template_label = QLabel("文件名模板:")
        template_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        template_layout.addWidget(template_label)
        self.template_combo = QComboBox()
        self.template_combo.addItems([
            "%(title)s",
            "%(title)s - %(resolution)s",
            "%(title)s - %(uploader)s",
            "%(uploader)s - %(title)s",
            "%(title)s [%(upload_date)s]",
            "%(playlist_title)s/%(playlist_index)s - %(title)s"
        ])
        self.template_combo.setEditable(True)
        self.template_combo.currentTextChanged.connect(self.update_preview)
        template_layout.addWidget(self.template_combo, 1)
        template_layout.addStretch()
        traditional_rename_layout.addLayout(template_layout)

        # 可用变量提示
        vars_label = QLabel(
            "可用变量: %(title)s, %(uploader)s, %(extractor)s, %(resolution)s, %(upload_date)s, %(id)s, %(playlist_title)s, %(playlist_index)s")
        vars_label.setStyleSheet(
            "color: #666; font-size: 9pt; font-style: italic; background-color: #f8f9fa; padding: 6px; border-radius: 4px;")
        traditional_rename_layout.addWidget(vars_label)

        # 文件名长度限制
        length_layout = QHBoxLayout()
        length_label = QLabel("最大文件名长度:")
        length_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        length_layout.addWidget(length_label)
        self.length_spin = QSpinBox()
        self.length_spin.setRange(0, 255)
        self.length_spin.setSpecialValueText("无限制")
        self.length_spin.setValue(100)
        self.length_spin.valueChanged.connect(self.update_preview)
        length_layout.addWidget(self.length_spin)
        length_layout.addStretch()
        traditional_rename_layout.addLayout(length_layout)

        # 其他选项
        self.replace_check = QCheckBox("自动替换非法字符（\\/*?:\"<>|）")
        self.replace_check.stateChanged.connect(self.update_preview)
        self.windows_check = QCheckBox("强制Windows兼容文件名")

        traditional_rename_layout.addWidget(self.replace_check)
        traditional_rename_layout.addWidget(self.windows_check)

        content_layout.addWidget(self.traditional_rename_group)

        # 预览
        preview_group = QGroupBox("👁️ 预览")
        preview_layout = QVBoxLayout(preview_group)
        self.preview_label = QLabel("示例路径将在此显示...")
        self.preview_label.setWordWrap(True)
        self.preview_label.setStyleSheet("""
            QLabel {
                color: #333;
                padding: 16px;
                background: linear-gradient(135deg, #f8fafc 0%, #e3e9f1 100%);
                border-radius: 8px;
                border: 2px solid #e1e8ed;
                font-family: 'Consolas', monospace;
                font-size: 11pt;
                min-height: 70px;
            }
        """)
        preview_layout.addWidget(self.preview_label)
        content_layout.addWidget(preview_group)

        content_layout.addStretch()
        self.tab_widget.addTab(tab, "✏️ 分类与重命名")

    def create_ui_tab(self):
        """创建界面设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)

        # 添加滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # 界面设置
        ui_group = QGroupBox("🎨 界面设置")
        ui_layout = QVBoxLayout(ui_group)
        ui_layout.setSpacing(15)

        theme_layout = QHBoxLayout()
        theme_label = QLabel("主题:")
        theme_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        theme_layout.addWidget(theme_label)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["light", "dark"])
        theme_layout.addWidget(self.theme_combo, 1)
        theme_layout.addStretch()
        ui_layout.addLayout(theme_layout)

        font_layout = QHBoxLayout()
        font_label = QLabel("字体大小:")
        font_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        font_layout.addWidget(font_label)
        self.font_spin = QSpinBox()
        self.font_spin.setRange(8, 16)
        self.font_spin.setValue(10)
        font_layout.addWidget(self.font_spin)
        font_layout.addStretch()
        ui_layout.addLayout(font_layout)

        window_layout = QHBoxLayout()
        width_label = QLabel("窗口宽度:")
        width_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        window_layout.addWidget(width_label)
        self.width_spin = QSpinBox()
        self.width_spin.setRange(800, 2000)
        self.width_spin.setValue(1200)
        window_layout.addWidget(self.width_spin)

        height_label = QLabel("窗口高度:")
        height_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        window_layout.addWidget(height_label)
        self.height_spin = QSpinBox()
        self.height_spin.setRange(600, 1500)
        self.height_spin.setValue(800)
        window_layout.addWidget(self.height_spin)
        window_layout.addStretch()
        ui_layout.addLayout(window_layout)

        self.show_advanced_check = QCheckBox("默认显示高级选项")
        ui_layout.addWidget(self.show_advanced_check)

        content_layout.addWidget(ui_group)

        content_layout.addStretch()
        self.tab_widget.addTab(tab, "🎨 界面设置")

    def create_easter_eggs_tab(self):
        """创建彩蛋设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)

        # 添加滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # 彩蛋设置
        egg_group = QGroupBox("🥚 彩蛋设置")
        egg_layout = QVBoxLayout(egg_group)
        egg_layout.setSpacing(15)

        # 彩蛋说明
        description = QLabel("这些是趣味功能，不影响主要下载功能。\n启用它们可以让下载过程更有趣！")
        description.setStyleSheet("color: #666; font-size: 10pt; padding: 10px;")
        description.setWordWrap(True)
        egg_layout.addWidget(description)

        # 彩蛋选项
        self.funny_messages_check = QCheckBox("启用趣味消息")
        self.secret_logos_check = QCheckBox("启用节日特别图标")
        self.hidden_features_check = QCheckBox("启用隐藏功能")
        self.secret_codes_check = QCheckBox("启用秘密按键序列检测")

        egg_layout.addWidget(self.funny_messages_check)
        egg_layout.addWidget(self.secret_logos_check)
        egg_layout.addWidget(self.hidden_features_check)
        egg_layout.addWidget(self.secret_codes_check)

        # 彩蛋提示
        tip_label = QLabel("💡 提示：在设置窗口尝试输入某些经典游戏秘籍...")
        tip_label.setStyleSheet("color: #888; font-size: 9pt; font-style: italic; padding: 10px;")
        egg_layout.addWidget(tip_label)

        content_layout.addWidget(egg_group)

        # 开发者彩蛋
        if EasterEggs.hidden_feature_enabled():
            dev_group = QGroupBox("🔧 开发者模式")
            dev_layout = QVBoxLayout(dev_group)
            dev_layout.setSpacing(15)

            dev_label = QLabel("🎉 今天是幸运日！开发者模式已解锁！")
            dev_label.setStyleSheet("color: #e74c3c; font-weight: bold; font-size: 11pt;")
            dev_layout.addWidget(dev_label)

            # 隐藏的开发者选项
            self.debug_mode_check = QCheckBox("调试模式")
            self.verbose_logging_check = QCheckBox("详细日志记录")

            dev_layout.addWidget(self.debug_mode_check)
            dev_layout.addWidget(self.verbose_logging_check)

            content_layout.addWidget(dev_group)

        content_layout.addStretch()
        self.tab_widget.addTab(tab, "🥚 彩蛋设置")

    def on_smart_rename_changed(self, state):
        """智能重命名选项变化处理"""
        enabled = state == Qt.Checked
        # 显示/隐藏传统重命名设置
        self.traditional_rename_group.setVisible(not enabled)

        # 启用/禁用智能重命名相关控件
        self.strategy_combo.setEnabled(enabled)
        self.min_length_spin.setEnabled(enabled)
        self.keep_original_check.setEnabled(enabled)
        self.uploader_fallback_check.setEnabled(enabled)
        self.include_res_check.setEnabled(enabled)
        self.include_date_check.setEnabled(enabled)

        # 更新预览
        self.update_preview()

    def on_classify_changed(self, text):
        """分类规则变化处理"""
        self.date_format_widget.setVisible(text == "按日期")
        self.update_preview()

    def update_preview(self):
        """更新预览"""
        download_path = self.download_edit.text().strip() or "C:/Downloads"
        classify_rule = self.classify_combo.currentText()

        # 创建模拟视频信息
        video_info = {
            'title': '罗小黑2开会！拉片抠细节！影片中的解释性对话',
            'uploader': '电影解说员小明',
            'extractor': 'Bilibili',
            'height': 1080,
            'upload_date': '20231220',
            'id': 'BV1YQSEBPEyD',
            'playlist_title': '电影解析系列',
            'playlist_index': 5,
            'duration': 1254
        }

        # 创建智能重命名器
        renamer = SmartRenamer(self.config)

        # 获取原文件名（模拟无意义文件名）
        original_filename = "2-1920x1080" if random.random() > 0.5 else "vid_123456789"

        # 构建文件名
        if self.smart_rename_check.isChecked():
            # 智能重命名
            filename = renamer.build_smart_filename(video_info, original_filename)
        else:
            # 传统模板重命名
            filename = renamer.build_template_filename(video_info)

        # 清理文件名
        filename = renamer.clean_filename(filename)

        # 添加扩展名
        filename = f"{filename}.mp4"

        # 生成分类文件夹
        classify_folder = ""
        if classify_rule == "按平台":
            classify_folder = "B站"
        elif classify_rule == "按作者":
            classify_folder = "电影解说员小明"
        elif classify_rule == "按番剧":
            classify_folder = "电影解析系列"
        elif classify_rule == "按日期":
            date_format = self.date_combo.currentText()
            classify_folder = date_format.replace("YYYY", "2023").replace("MM", "12").replace("DD", "20")

        # 构建完整路径
        if classify_folder:
            full_path = os.path.join(download_path, classify_folder, filename)
        else:
            full_path = os.path.join(download_path, filename)

        # 更新预览标签
        preview_text = f"📁 示例保存路径:\n{full_path}"

        # 添加策略说明
        if self.smart_rename_check.isChecked():
            strategy = self.strategy_combo.currentText().split(" - ")[0]
            preview_text += f"\n\n🔍 当前策略: {strategy}"
            if original_filename != filename.replace('.mp4', ''):
                preview_text += f"\n📝 原文件名: {original_filename}.mp4"

        self.preview_label.setText(preview_text)

    def load_settings(self):
        """加载设置"""
        try:
            # 基础设置
            self.res_combo.setCurrentText(self.config["Basic"]["resolution"])
            self.format_combo.setCurrentText(self.config["Basic"]["output_format"])
            self.cover_check.setChecked(self.config["Basic"].getboolean("embed_cover"))
            self.metadata_check.setChecked(self.config["Basic"].getboolean("embed_metadata"))
            self.skip_check.setChecked(self.config["Basic"].getboolean("skip_existing"))

            # 音视频设置
            self.extract_audio_check.setChecked(self.config["Basic"].getboolean("extract_audio"))
            self.audio_format_combo.setCurrentText(self.config["Basic"]["audio_format"])
            self.audio_quality_spin.setValue(int(self.config["Basic"]["audio_quality"]))
            self.remux_combo.setCurrentText(self.config["PostProcessing"]["remux_video"])
            self.recode_combo.setCurrentText(self.config["PostProcessing"]["recode_video"])
            self.on_extract_audio_changed(
                Qt.Checked if self.config["Basic"].getboolean("extract_audio") else Qt.Unchecked)

            # 网络设置
            self.cert_check.setChecked(self.config["Advanced"].getboolean("no_check_certificate"))
            self.warn_check.setChecked(self.config["Advanced"].getboolean("no_warnings"))

            retries_val = self.config["Advanced"]["retries"]
            self.retry_spin.setValue(int(retries_val) if retries_val and retries_val != "infinite" else 0)

            fragment_val = self.config["Advanced"]["fragment_retries"]
            self.fragment_retry_spin.setValue(int(fragment_val) if fragment_val and fragment_val != "infinite" else 0)

            self.timeout_spin.setValue(int(self.config["Advanced"]["timeout"]))
            self.socket_timeout_spin.setValue(int(self.config["Advanced"]["socket_timeout"]))
            self.concurrent_spin.setValue(int(self.config["Advanced"]["concurrent_fragments"]))
            self.rate_limit_edit.setText(self.config["Advanced"]["limit_rate"])
            self.throttled_edit.setText(self.config["Advanced"]["throttled_rate"])
            self.proxy_edit.setText(self.config["Advanced"]["proxy"])
            self.source_addr_edit.setText(self.config["Advanced"]["source_address"])
            self.impersonate_edit.setCurrentText(self.config["Advanced"]["impersonate"])
            self.ipv4_check.setChecked(self.config["Advanced"].getboolean("force_ipv4"))
            self.ipv6_check.setChecked(self.config["Advanced"].getboolean("force_ipv6"))
            self.dynamic_mpd_check.setChecked(self.config["Advanced"].getboolean("allow_dynamic_mpd"))
            self.hls_split_check.setChecked(self.config["Advanced"].getboolean("hls_split_discontinuity"))

            extractor_val = self.config["Advanced"]["extractor_retries"]
            self.extractor_retry_spin.setValue(
                int(extractor_val) if extractor_val and extractor_val != "infinite" else 0)

            # 批量设置
            self.batch_check.setChecked(self.config["Batch"].getboolean("auto_recognize_batch"))
            self.playlist_items_edit.setText(self.config["Batch"]["playlist_items"])

            max_downloads_val = self.config["Batch"]["max_downloads"]
            self.max_downloads_spin.setValue(
                int(max_downloads_val) if max_downloads_val and max_downloads_val.isdigit() else 0)

            self.playlist_random_check.setChecked(self.config["Batch"].getboolean("playlist_random"))
            self.lazy_playlist_check.setChecked(self.config["Batch"].getboolean("lazy_playlist"))

            # 视频选择设置
            self.min_filesize_edit.setText(self.config["Selection"]["min_filesize"])
            self.max_filesize_edit.setText(self.config["Selection"]["max_filesize"])
            self.date_edit.setText(self.config["Selection"]["date"])
            self.datebefore_edit.setText(self.config["Selection"]["datebefore"])
            self.dateafter_edit.setText(self.config["Selection"]["dateafter"])

            age_limit_val = self.config["Selection"]["age_limit"]
            self.age_limit_spin.setValue(int(age_limit_val) if age_limit_val and age_limit_val.isdigit() else 0)

            self.match_filters_edit.setText(self.config["Selection"]["match_filters"])
            self.download_archive_edit.setText(self.config["Selection"]["download_archive"])

            # 字幕设置
            self.write_subs_check.setChecked(self.config["Subtitles"].getboolean("write_subs"))
            self.write_auto_subs_check.setChecked(self.config["Subtitles"].getboolean("write_auto_subs"))
            self.sub_format_combo.setCurrentText(self.config["Subtitles"]["sub_format"])
            self.sub_langs_edit.setText(self.config["Subtitles"]["sub_langs"])
            self.embed_subs_check.setChecked(self.config["Subtitles"].getboolean("embed_subs"))
            self.convert_subs_combo.setCurrentText(self.config["Subtitles"]["convert_subs"])

            # 后处理设置
            self.keep_video_check.setChecked(self.config["PostProcessing"].getboolean("keep_video"))
            self.post_overwrites_check.setChecked(self.config["PostProcessing"].getboolean("post_overwrites"))
            self.embed_chapters_check.setChecked(self.config["PostProcessing"].getboolean("embed_chapters"))
            self.embed_info_json_check.setChecked(self.config["PostProcessing"].getboolean("embed_info_json"))
            self.fixup_combo.setCurrentText(self.config["PostProcessing"]["fixup"])
            self.split_chapters_check.setChecked(self.config["PostProcessing"].getboolean("split_chapters"))
            self.force_keyframes_check.setChecked(self.config["PostProcessing"].getboolean("force_keyframes_at_cuts"))
            self.remove_chapters_edit.setText(self.config["PostProcessing"]["remove_chapters"])
            self.concat_combo.setCurrentText(self.config["PostProcessing"]["concat_playlist"])
            self.exec_edit.setText(self.config["PostProcessing"]["exec_cmd"])

            # SponsorBlock设置
            self.sb_mark_edit.setText(self.config["SponsorBlock"]["sponsorblock_mark"])
            self.sb_remove_edit.setText(self.config["SponsorBlock"]["sponsorblock_remove"])
            self.sb_title_edit.setText(self.config["SponsorBlock"]["sponsorblock_chapter_title"])
            self.sb_api_edit.setText(self.config["SponsorBlock"]["sponsorblock_api"])

            # 路径设置
            self.download_edit.setText(self.config["Path"]["download_path"])
            self.cookie_edit.setText(self.config["Path"]["cookie_path"])
            self.auto_open_check.setChecked(self.config["Path"].getboolean("auto_open_folder"))
            self.ffmpeg_edit.setText(self.config["Path"]["ffmpeg_location"])
            self.cache_dir_edit.setText(self.config["Path"]["cache_dir"])

            # 分类与重命名
            self.classify_combo.setCurrentText(self.config["Classification"]["classify_rule"])
            self.date_combo.setCurrentText(self.config["Classification"]["date_format"])

            # 智能重命名设置
            self.smart_rename_check.setChecked(self.config["Rename"].getboolean("smart_rename"))

            # 设置策略组合框
            strategy = self.config["Rename"]["rename_strategy"]
            strategy_texts = {
                "auto": "auto - 自动选择最佳方案",
                "smart": "smart - 智能提取关键词",
                "title": "title - 仅使用原标题",
                "combined": "combined - 组合信息 (上传者 - 标题)",
                "compact": "compact - 紧凑命名",
                "template": "template - 使用自定义模板"
            }
            self.strategy_combo.setCurrentText(strategy_texts.get(strategy, "auto - 自动选择最佳方案"))

            self.min_length_spin.setValue(int(self.config["Rename"]["min_meaningful_length"]))
            self.keep_original_check.setChecked(self.config["Rename"].getboolean("keep_original_if_good"))
            self.uploader_fallback_check.setChecked(self.config["Rename"].getboolean("use_uploader_as_fallback"))
            self.include_res_check.setChecked(self.config["Rename"].getboolean("include_resolution"))
            self.include_date_check.setChecked(self.config["Rename"].getboolean("include_date"))

            # 传统重命名设置
            self.template_combo.setCurrentText(self.config["Rename"]["rename_template"])
            self.length_spin.setValue(int(self.config["Rename"]["max_char_length"]))
            self.replace_check.setChecked(self.config["Rename"].getboolean("replace_illegal_chars"))
            self.windows_check.setChecked(self.config["Rename"].getboolean("windows_filenames"))

            # 界面设置
            self.theme_combo.setCurrentText(self.config["UI"]["theme"])
            self.font_spin.setValue(int(self.config["UI"]["font_size"]))
            self.width_spin.setValue(int(self.config["UI"]["window_width"]))
            self.height_spin.setValue(int(self.config["UI"]["window_height"]))
            self.show_advanced_check.setChecked(self.config["UI"].getboolean("show_advanced"))

            # 彩蛋设置
            self.funny_messages_check.setChecked(self.config["EasterEggs"].getboolean("enable_funny_messages"))
            self.secret_logos_check.setChecked(self.config["EasterEggs"].getboolean("enable_secret_logos"))
            self.hidden_features_check.setChecked(self.config["EasterEggs"].getboolean("enable_hidden_features"))
            # secret_codes_check 没有对应的配置项，默认启用

            self.on_smart_rename_changed(
                Qt.Checked if self.config["Rename"].getboolean("smart_rename") else Qt.Unchecked)
            self.on_classify_changed(self.classify_combo.currentText())
            self.update_preview()

        except Exception as e:
            print(f"加载设置失败: {e}")
            import traceback
            traceback.print_exc()

    def reset_settings(self):
        """重置为默认设置"""
        reply = QMessageBox.question(
            self, "确认重置",
            "确定要将所有设置重置为默认值吗？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            default_config, _ = load_config()
            self.config = default_config
            self.load_settings()

            # 彩蛋：重置时显示有趣的消息
            if random.random() < 0.5:
                QMessageBox.information(self, "重置成功", "✨ 设置已重置为默认值，一切重新开始！")
            else:
                QMessageBox.information(self, "重置成功", "✅ 设置已重置为默认值")

    def save_settings(self):
        """保存设置"""
        try:
            # 基础设置
            self.config["Basic"]["resolution"] = self.res_combo.currentText()
            self.config["Basic"]["output_format"] = self.format_combo.currentText()
            self.config["Basic"]["embed_cover"] = str(self.cover_check.isChecked())
            self.config["Basic"]["embed_metadata"] = str(self.metadata_check.isChecked())
            self.config["Basic"]["skip_existing"] = str(self.skip_check.isChecked())

            # 音视频设置
            self.config["Basic"]["extract_audio"] = str(self.extract_audio_check.isChecked())
            self.config["Basic"]["audio_format"] = self.audio_format_combo.currentText()
            self.config["Basic"]["audio_quality"] = str(self.audio_quality_spin.value())
            self.config["PostProcessing"]["remux_video"] = self.remux_combo.currentText()
            self.config["PostProcessing"]["recode_video"] = self.recode_combo.currentText()

            # 网络设置
            self.config["Advanced"]["no_check_certificate"] = str(self.cert_check.isChecked())
            self.config["Advanced"]["no_warnings"] = str(self.warn_check.isChecked())
            self.config["Advanced"]["retries"] = "infinite" if self.retry_spin.value() == 0 else str(
                self.retry_spin.value())
            self.config["Advanced"]["fragment_retries"] = "infinite" if self.fragment_retry_spin.value() == 0 else str(
                self.fragment_retry_spin.value())
            self.config["Advanced"]["timeout"] = str(self.timeout_spin.value())
            self.config["Advanced"]["socket_timeout"] = str(self.socket_timeout_spin.value())
            self.config["Advanced"]["concurrent_fragments"] = str(self.concurrent_spin.value())
            self.config["Advanced"]["limit_rate"] = self.rate_limit_edit.text()
            self.config["Advanced"]["throttled_rate"] = self.throttled_edit.text()
            self.config["Advanced"]["proxy"] = self.proxy_edit.text()
            self.config["Advanced"]["source_address"] = self.source_addr_edit.text()
            self.config["Advanced"]["impersonate"] = self.impersonate_edit.currentText()
            self.config["Advanced"]["force_ipv4"] = str(self.ipv4_check.isChecked())
            self.config["Advanced"]["force_ipv6"] = str(self.ipv6_check.isChecked())
            self.config["Advanced"]["allow_dynamic_mpd"] = str(self.dynamic_mpd_check.isChecked())
            self.config["Advanced"]["hls_split_discontinuity"] = str(self.hls_split_check.isChecked())
            self.config["Advanced"][
                "extractor_retries"] = "infinite" if self.extractor_retry_spin.value() == 0 else str(
                self.extractor_retry_spin.value())

            # 批量设置
            self.config["Batch"]["auto_recognize_batch"] = str(self.batch_check.isChecked())
            self.config["Batch"]["playlist_items"] = self.playlist_items_edit.text()
            self.config["Batch"]["max_downloads"] = "" if self.max_downloads_spin.value() == 0 else str(
                self.max_downloads_spin.value())
            self.config["Batch"]["playlist_random"] = str(self.playlist_random_check.isChecked())
            self.config["Batch"]["lazy_playlist"] = str(self.lazy_playlist_check.isChecked())

            # 视频选择设置
            self.config["Selection"]["min_filesize"] = self.min_filesize_edit.text()
            self.config["Selection"]["max_filesize"] = self.max_filesize_edit.text()
            self.config["Selection"]["date"] = self.date_edit.text()
            self.config["Selection"]["datebefore"] = self.datebefore_edit.text()
            self.config["Selection"]["dateafter"] = self.dateafter_edit.text()
            self.config["Selection"]["age_limit"] = "" if self.age_limit_spin.value() == 0 else str(
                self.age_limit_spin.value())
            self.config["Selection"]["match_filters"] = self.match_filters_edit.text()
            self.config["Selection"]["download_archive"] = self.download_archive_edit.text()

            # 字幕设置
            self.config["Subtitles"]["write_subs"] = str(self.write_subs_check.isChecked())
            self.config["Subtitles"]["write_auto_subs"] = str(self.write_auto_subs_check.isChecked())
            self.config["Subtitles"]["sub_format"] = self.sub_format_combo.currentText()
            self.config["Subtitles"]["sub_langs"] = self.sub_langs_edit.text()
            self.config["Subtitles"]["embed_subs"] = str(self.embed_subs_check.isChecked())
            self.config["Subtitles"]["convert_subs"] = self.convert_subs_combo.currentText()

            # 后处理设置
            self.config["PostProcessing"]["keep_video"] = str(self.keep_video_check.isChecked())
            self.config["PostProcessing"]["post_overwrites"] = str(self.post_overwrites_check.isChecked())
            self.config["PostProcessing"]["embed_chapters"] = str(self.embed_chapters_check.isChecked())
            self.config["PostProcessing"]["embed_info_json"] = str(self.embed_info_json_check.isChecked())
            self.config["PostProcessing"]["fixup"] = self.fixup_combo.currentText()
            self.config["PostProcessing"]["split_chapters"] = str(self.split_chapters_check.isChecked())
            self.config["PostProcessing"]["force_keyframes_at_cuts"] = str(self.force_keyframes_check.isChecked())
            self.config["PostProcessing"]["remove_chapters"] = self.remove_chapters_edit.text()
            self.config["PostProcessing"]["concat_playlist"] = self.concat_combo.currentText()
            self.config["PostProcessing"]["exec_cmd"] = self.exec_edit.text()

            # SponsorBlock设置
            self.config["SponsorBlock"]["sponsorblock_mark"] = self.sb_mark_edit.text()
            self.config["SponsorBlock"]["sponsorblock_remove"] = self.sb_remove_edit.text()
            self.config["SponsorBlock"]["sponsorblock_chapter_title"] = self.sb_title_edit.text()
            self.config["SponsorBlock"]["sponsorblock_api"] = self.sb_api_edit.text()

            # 路径设置
            self.config["Path"]["download_path"] = self.download_edit.text()
            self.config["Path"]["cookie_path"] = self.cookie_edit.text()
            self.config["Path"]["auto_open_folder"] = str(self.auto_open_check.isChecked())
            self.config["Path"]["ffmpeg_location"] = self.ffmpeg_edit.text()
            self.config["Path"]["cache_dir"] = self.cache_dir_edit.text()

            # 分类设置
            self.config["Classification"]["classify_rule"] = self.classify_combo.currentText()
            self.config["Classification"]["date_format"] = self.date_combo.currentText()

            # 重命名设置
            self.config["Rename"]["smart_rename"] = str(self.smart_rename_check.isChecked())

            # 获取策略
            strategy_text = self.strategy_combo.currentText()
            strategy = strategy_text.split(" - ")[0] if " - " in strategy_text else "auto"
            self.config["Rename"]["rename_strategy"] = strategy

            self.config["Rename"]["min_meaningful_length"] = str(self.min_length_spin.value())
            self.config["Rename"]["keep_original_if_good"] = str(self.keep_original_check.isChecked())
            self.config["Rename"]["use_uploader_as_fallback"] = str(self.uploader_fallback_check.isChecked())
            self.config["Rename"]["include_resolution"] = str(self.include_res_check.isChecked())
            self.config["Rename"]["include_date"] = str(self.include_date_check.isChecked())

            # 传统重命名设置
            self.config["Rename"]["rename_template"] = self.template_combo.currentText()
            self.config["Rename"]["max_char_length"] = str(self.length_spin.value())
            self.config["Rename"]["replace_illegal_chars"] = str(self.replace_check.isChecked())
            self.config["Rename"]["windows_filenames"] = str(self.windows_check.isChecked())

            # 界面设置
            self.config["UI"]["theme"] = self.theme_combo.currentText()
            self.config["UI"]["font_size"] = str(self.font_spin.value())
            self.config["UI"]["window_width"] = str(self.width_spin.value())
            self.config["UI"]["window_height"] = str(self.height_spin.value())
            self.config["UI"]["show_advanced"] = str(self.show_advanced_check.isChecked())

            # 彩蛋设置
            self.config["EasterEggs"]["enable_funny_messages"] = str(self.funny_messages_check.isChecked())
            self.config["EasterEggs"]["enable_secret_logos"] = str(self.secret_logos_check.isChecked())
            self.config["EasterEggs"]["enable_hidden_features"] = str(self.hidden_features_check.isChecked())

            if save_config(self.config, self.config_path):
                # 彩蛋：保存成功的有趣消息
                if self.funny_messages_check.isChecked() and random.random() < 0.3:
                    QMessageBox.information(self, "保存成功", random.choice([
                        "✅ 设置已保存！魔法生效中... ✨",
                        "🎉 设置保存成功！准备好下载了吗？",
                        "💾 设置已存档，随时可以召唤下载！"
                    ]))
                else:
                    QMessageBox.information(self, "成功", "✅ 设置已保存")
                self.accept()
            else:
                QMessageBox.warning(self, "失败", "❌ 保存设置失败")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存设置时发生错误: {str(e)}")
            import traceback
            traceback.print_exc()


# ============================================
# 主窗口
# ============================================
class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        # 加载配置
        self.config, self.config_path = load_config()
        self.download_thread = None
        self.init_ui()

        # 彩蛋：秘密按键序列检测
        self.secret_sequence, self.check_secret = EasterEggs.secret_key_sequence()
        self.installEventFilter(self)

        # 彩蛋：记录启动时间
        self.start_time = time.time()

    def eventFilter(self, obj, event):
        """事件过滤器，用于检测秘密按键序列"""
        if event.type() == event.KeyPress:
            key = event.key()
            # 记录按键（转换为字符）
            if Qt.Key_A <= key <= Qt.Key_Z:
                char = chr(key).upper()
                self.secret_sequence.append(char)
            elif Qt.Key_0 <= key <= Qt.Key_9:
                char = chr(key)
                self.secret_sequence.append(char)
            elif key in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right]:
                directions = {Qt.Key_Up: '上', Qt.Key_Down: '下',
                              Qt.Key_Left: '左', Qt.Key_Right: '右'}
                self.secret_sequence.append(directions[key])

            # 检查秘密序列
            message = self.check_secret()
            if message:
                # 彩蛋：显示秘密消息
                self.append_log(f"🎮 {message}")
                self.secret_sequence.clear()

        return super().eventFilter(obj, event)

    def init_ui(self):
        """初始化UI"""
        # 窗口设置
        self.setWindowTitle(EasterEggs.get_secret_logo() if self.config["EasterEggs"].getboolean(
            "enable_secret_logos") else "🎬 PyQtDL")
        self.setMinimumSize(
            int(self.config["UI"]["window_width"]),
            int(self.config["UI"]["window_height"])
        )

        # 设置窗口图标
        self.setWindowIcon(QIcon.fromTheme("applications-multimedia"))

        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 标题标签 - 根据彩蛋设置显示不同标题
        title_text = EasterEggs.get_secret_logo() if self.config["EasterEggs"].getboolean(
            "enable_secret_logos") else "🎬 PyQtDL"
        title_label = QLabel(title_text)
        title_label.setStyleSheet("""
            font-size: 28pt;
            font-weight: 700;
            color: #1c2b36;
            padding: 15px 0;
            border-bottom: 3px solid #0078d4;
            background: linear-gradient(135deg, #f8fafc 0%, #e3e9f1 100%);
            border-radius: 12px;
            margin-bottom: 10px;
        """)
        title_label.setAlignment(Qt.AlignCenter)

        # 彩蛋：如果是特殊日子，添加额外装饰
        if EasterEggs.hidden_feature_enabled():
            title_label.setStyleSheet(title_label.styleSheet() + """
                background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
                border-bottom: 3px solid #e74c3c;
            """)

        main_layout.addWidget(title_label)

        # 链接输入区域
        input_group = QGroupBox("🔗 输入链接")
        input_group.setStyleSheet("""
            QGroupBox {
                font-weight: 700;
                font-size: 12pt;
                color: #2c3e50;
            }
        """)
        input_layout = QVBoxLayout(input_group)

        # 链接输入标签页
        self.url_tab = QTabWidget()
        input_layout.addWidget(self.url_tab)

        # 单个链接输入
        single_tab = QWidget()
        single_layout = QVBoxLayout(single_tab)
        self.single_url_edit = DragDropLineEdit("🔗 输入单个视频链接，或拖放链接到此处")
        self.single_url_edit.setPlaceholderText("例如: https://www.bilibili.com/video/BV1xxx...")
        single_layout.addWidget(self.single_url_edit)
        self.url_tab.addTab(single_tab, "🔗 单个链接")

        # 批量链接输入
        batch_tab = QWidget()
        batch_layout = QVBoxLayout(batch_tab)
        self.batch_url_edit = DragDropTextEdit("📋 输入多个视频链接（每行一个），或拖放txt文件到此处")
        batch_layout.addWidget(self.batch_url_edit)
        batch_hint = QLabel("💡 提示：每行输入一个链接，支持播放列表链接")
        batch_hint.setStyleSheet("color: #666; font-size: 10pt; font-style: italic; padding: 5px;")
        batch_layout.addWidget(batch_hint)
        self.url_tab.addTab(batch_tab, "📋 批量链接")

        main_layout.addWidget(input_group)

        # 按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        self.start_btn = QPushButton("🚀 开始下载")
        self.start_btn.setMinimumHeight(48)
        self.start_btn.setMinimumWidth(140)
        self.start_btn.clicked.connect(self.start_download)

        self.clear_btn = QPushButton("🗑️ 清空输入")
        self.clear_btn.setMinimumHeight(48)
        self.clear_btn.setMinimumWidth(140)
        self.clear_btn.clicked.connect(self.clear_input)

        self.settings_btn = QPushButton("⚙️ 设置")
        self.settings_btn.setMinimumHeight(48)
        self.settings_btn.setMinimumWidth(140)
        self.settings_btn.clicked.connect(self.open_settings)

        self.about_btn = QPushButton("❓ 关于")
        self.about_btn.setMinimumHeight(48)
        self.about_btn.setMinimumWidth(140)
        self.about_btn.clicked.connect(self.show_about)

        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addWidget(self.settings_btn)
        btn_layout.addWidget(self.about_btn)
        main_layout.addLayout(btn_layout)

        # 日志显示区域
        log_group = QGroupBox("📝 下载日志")
        log_group.setStyleSheet("""
            QGroupBox {
                font-weight: 700;
                font-size: 12pt;
                color: #2c3e50;
            }
        """)
        log_layout = QVBoxLayout(log_group)

        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        log_layout.addWidget(self.log_edit)

        main_layout.addWidget(log_group, 1)

        # 进度区域
        progress_layout = QHBoxLayout()
        progress_layout.setSpacing(15)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)

        self.status_label = QLabel("✅ 就绪")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 11pt;
                font-weight: 600;
                padding: 8px 16px;
                background-color: #f8fafc;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                min-width: 150px;
                text-align: center;
            }
        """)

        progress_layout.addWidget(self.progress_bar, 3)
        progress_layout.addWidget(self.status_label, 1)
        main_layout.addLayout(progress_layout)

        # 状态栏
        self.statusBar().showMessage("✅ 准备就绪")

        # 应用样式
        self.apply_theme()

    def start_download(self):
        """开始下载"""
        # 获取链接列表
        url_list = []
        if self.url_tab.currentIndex() == 0:  # 单个链接
            url = self.single_url_edit.text().strip()
            if url:
                url_list = [url]
            else:
                QMessageBox.warning(self, "输入错误", "⚠️ 请输入视频链接")
                return
        else:  # 批量链接
            text = self.batch_url_edit.toPlainText().strip()
            if text:
                url_list = [line.strip() for line in text.split('\n') if line.strip()]
            else:
                QMessageBox.warning(self, "输入错误", "⚠️ 请输入至少一个视频链接")
                return

        # 检查是否正在下载
        if self.download_thread and self.download_thread.isRunning():
            QMessageBox.information(self, "提示", "⏳ 正在下载中，请等待当前任务完成")
            return

        # 检查下载路径
        download_path = self.config["Path"]["download_path"]
        if not os.path.exists(download_path):
            try:
                os.makedirs(download_path, exist_ok=True)
            except Exception as e:
                QMessageBox.critical(self, "路径错误", f"❌ 无法创建下载目录：{str(e)}")
                return

        # 彩蛋：有趣的开场白
        if self.config["EasterEggs"].getboolean("enable_funny_messages"):
            funny_intros = [
                "🚀 发射！开始下载冒险！",
                "🎬 灯光！摄影机！下载！",
                "🦸 超级下载英雄出动！",
                "🎪 下载马戏团开始表演！"
            ]
            if random.random() < 0.3:
                self.append_log(f"✨ {random.choice(funny_intros)}")

        # 初始化并启动下载线程
        self.download_thread = BatchDownloadThread(url_list, self.config)
        self.download_thread.log_signal.connect(self.append_log)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.finish_signal.connect(self.download_finished)
        self.download_thread.info_signal.connect(self.update_video_info)

        # 更新UI状态
        self.start_btn.setEnabled(False)
        self.start_btn.setText("⏳ 下载中...")
        self.clear_btn.setEnabled(False)
        self.settings_btn.setEnabled(False)
        self.about_btn.setEnabled(False)
        self.url_tab.setEnabled(False)
        self.progress_bar.setValue(0)

        # 彩蛋：有趣的进度标签
        if self.config["EasterEggs"].getboolean("enable_funny_messages"):
            progress_labels = [
                f"📥 准备下载 {len(url_list)} 个任务...",
                f"🎯 锁定 {len(url_list)} 个目标...",
                f"📋 处理 {len(url_list)} 个任务中..."
            ]
            self.status_label.setText(random.choice(progress_labels))
        else:
            self.status_label.setText(f"📥 准备下载 {len(url_list)} 个任务...")

        # 开始下载
        self.download_thread.start()
        self.append_log(f"🚀 开始下载 {len(url_list)} 个任务...")

    def append_log(self, text):
        """追加日志"""
        self.log_edit.append(text)
        # 滚动到底部
        cursor = self.log_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log_edit.setTextCursor(cursor)
        # 更新状态栏
        self.statusBar().showMessage(text[:100])

    def update_progress(self, current, total):
        """更新进度"""
        progress = int((current / total) * 100)
        self.progress_bar.setValue(progress)

        # 彩蛋：有趣的进度标签
        if self.config["EasterEggs"].getboolean("enable_funny_messages"):
            funny_status = EasterEggs.get_funny_progress_message(progress)
            self.status_label.setText(f"📥 {funny_status}")
        else:
            self.status_label.setText(f"📥 正在处理：{current}/{total}")

    def update_video_info(self, info):
        """更新视频信息"""
        title = info.get('title', '未知标题')
        self.statusBar().showMessage(f"🎬 正在下载：{title[:30]}...")

    def download_finished(self, success, message):
        """下载完成处理"""
        self.append_log(f"\n{'=' * 60}")

        # 彩蛋：根据结果添加不同表情
        if success:
            if self.config["EasterEggs"].getboolean("enable_funny_messages"):
                finish_messages = [
                    "🎉 下载大胜利！",
                    "🏆 任务完成，掌声鼓励！",
                    "🌟 完美收工！",
                    "✅ 全部搞定！"
                ]
                self.append_log(random.choice(finish_messages))
            else:
                self.append_log("✅ 下载完成")
        else:
            if self.config["EasterEggs"].getboolean("enable_funny_messages"):
                self.append_log("😅 下载完成，但有些小插曲...")
            else:
                self.append_log("⚠️ 下载完成但有错误")

        self.append_log(message)

        # 更新UI状态
        self.start_btn.setEnabled(True)
        self.start_btn.setText("🚀 开始下载")
        self.clear_btn.setEnabled(True)
        self.settings_btn.setEnabled(True)
        self.about_btn.setEnabled(True)
        self.url_tab.setEnabled(True)
        self.progress_bar.setValue(100)

        # 彩蛋：计算并显示任务耗时
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 60 and self.config["EasterEggs"].getboolean("enable_funny_messages"):
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            time_message = random.choice([
                f"⏱️ 本次任务耗时: {minutes}分{seconds}秒",
                f"🕒 用时: {minutes}分{seconds}秒",
                f"⏰ 耗时: {minutes}分{seconds}秒"
            ])
            self.append_log(time_message)

        if success:
            self.status_label.setText("✅ 下载完成")
            self.statusBar().showMessage("✅ 下载完成")

            # 只显示成功的消息对话框
            if self.config["EasterEggs"].getboolean("enable_funny_messages") and random.random() < 0.3:
                QMessageBox.information(self, "下载完成", random.choice([
                    "🎉 任务完成！视频已就绪！",
                    "✅ 下载成功！快去查看吧！",
                    "🌟 太棒了！所有视频都下载好了！"
                ]))
            else:
                QMessageBox.information(self, "下载完成", f"✅ {message}")
        else:
            # 失败时不弹窗，只在日志中显示
            self.status_label.setText("⚠️ 下载完成但有错误")
            self.statusBar().showMessage("⚠️ 下载完成但有错误")

    def clear_input(self):
        """清空输入"""
        if self.url_tab.currentIndex() == 0:
            self.single_url_edit.clear()
        else:
            self.batch_url_edit.clear()
        self.log_edit.clear()
        self.progress_bar.setValue(0)
        self.status_label.setText("✅ 就绪")

        # 彩蛋：有趣的清空消息
        if self.config["EasterEggs"].getboolean("enable_funny_messages") and random.random() < 0.5:
            self.statusBar().showMessage("🧹 输入已清空，一切重新开始！")
        else:
            self.statusBar().showMessage("✅ 输入已清空")

    def open_settings(self):
        """打开设置窗口"""
        settings_window = SettingsWindow(self, self.config, self.config_path)
        if settings_window.exec_():
            # 保存设置后重新加载配置
            self.config, self.config_path = load_config()
            self.append_log("⚙️ 设置已更新")
            # 应用UI主题设置
            self.apply_theme()
            # 更新窗口标题（彩蛋）
            if self.config["EasterEggs"].getboolean("enable_secret_logos"):
                self.setWindowTitle(EasterEggs.get_secret_logo())

    def apply_theme(self):
        """应用主题设置"""
        theme = self.config["UI"]["theme"]

        if theme == "dark":
            # 暗色主题
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2c3e50;
                }
                QWidget {
                    background-color: #34495e;
                    color: #ecf0f1;
                }
                QGroupBox {
                    border: 2px solid #4a6572;
                    background-color: #3a506b;
                    color: #ecf0f1;
                }
                QTextEdit {
                    background-color: #2c3e50;
                    color: #ecf0f1;
                    border: 2px solid #4a6572;
                }
                QLineEdit {
                    background-color: #2c3e50;
                    color: #ecf0f1;
                    border: 2px solid #4a6572;
                }
                QProgressBar {
                    border: 2px solid #4a6572;
                    background-color: #2c3e50;
                    color: #ecf0f1;
                }
                QProgressBar::chunk {
                    background-color: #3498db;
                }
            """)
        else:
            # 亮色主题（默认）
            self.setStyleSheet("""
        QGroupBox {
            font-size: 11pt;
            font-weight: bold;
            margin-top: 10px;
            padding: 10px 15px 15px 15px;
            border: 1px solid #d1d1d1;
            border-radius: 4px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        QPushButton {
            background-color: #0078d4;
            color: white;
            border-radius: 4px;
            padding: 6px 12px;
            font-size: 11pt;
            border: none;
        }
        QPushButton:hover {
            background-color: #0066b2;
        }
        QPushButton:pressed {
            background-color: #005cae;
        }
        QPushButton:disabled {
            background-color: #cccccc;
            color: #666666;
        }
        QTabWidget::pane {
            border: 1px solid #d1d1d1;
            border-radius: 4px;
            padding: 10px;
        }
        QTabBar::tab {
            padding: 8px 16px;
            font-size: 10pt;
            border-radius: 4px 4px 0 0;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: white;
            border: 1px solid #d1d1d1;
            border-bottom-color: white;
        }
        QTabBar::tab:!selected {
            background-color: #f0f0f0;
        }
        QTabBar::tab:hover:!selected {
            background-color: #e0e0e0;
        }
    """)

    def show_about(self):
        """显示关于信息"""
        about_text = """
        PyQtDL
        项目主页：https://github.com/Aiien2011/PyQtDL

        基于 yt-dlp 的强大视频下载工具
        ✨ 支持多种平台视频下载

        📋 主要特性：
        • 🤖 智能重命名系统
        • 🔗 单个/批量视频下载
        • 🎯 自定义分辨率和输出格式
        • 🗂️ 自动分类和智能重命名
        • 🎨 嵌入封面和元数据
        • ⚡ 多线程加速下载
        • 🎥 SponsorBlock 支持

        🤖 智能重命名：
        • 自动识别无意义文件名
        • 从标题提取关键词
        • 多种命名策略可选
        • 保留有意义原文件名

        🛠️ 技术支持：
        • 基于 yt-dlp 核心
        • 支持 ffmpeg 后处理
        • 自定义下载参数

        📧 反馈与支持：
        如有问题或建议，请联系开发者Aiien2011
        
        PyQtDL
        """

        # 彩蛋：特殊日子里显示特殊关于信息
        if EasterEggs.hidden_feature_enabled():
            about_text += "\n\n🎉 今天是幸运日！隐藏功能已解锁！"

        QMessageBox.about(self, "关于", about_text)

    def closeEvent(self, event):
        """窗口关闭事件"""
        if self.download_thread and self.download_thread.isRunning():
            reply = QMessageBox.question(
                self, "确认关闭",
                "⏳ 正在下载中，确定要关闭吗？",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.No:
                event.ignore()
                return

        # 保存窗口大小
        self.config["UI"]["window_width"] = str(self.width())
        self.config["UI"]["window_height"] = str(self.height())
        save_config(self.config, self.config_path)

        # 彩蛋：关闭时的有趣消息
        if self.config["EasterEggs"].getboolean("enable_funny_messages") and random.random() < 0.2:
            goodbye_messages = ["下次再见！👋", "期待再次使用！✨", "拜拜！👋", "后会有期！🌟"]
            print(random.choice(goodbye_messages))

        event.accept()


# ============================================
# 应用程序入口
# ============================================
def main():
    # 确保中文显示正常
    import matplotlib
    matplotlib.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))

    # 设置应用程序图标和名称
    app.setApplicationName("PyQtDL")
    app.setApplicationDisplayName("🎬 PyQtDL")

    # 设置全局字体
    font = QFont()
    font.setFamily("Microsoft YaHei")
    font.setPointSize(10)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
