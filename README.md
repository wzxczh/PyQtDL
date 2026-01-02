# PyQtDL

<div align="center">
  <p>一款基于 PyQt5 开发的轻量级可视化视频下载工具，简洁易用、高效稳定</p>
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/PyQt5-5.15%2B-green.svg" alt="PyQt5 Version">
</div>

## 项目简介
PyQtDL（PyQt Downloader）是一款专注于yt-dlp可视化的桌面工具，核心基于 **PyQt5** 框架构建图形界面，摆脱了命令行下载的繁琐操作，为用户提供直观、便捷的视频获取体验。项目代码简洁易懂，可扩展性强，支持主流视频平台解析与下载，兼顾了功能性与易用性，适合个人日常使用或二次开发学习。

## 核心特性
-  **可视化界面**：基于 PyQt5 打造简洁美观的yt-dlp桌面交互界面，无需命令行操作，新手友好
-  **高效下载**：支持多线程下载、断点续传，提升视频获取效率
-  **轻量无冗余**：核心代码精简，无多余依赖，安装便捷，运行占用资源少
-  **方便快捷**：软件直接内置yt-dlp,ffprobe.exe,ffmpeg.exe，无需下载即可立刻使用！

## 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/Aiien2011/pyqtdl.git
cd pyqtdl
```

### 2. 运行软件
直接运行主程序


### 3. 使用流程
1. 打开软件后，在输入框中粘贴目标视频链接
2. 点击「开始下载」按钮，等待下载完成

## PyQt-Fluent-Widgets 版本使用指南

### 运行Fluent版本
```bash
.venv\Scripts\python.exe PyQtDl_fluent.py
```

### 功能介绍

#### 📊 仪表盘
- **下载统计**：显示总下载次数、成功下载数、失败次数
- **快速操作**：一键跳转到下载页面或设置页面

#### 📥 下载
- **单个下载**：输入单个视频链接进行下载
- **批量下载**：输入多个链接（每行一个）进行批量下载
- **拖拽支持**：支持直接拖拽链接到输入框
- **实时进度**：显示下载进度、速度和预计剩余时间
- **下载日志**：实时显示下载状态和日志信息

#### 📜 历史记录
- **记录查看**：表格形式展示所有下载历史
- **搜索功能**：快速搜索历史记录
- **清空历史**：一键清空所有历史记录
- **导出记录**：导出历史记录（开发中）

#### ⚙️ 设置
- **下载设置**：
  - 保存路径：自定义下载文件保存位置
  - 并发线程数：设置同时下载的任务数量（1-10）
  - 重试次数：下载失败后的重试次数
  - 超时时间：下载超时时间设置
- **视频设置**：
  - 视频质量：选择下载的视频质量（最佳质量、1080p、720p等）
  - 音频质量：选择下载的音频质量
  - 下载字幕：是否下载视频字幕
  - 下载缩略图：是否下载视频缩略图
- **代理设置**：
  - 启用代理：开启代理功能
  - 代理地址：设置代理服务器地址

#### ℹ️ 关于
- **应用信息**：查看应用版本和描述
- **功能列表**：了解软件的主要功能
- **相关链接**：GitHub仓库和问题反馈

### 使用技巧
1. **快速下载**：在仪表盘点击"快速下载"按钮直接跳转到下载页面
2. **批量下载**：使用批量下载标签页，每行输入一个链接
3. **拖拽链接**：可以直接拖拽链接到输入框，无需手动粘贴
4. **查看历史**：在历史记录页面可以查看所有下载记录
5. **自定义设置**：在设置页面根据需要调整下载参数

## UI开发提示

### PyQt-Fluent-Widgets 组件使用

**卡片组件**
- `HeaderCardWidget` - 带有标题的卡片，适合页面标题
- `ElevatedCardWidget` - 带阴影的卡片，用于主要内容区域
- `SimpleCardWidget` - 简单卡片，用于嵌套内容

**按钮组件**
- `PrimaryPushButton` - 主要操作按钮，突出显示
- `PillPushButton` - 胶囊形状按钮，适合快速操作
- `PushButton` - 普通按钮，用于次要操作
- `TransparentPushButton` - 透明按钮，用于工具栏

**输入组件**
- `LineEdit` - 单行输入框
- `TextEdit` - 多行文本输入框
- `ComboBox` - 下拉选择框
- `SpinBox` - 数字输入框
- `CheckBox` - 复选框

**导航组件**
- `FluentWindow` - 主窗口基类
- `NavigationInterface` - 侧边栏导航
- `SegmentedWidget` - 分段切换器（Tab）

**其他组件**
- `ProgressBar` - 进度条
- `InfoBar` - 通知栏
- `ScrollArea` - 滚动区域
- `TableWidget` - 表格

### 开发注意事项

1. **避免使用不存在的API**
   - `HeaderCardWidget.setTitleSize()` - 此方法不存在
   - `SegmentedWidget.currentIndex()` - 使用`setCurrentItem(routeKey)`代替
   - `NavigationInterface.items()` - 直接使用路由键操作

2. **信号连接**
   - `SegmentedWidget.addItem()` 使用 `onClick` 回调处理切换
   - 不要将 `currentItemChanged` 连接到需要整数的 `setCurrentIndex`

3. **页面切换**
   - 使用 `stackedWidget.setCurrentWidget(widget)` 切换页面
   - 使用 `navigationInterface.setCurrentItem(routeKey)` 更新导航栏选中状态

4. **对象命名**
   - 每个页面必须设置 `objectName`
   - 路由键应与对象名称一致

5. **布局管理**
   - 使用 `VBoxLayout`、`QHBoxLayout` 进行布局
   - 设置合适的间距和边距
   - 使用 `ScrollArea` 包装长内容

### 主题设置
```python
from qfluentwidgets import setTheme, Theme
setTheme(Theme.LIGHT)  # 或 Theme.DARK
```



## 贡献指南
1. Fork 本仓库到个人账号
2. 创建特性分支（`git checkout -b feature/your-feature-name`）
3. 提交代码修改（`git commit -m "feat: 添加xxx功能"`）
4. 推送分支到远程仓库（`git push origin feature/your-feature-name`）
5. 提交 Pull Request，描述清楚修改内容及用途

我欢迎各类贡献，包括但不限于：功能优化、Bug 修复、界面美化、文档完善等。



## 致谢
- 感谢 [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) 提供强大的桌面界面开发框架
- 感谢开源项目[yt-dlp](https://github.com/yt-dlp/yt-dlp)提供的强大支持。
- 感谢所有为开源视频下载工具提供技术参考的开发者社区

## 联系方式
- 项目维护者：Aiien2011, wzxczh
- 邮箱：zzh82011@126.com, 28151655630@qq.com
- 仓库地址：https://github.com/Aiien2011/pyqtdl

如果本项目对你有帮助，欢迎点亮 ⭐ Star 支持！如有问题或建议，可提交 Issue 反馈。


由于本人为个人开发者，并且此项目并不是直接在此仓库中提交，所以此仓库只展示代码部分，并不非常合规。大家可以直接下载已经打包后的版本，位于发行版中。同时由于技术不过关和目前还是初中生等原因。软件虽然尽可能做到方便和利于使用，但是依然有很多不够完善的地方，请大家多多谅解。如果你是一位技术人员，希望您可以对项目做出贡献。
