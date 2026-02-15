<div align="center">

# MindTrack Desk · 灵迹桌面

基于火山引擎豆包多模态能力的 **Windows 智能屏幕记忆助手**  
记录你在电脑前的每一段「专注时刻」。

</div>

---

## ✨ 项目简介

**MindTrack Desk（灵迹桌面）** 是一个运行在 Windows 上的悬浮窗工具：

- 检测当前活动窗口的切换（例如你从 VS Code 切到浏览器）
- 自动为当前窗口截图，并调用 **火山引擎 Ark / 豆包多模态模型** 进行理解和总结
- 将「时间 + 窗口标题 + 截图 + AI 总结」保存到本地
- 提供一个炫酷的历史记录界面，帮助你回顾：  
  > 今天我到底都在干什么？

非常适合作为：

- 个人工作日志 / 时间追踪辅助
- 学习过程记录（看文档、写代码、看网课）
- 项目复盘时的时间线素材

> 🔒 所有截图与记录默认保存在本地（SQLite + 本地图片），不用担心被上传到第三方服务（除调用豆包 API 所需的图片外）。

---

## 🌈 核心特性

- 🪟 **悬浮窗 UI**
  - 无边框、始终置顶、可拖拽移动
  - 半透明深色风格，适合搭配各种主题桌面
  - 一键「开始/暂停监控」、入口按钮打开历史记录

- 👀 **智能窗口监控**
  - 基于 `pywin32` 捕获当前前台窗口句柄和标题
  - 防抖逻辑：只有停留一定时间（例如 1.5s）才会触发一次分析
  - 防刷屏：短时间频繁来回切换不会生成大量垃圾记录

- 🧠 **豆包多模态理解**
  - 使用火山引擎 Ark Runtime SDK，调用豆包多模态模型（如 `doubao-seed-2-0-pro-260215` 或 vision 模型）
  - 自动将截图编码为 Base64 传入 API，请求中包含提示词：
    - 总结当前屏幕内容
    - 推断你现在大概在做什么
    - 对文档 / 代码 / 网页做简要提炼

- 📚 **可视化历史时间线**
  - 以时间倒序展示最近若干条记录
  - 点选任意一条可以查看：
    - 截图大图
    - AI 生成的文字总结
    - 对应窗口标题与时间

- 💾 **本地存储**
  - 使用 SQLite 数据库存储结构化信息
  - 截图以 JPG 的形式保存在 `logs/images/` 目录

---

## 🏗 技术栈

- **语言**：Python 3.10+
- **桌面 UI**：PySide6 (Qt for Python)
- **Windows 底层能力**：pywin32（获取前台窗口、窗口标题、坐标）
- **截图**：mss + Pillow
- **AI 能力**：火山引擎 Ark Runtime（豆包多模态模型）
- **配置管理**：python-dotenv
- **本地存储**：SQLite3

---

## 📦 安装与运行

### 1. 克隆项目

```bash
git clone https://github.com/CanFlyhang/mindtrack-desk.git
cd mindtrack-desk
```

> ⚠️ 仓库名建议使用：`mindtrack-desk`

### 2. 创建虚拟环境（可选但推荐）

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置火山引擎豆包 Ark API

1. 参考火山引擎文档，在控制台创建 Ark API Key。
2. 将根目录下的 `.env.example` 复制为 `.env`：

   ```bash
   cp .env.example .env   # Windows 可直接手动复制重命名
   ```

3. 打开 `.env`，填入你的配置：

   ```ini
   ARK_API_KEY=你的APIKey
   # 选择你开通的多模态模型，比如：
   ARK_MODEL_NAME=doubao-seed-2-0-pro-260215

   # 截图保存目录（可保持默认）
   SCREENSHOT_DIR=logs/images
   ```

### 5. 启动程序

```bash
python main.py
```

首次运行后，你会看到一个小巧的悬浮窗：

- 点击 **「开始监控」**，然后像平常一样切换不同窗口工作
- 稍等片刻，悬浮窗状态文案会变成「正在分析：xxx」、「完成：xxx」
- 点击 **「历史记录」**，可以看到 AI 总结过的时间线和截图

---

## 🧩 目录结构

