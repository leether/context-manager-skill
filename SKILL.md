# Context Manager Enhanced v2.0 - 工作区上下文管理（融合版）

自动检测和恢复工作区记忆，支持多项目快速切换、会话追踪、智能迁移。

## 激活条件

在任意目录启动时自动激活，或在项目间切换时调用。

## 核心功能

### 1. 双格式兼容
- 自动识别并解析 v1（旧版）和 v2（融合版）格式
- 无缝兼容，无需手动修改
- 智能字段映射（如 `project_type` → `category`）

### 2. 项目状态管理
- 检测 `.claude/context.md`
- 自动显示项目摘要和待办
- 支持状态分类（active/paused/completed）
- 支持项目分类（探索性/产品/临时/学习）

### 3. 会话追踪
- 自动记录会话次数（`session_count`）
- 追踪当前 Git 分支（`branch`）
- 保留完整会话历史

### 4. 多项目切换
- 快速列出所有项目及状态
- 在项目间快速切换
- 自动加载目标项目上下文

### 5. 智能迁移
- 一键迁移旧格式到融合版
- 保留所有原有内容
- 自动合并字段

## 命令参考

### `ctx` - 显示当前项目上下文
```
ctx
```
显示完整的项目状态、待办列表、会话数、分支等信息。

### `ctx status` - 简要状态
```
ctx status
```
显示紧凑版项目状态（单行），包括：
- 项目名和状态图标
- 状态分类和项目类型
- 当前 Git 分支
- 当前焦点
- 待办数量和会话数
- 上次工作时间

### `ctx ls` - 列出所有项目
```
ctx ls
```
按状态分组显示所有项目：
- 🟢 进行中 (active)
- 🟡 已暂停 (paused)
- ✅ 已完成 (completed)
- ⚪ 其他

每个项目显示：
- 项目名称
- 当前焦点
- 会话计数（如果有）

### `ctx switch <项目名>` - 切换项目
```
ctx switch example-project
```
切换到指定项目并显示其状态。

### `ctx init` - 初始化 context
```
ctx init                           # 自动检测类型
ctx init --type workspace          # 工作区模板
ctx init --type project            # 项目模板
ctx init -t workspace             # 简写
```

**两种 Context 类型**:

1. **工作区 Context** (`--type workspace`)
   - 用途: 元项目管理（工具链、规范、跨项目任务）
   - 适用: 工作区根目录、包含多个项目的容器
   - 内容: 工作区级别任务、工具链配置、项目组合管理

2. **项目 Context** (`--type project`)
   - 用途: 具体业务（功能、待办、会话历史）
   - 适用: 具体项目目录
   - 内容: 业务功能、技术实现、项目状态

**自动检测** (`--type auto` 默认):
- 目录名包含 'workspace' → 工作区模板
- 其他目录 → 项目模板

### `ctx update <字段> <值>` - 更新字段
```
ctx update status paused
ctx update current_focus "修复音频播放问题"
ctx update category 产品
ctx update brief "AI 驱动的播客生成平台"
ctx update branch feature/audio-player
```
快速更新 context.md 中的字段，支持的字段：
- `project` - 项目名称
- `status` - 状态 (active/paused/completed)
- `category` - 分类 (探索性/产品/临时/学习)
- `project_type` - 技术类型
- `current_focus` - 当前焦点
- `next_steps` - 下一步计划
- `brief` - 项目描述
- `branch` - Git 分支

**注意**：每次更新会自动：
- 更新 `last_session` 为今天
- 增加 `session_count` 计数

### `ctx migrate` - 迁移旧格式
```
ctx migrate
```
自动检测并迁移旧版 context.md 到融合版：
- 自动识别格式版本（v1/v2/mixed）
- 保留所有原有内容和会话记录
- 添加新字段（status、category、brief 等）
- 智能映射旧字段（project_type → category）

## Shell 集成

在 `~/.bashrc` 或 `~/.zshrc` 中添加：

```bash
source ~/.claude/skills/context-manager/shell-integration.sh
```

然后可以使用：

