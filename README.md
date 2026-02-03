# Context Manager Enhanced

<div align="center">

[![CI Status](https://github.com/username/context-manager/workflows/CI/badge.svg)](https://github.com/username/context-manager/actions)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/username/context-manager/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![codecov](https://codecov.io/gh/username/context-manager/branch/main/graph/badge.svg)](https://codecov.io/gh/username/context-manager)

### 🧠 工作区上下文管理工具 - 专为多项目并行开发设计

融合版工作区上下文管理工具，支持会话追踪、智能迁移、项目状态分类。

[功能特性](#-特性) • [快速开始](#-快速开始) • [使用指南](#-使用指南) • [贡献指南](#-贡献)

</div>

---

## ✨ 特性

- 🔄 **双格式兼容** - 自动识别 v1/v2 格式，无缝兼容
- 📊 **会话追踪** - 自动记录会话次数和 Git 分支
- 🚀 **智能迁移** - 一键从旧格式升级到融合版
- 🎯 **状态管理** - 按活跃/暂停/完成分类项目
- 📝 **快速切换** - 在多个项目间快速切换
- 🛠️ **零依赖** - 纯 Python 实现，无需额外依赖
- 🧪 **测试覆盖** - 完整的单元测试和集成测试

## 📊 目录

- [快速开始](#-快速开始)
- [使用指南](#-使用指南)
- [命令参考](#-命令参考)
- [项目结构](#-项目结构)
- [context.md 格式](#contextmd-格式)
- [使用场景](#-使用场景)
- [版本对比](#-版本对比)
- [贡献指南](#-贡献)
- [FAQ](#faq)
- [许可证](#-许可证)

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/username/context-manager.git
cd context-manager

# 创建虚拟环境（可选）
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# ctx 命令已可用，或添加到 PATH
export PATH="$PATH:$PWD"
```

### Shell 集成（推荐）

在 `~/.zshrc` 或 `~/.bashrc` 中添加：

```bash
source /path/to/context-manager/shell-integration.sh
```

然后就可以使用快捷命令：

```bash
repos           # 列出所有项目
go <project>    # 快速切换到项目
```

### 验证安装

```bash
ctx --version
ctx ls          # 查看所有项目
```

## 📖 使用指南

### 初始化新项目

```bash
mkdir ~/workspace/my-project
cd ~/workspace/my-project

# 初始化 context.md
ctx init

# 查看生成的文件
cat .claude/context.md
```

### 查看项目状态

```bash
# 完整信息
ctx

# 紧凑状态
ctx status
```

**输出示例：**

```
╔══════════════════════════════════════════════════════════════════╗
║                    🧠 工作区记忆已恢复                            ║
╠══════════════════════════════════════════════════════════════════╣
║  项目: example-project                                         ║
║  上次: 2026-02-03                                         ║
║  会话: #5                                                  ║
║  分支: feature/audio-sync                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  当前焦点: 实现音频同步功能                              ║
╠══════════════════════════════════════════════════════════════════╣
║  📋 待办列表:                                                    ║
║  - [ ] 完成音频上传                                        ║
║  - [ ] 实现同步逻辑                                        ║
╚══════════════════════════════════════════════════════════════════╝
```

### 列出所有项目

```bash
ctx ls
```

**输出示例：**

```
📁 Workspace 项目概览 (4 个项目)

🟢 进行中
   example-project               | 实现音频同步功能 #5

🟡 已暂停
   video-demo           | 2026-02-03
   demo-project                   | 2026-02-03
   tool-demo         | 2026-02-03
```

### 更新项目状态

```bash
# 暂停项目
ctx update status paused

# 更新焦点
ctx update current_focus "实现音频同步"

# 更新分类
ctx update category 产品

# 添加项目描述
ctx update brief "AI 驱动的播客生成平台"

# 更新分支
ctx update branch feature/new-feature
```

### 切换项目

```bash
# 使用 ctx switch
ctx switch example-project

# 或使用 shell 集成的 go 命令
go example-project
```

### 迁移旧格式

```bash
cd ~/workspace/old-project
ctx migrate
```

## 🛠️ 命令参考

| 命令 | 功能 | 示例 |
|------|------|------|
| `ctx` | 显示完整项目上下文 | `ctx` |
| `ctx status` | 显示紧凑状态（单行） | `ctx status` |
| `ctx ls` | 列出所有项目（按状态分组） | `ctx ls` |
| `ctx switch <项目>` | 切换到指定项目 | `ctx switch example-project` |
| `ctx init` | 初始化新项目 | `ctx init` |
| `ctx update <字段> <值>` | 更新项目字段 | `ctx update status paused` |
| `ctx migrate` | 迁移旧格式到融合版 | `ctx migrate` |

### 支持的字段

`ctx update` 支持更新以下字段：

| 字段 | 说明 | 示例值 |
|------|------|--------|
| `status` | 项目状态 | `active`, `paused`, `completed` |
| `category` | 项目分类 | `探索性`, `产品`, `临时`, `学习` |
| `current_focus` | 当前工作重点 | `"实现音频同步"` |
| `brief` | 项目描述 | `"AI 驱动的播客平台"` |
| `branch` | Git 分支 | `feature/new-feature` |
| `next_steps` | 下一步计划 | `"完成测试"` |
| `project_type` | 技术类型 | `flask-api` |

## 📁 项目结构

```
context-manager/
├── .github/
│   ├── workflows/           # CI/CD 配置
│   │   ├── ci.yml
│   │   └── release.yml
│   ├── ISSUE_TEMPLATE/      # Issue 模板
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
├── scripts/
│   └── context_manager.py   # 核心脚本
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_context_manager.py
├── ctx                      # 可执行命令
├── setup.sh                 # 安装脚本
├── shell-integration.sh     # Shell 集成
├── SKILL.md                 # 完整文档
├── MIGRATION.md             # 迁移指南
├── CONTRIBUTING.md          # 贡献指南
├── CHANGELOG.md             # 变更日志
├── LICENSE                  # MIT 许可证
├── pyproject.toml           # 项目配置
├── .gitignore
└── README.md
```

## 📋 context.md 格式

### 融合版模板

```yaml
---
# ============ 基本信息 ============
project: 项目名称
created: 2025-01-27          # 创建日期
last_session: 2025-01-27      # 最后工作日期
session_count: 5             # 总会话数

# ============ 状态分类 ============
status: active               # active | paused | completed
category: 探索性             # 探索性 | 产品 | 临时 | 学习
project_type: flask-api      # 技术类型（可选）

# ============ 工作追踪 ============
current_focus: "当前工作重点"
next_steps: "下一步计划"
branch: main                 # 当前 Git 分支

# ============ 项目描述 ============
brief: "一句话描述项目目标"

# ============ 技术栈 ============
stack:
  - Python/Flask
  - Vue 3

---

## 📋 待办事项

### P0 [本周]
- [ ] 待办项 1
- [ ] 待办项 2

### P1 [本月]
- [ ] 待办项 3

## 📝 会话记录

### 2025-01-27 (会话 #5)
**主题**: 实现音频同步
**分支**: feature/audio-sync
**完成**:
- ✅ 完成音频文件上传
- ✅ 实现音频同步逻辑

## 📝 笔记/决策
<!-- 重要决策、问题记录 -->

## 🔗 相关资源
<!-- 链接、文档等 -->
```

## 🎯 使用场景

### 场景 1: 每日工作启动

```bash
# 查看所有项目状态
ctx ls

# 切换到要处理的项目
go example-project

# 查看项目详情
ctx
```

### 场景 2: 完成工作，暂停项目

```bash
# 更新状态为暂停
ctx update status paused
ctx update current_focus "已完成音频同步功能"

# 切换到下一个项目
go demo-project
```

### 场景 3: 恢复项目工作

```bash
# 切换到项目
go tool-demo

# 更新状态为活跃
ctx update status active
ctx update current_focus "修复卦象显示 bug"
# session_count 自动 +1
```

### 场景 4: 创建新探索项目

```bash
mkdir ~/workspace/new-experiment
cd ~/workspace/new-experiment

# 初始化项目
ctx init

# 编辑项目信息
ctx update category 探索性
ctx update brief "测试新技术的实验性项目"
```

## 🆚 版本对比

### v2.0 新特性

相比 v1.0 版本，v2.0 融合版新增：

| 特性 | v1.0 | v2.0 融合版 |
|------|------|------------|
| 格式检测 | ❌ | ✅ 自动识别 |
| 会话计数 | ✅ | ✅ |
| 分支追踪 | ✅ | ✅ |
| 状态管理 | ❌ | ✅ active/paused/completed |
| 项目分类 | project_type | ✅ category + project_type |
| 项目描述 | ❌ | ✅ brief |
| 创建日期 | ❌ | ✅ created |
| 会话记录 | ✅ | ✅ 完全保留 |
| 待办结构 | ❌ | ✅ P0/P1 优先级 |
| 智能迁移 | ❌ | ✅ 一键迁移 |

## 📊 对比其他方案

| 特性 | Context Manager | planning-with-files | beads |
|------|----------------|---------------------|-------|
| 实现时间 | ✅ 10 分钟 | 30 分钟 | 2 小时 |
| 学习曲线 | ✅ 零 | 低 | 中 |
| 依赖 | ✅ 无 | 无 | Git + bd CLI |
| 会话追踪 | ✅ | ❌ | ❌ |
| 状态管理 | ✅ | ✅ | ✅ |
| 匹配需求 | ✅ 95% | 60% | 40% |

## 🤝 贡献

我们欢迎所有形式的贡献！

### 快速贡献流程

1. 🍴 Fork 本仓库
2. 🔨 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 💾 提交更改 (`git commit -m 'feat: add some amazing feature'`)
4. 📤 推送到分支 (`git push origin feature/AmazingFeature`)
5. 🎯 开启 Pull Request

详细贡献指南请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

### 开发环境设置

```bash
# 克隆你的 fork
git clone https://github.com/YOUR_USERNAME/context-manager.git
cd context-manager

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black scripts/ tests/
isort scripts/ tests/

# 代码检查
ruff check scripts/
```

## 📚 相关文档

- **[SKILL.md](SKILL.md)** - 完整技能文档
- **[MIGRATION.md](MIGRATION.md)** - 详细迁移指南
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - 贡献指南
- **[CHANGELOG.md](CHANGELOG.md)** - 变更日志

## ❓ FAQ

<details>
<summary><b>Q: ctx migrate 提示"已经是融合版"怎么办？</b></summary>

A: 说明项目已经是最新格式，无需迁移。你可以继续使用所有功能。
</details>

<details>
<summary><b>Q: 迁移后看到注释"请根据实际情况修改"需要删除吗？</b></summary>

A: 这些注释只是提醒，不删除也不影响功能。如果要删除，使用文本编辑器手动删除即可。
</details>

<details>
<summary><b>Q: session_count 没有自动增加？</b></summary>

A: 确保使用 `ctx update` 而不是手动编辑文件。每次 `ctx update` 都会自动增加 session_count。
</details>

<details>
<summary><b>Q: 支持自定义 workspace 路径吗？</b></summary>

A: 支持。编辑 `scripts/context_manager.py` 中的 `WORKSPACE_ROOT` 变量。
</details>

<details>
<summary><b>Q: 如何回退到旧格式？</b></summary>

A: 如果使用 Git，可以执行：`git checkout .claude/context.md`
</details>

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🌟 致谢

- 感谢所有为改进此工具做出贡献的开发者！
- 感谢 [Claude Code](https://claude.com/claude-code) 提供的强大 AI 辅助开发能力
- 灵感来源于实际多项目并行开发需求

---

<div align="center">

**[⬆ 返回顶部](#context-manager-enhanced)**

Made with ❤️ by Context Manager Team

</div>