```text
mindtrack-desk/
├── main.py               # 程序入口，初始化 Qt 应用与控制器
├── requirements.txt      # 依赖列表
├── .env.example          # 环境变量示例（API Key / 模型名等）
├── src/
│   ├── ui/
│   │   ├── floating_window.py  # 悬浮窗 UI
│   │   ├── history_window.py   # 历史记录窗口 UI
│   │   └── styles.qss          # 全局样式表（深色主题）
│   ├── services/
│   │   ├── monitor.py          # WindowWatcher：监控当前活动窗口的 QThread
│   │   ├── capture.py          # ScreenCapture：窗口 / 全屏截图 + Base64
│   │   ├── ai_client.py        # ArkClient：封装豆包多模态 API 调用
│   │   ├── storage.py          # DataManager：SQLite 本地存储
│   │   └── worker.py           # AnalysisWorker：截图 + 调用 AI + 落地的后台线程
│   └── app_controller.py       # AppController：将 UI 与所有服务串联起来
└── logs/
    └── images/                 # 截图保存目录
```

---

## 🧠 工作原理（简要）

1. **前台窗口监听**
   - `WindowWatcher` 周期性调用 `win32gui.GetForegroundWindow()` 获取当前活动窗口句柄。
   - 如果发现句柄变化且稳定一段时间（防抖），则触发一次「窗口变更」事件。

2. **截图与编码**
   - 使用 `GetWindowRect` 获取窗口区域坐标。
   - `mss` 按坐标截取当前窗口（失败时退化为全屏截屏）。
   - 使用 Pillow 将图像压缩成 JPEG，并转成 Base64 字符串。

3. **调用豆包多模态模型**
   - `ArkClient` 使用 `volcenginesdkarkruntime` 向 Ark 的 `/responses` / Chat 接口发送请求。
   - 文本部分给出「请总结屏幕内容」等提示词，图像部分使用 `data:image/jpeg;base64,...` 方式嵌入。

4. **结果写入本地**
   - `AnalysisWorker` 在后台线程中完成「截图 → 调用 AI → 写入 SQLite / 保存图片」的全流程。
   - 完成后将简短的结果通过信号返回 UI，在悬浮窗中进行展示。

5. **历史记录展示**
   - `HistoryWindow` 从 SQLite 中读取最近 N 条记录，左侧列表 + 右侧大图 + 文本详细摘要。

---

## 🤝 如何参与共创

欢迎任何形式的贡献，包括但不限于：

- 新功能：比如
  - 黑名单应用（不对某些 App 截图）
  - 自定义截图频率 / 防抖时间
  - 导出为 Markdown 日志 / 导出为时间线 PDF
- Bug 修复：Windows 多屏形态、DPI 缩放适配问题等
- UI 改进：更酷的主题 / 动画 / 图标
- 文档与示例：使用教程、最佳实践、Demo 视频

### 提交方式

1. Fork 本仓库
2. 创建你的特性分支：`git checkout -b feature/your-feature-name`
3. 提交你的修改：`git commit -m "feat: xxx"`
4. 推送到你的仓库：`git push origin feature/your-feature-name`
5. 在 GitHub 上发起 Pull Request

---

## 📜 开源协议

建议使用 **MIT License** 或 **Apache-2.0 License**。  
你可以在项目根目录添加 `LICENSE` 文件，例如 MIT：

```text
MIT License

Copyright (c) 2026 YOUR NAME
...
```

---

## ❓ 常见问题

### 1. 运行时提示「未配置 API Key」

请确认：

- `.env` 文件已存在且位于项目根目录
- 文件中包含正确的 `ARK_API_KEY`
- 你已经重新启动了程序

### 2. 关闭程序时终端出现 QThread 警告

项目中已经通过 `AppController.cleanup()` 做了统一线程收尾逻辑。  
如果还有类似问题，欢迎提 Issue 并附上完整的终端输出日志。

### 3. 模型不返回图片相关内容，或者报「不支持图像」

请确认：

- `ARK_MODEL_NAME` 对应的是一个支持图片输入的 **多模态模型**
- 你在火山引擎控制台已经为该模型开通了对应的调用权限

---

## 🌟 Star & 分享

如果你觉得 **MindTrack Desk · 灵迹桌面** 对你有帮助，  
欢迎在 GitHub 上点一个 ⭐ Star，并分享给更多也在折腾效率工具的朋友们。