```bash
repos              # 列出所有项目
go <项目名>         # 快速切换并显示状态
ctx                # 等同于 ~/.claude/skills/context-manager/ctx
```

## context.md 结构（融合版）

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
project_type: flask-api      # 技术类型（可选，兼容旧版）

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
  - ListenHub API

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

### 2025-01-26 (会话 #4)
**主题**: 修复播放器崩溃
**完成**:
- ✅ 定位崩溃原因
- ✅ 修复内存泄漏

## 📝 笔记/决策
<!-- 重要决策、问题记录 -->

## 🔗 相关资源
<!-- 链接、文档等 -->
```

## 格式版本说明

### v1 格式（旧版）
```yaml
---
project: name
project_type: cli-tool-python
last_session: "2025-01-30 15:35"
current_focus: "..."
branch: main
session_count: 1
---
```

特点：
- 使用 `project_type` 而不是 `category`
- 有 `branch` 和 `session_count` 追踪
- 有详细的会话记录结构

### v2 格式（新版）
```yaml
---
project: name
created: 2025-01-27
last_session: 2025-01-27
status: active
category: 探索性
current_focus: "..."
next_steps: "..."
brief: "..."
stack: [...]
---
```

特点：
- 使用 `status` 和 `category` 标准字段
- 有 `created` 和 `next_steps` 字段
- 结构化的项目描述

### 融合版（推荐）
结合两种格式的优点：
- 保留 v1 的会话追踪能力
- 使用 v2 的状态管理字段
- 双向兼容，自动识别

## 使用场景

### 场景 1: 启动工作会话
```bash
cd ~/workspace/example-project
ctx              # 查看项目状态（显示会话数和分支）
```

### 场景 2: 项目间切换
```bash
repos            # 查看所有项目
go example-project   # 切换到 example-project（自动显示状态）
# 或
ctx switch aiplus
```

### 场景 3: 更新工作状态
```bash
ctx update current_focus "实现音频同步"
# 自动更新 last_session，增加 session_count
```

### 场景 4: 暂停/恢复项目
```bash
ctx update status paused    # 暂停项目
ctx update status active    # 恢复项目
```

### 场景 5: 迁移旧项目
```bash
cd ~/workspace/old-project
ctx migrate      # 一键迁移到融合版
```

### 场景 6: 创建新项目
```bash
mkdir ~/workspace/new-project
cd ~/workspace/new-project
ctx init         # 创建融合版模板
```

### 场景 7: 初始化工作区 context
```bash
cd ~/workspace
ctx init --type workspace    # 或: ctx init -t workspace
```

### 场景 8: 初始化项目 context
```bash
cd ~/workspace/my-project
ctx init --type project      # 或: ctx init -t project
```

## 工作区 vs 项目 Context

### 核心区别

| 维度 | 工作区 Context | 项目 Context |
|------|---------------|-------------|
| **粒度** | 宏观、跨项目 | 微观、具体项目 |
| **时间跨度** | 长期（月/年） | 短期（周/天） |
| **任务类型** | 工具链、规范、协调 | 功能、Bug、优化 |
| **会话内容** | 工作流改进决策 | 功能实现进展 |
| **关注点** | 效率、质量、协作 | 用户价值、业务逻辑 |

### 工作区 Context 适用场景

**何时使用** `--type workspace`:
- ✅ 工作区根目录
- ✅ 需要记录跨项目的任务
- ✅ 管理工具链和规范
- ✅ 追踪项目组合状态

**包含内容**:
```markdown
## 🎯 工作区级别任务
- [ ] 统一 CI/CD 配置
- [ ] 建立代码规范
- [ ] 优化项目切换流程

## 📊 项目组合管理
### 进行中
- podcast-app
- context-manager-skill

## 🔧 工具链配置
- Python 版本管理
- GitHub Actions 模板
```

### 项目 Context 适用场景

**何时使用** `--type project`:
- ✅ 具体业务项目
- ✅ 需要追踪功能开发
- ✅ 记录会话历史
- ✅ 管理待办事项

**包含内容**:
```markdown
## 📋 待办事项
### P0 [本周]
- [ ] 完成音频上传
- [ ] 实现同步逻辑

## 📝 会话记录
### 2026-02-04 (会话 #5)
**主题**: 音频同步
**完成**:
- ✅ 实现文件上传
```

### 双层上下文系统

```
工作区层 (战略)
├── 工具链配置
├── 代码规范
├── 跨项目任务
└── 项目组合管理
    ↓ 协调
项目层 (战术)
├── 业务功能
├── 技术实现
├── 待办事项
└── 会话历史
```

**实践建议**:
1. **工作区 context** - 月度/季度回顾时更新
2. **项目 context** - 每次会话时更新
3. **定期同步** - 将项目进展同步到工作区 context

## 依赖

- Python 3.9+
- 无第三方依赖

## 配置

默认 workspace 路径：`~/workspace`

如需自定义，修改 `scripts/context_manager.py` 中的 `WORKSPACE_ROOT`。

## 最佳实践

1. **每次切换项目时使用 `ctx`** - 快速恢复上下文，查看会话历史
2. **定期更新 `current_focus`** - 保持焦点清晰，便于回顾
3. **使用 `status` 字段** - 标记项目状态，便于筛选
4. **填写 `category` 字段** - 区分探索性/产品/临时项目
5. **维护会话记录** - 记录每次会话的关键进展
6. **更新 `branch` 字段** - 追踪当前工作分支
7. **维护待办列表** - 保持任务可视化

## 字段说明

### 基本信息
- `project` - 项目名称
- `created` - 项目创建日期
- `last_session` - 最后工作日期（自动更新）
- `session_count` - 总会话数（自动递增）

### 状态分类
- `status` - 项目状态
  - `active` - 正在开发
  - `paused` - 暂时暂停
  - `completed` - 已完成
- `category` - 项目类型
  - `探索性` - 初步探索
  - `产品` - 产品级项目
  - `临时` - 临时任务
  - `学习` - 学习练手
- `project_type` - 技术类型（兼容旧版）

### 工作追踪
- `current_focus` - 当前工作重点
- `next_steps` - 下一步计划
- `branch` - 当前 Git 分支

### 项目描述
- `brief` - 一句话描述项目目标
- `stack` - 技术栈列表

## 迁移指南

如果你有旧版 context.md，使用以下步骤迁移：

1. **检查当前格式**
   ```bash
   ctx status  # 会显示格式版本信息
   ```

2. **执行迁移**
   ```bash
   ctx migrate
   ```

3. **确认和修正**
   ```bash
   # 编辑 context.md，确认以下字段：
   ctx update status active      # 根据实际情况
   ctx update category 产品      # 根据实际情况
   ctx update brief "项目目标"   # 添加项目描述
   ```

4. **验证结果**
   ```bash
   ctx ls       # 检查项目分类
   ctx status   # 检查状态显示
   ```

## 故障排除

### Q: ctx status 显示格式版本为 unknown
A: 可能是格式混合，运行 `ctx migrate` 统一格式。

### Q: 更新字段后出现重复
A: 迁移后的模板可能有注释，手动编辑删除注释行。

### Q: session_count 没有自动增加
A: 确保使用 `ctx update` 而不是手动编辑文件。

### Q: 旧版内容丢失了
A: `ctx migrate` 会保留所有原有内容，包括会话记录。

## 更新日志

### v2.0 (2026-02-03) - 融合版
- ✅ 双格式解析器，自动识别 v1/v2
- ✅ 添加 `ctx migrate` 智能迁移命令
- ✅ 融合模板，结合两种格式优点
- ✅ 会话计数自动递增
- ✅ 分支追踪显示
- ✅ 支持 8 个字段更新
- ✅ 增强的状态显示

### v1.0 (2026-02-03) - 增强版
- ✅ `ctx ls` 命令
- ✅ `ctx status` 命令
- ✅ `ctx init` 命令
- ✅ `ctx switch` 命令
- ✅ `ctx update` 命令
- ✅ Shell 集成脚本

### 原版
- 基础的上下文显示功能
