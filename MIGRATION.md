# Context Manager 迁移指南

本指南帮助你将旧版 context.md 迁移到融合版格式。

## 什么是融合版？

融合版结合了两种格式的优点：

| 特性 | v1（旧版） | v2（新版） | 融合版 |
|------|-----------|-----------|--------|
| 状态管理 | ❌ | ✅ active/paused/completed | ✅ |
| 项目分类 | project_type | ✅ category | ✅ |
| 会话追踪 | ✅ session_count | ❌ | ✅ |
| 分支追踪 | ✅ branch | ❌ | ✅ |
| 会话记录 | ✅ 详细 | ❌ | ✅ |
| 项目描述 | ❌ | ✅ brief | ✅ |
| 创建日期 | ❌ | ✅ created | ✅ |

## 快速迁移

### 一键迁移命令

```bash
cd ~/workspace/your-project
ctx migrate
```

就这么简单！迁移命令会：
1. ✅ 自动检测格式版本
2. ✅ 保留所有原有内容
3. ✅ 添加新字段
4. ✅ 智能映射字段（如 project_type → category）
5. ✅ 保留会话记录

### 迁移示例

**迁移前（v1 格式）**：
```yaml
---
project: iching-calculator
project_type: cli-tool-python
last_session: "2025-01-30 15:35"
current_focus: "创建三硬币起卦解卦程序"
branch: main
session_count: 1
---

## 本次会话概览
**会话主题**: 从 tangshi 项目热切换
**已完成工作**:
- ✅ 创建 iching.py
```

**迁移后（融合版）**：
```yaml
---
# ============ 基本信息 ============
project: iching-calculator
created: 2026-02-03
last_session: 2026-02-03
session_count: 1

# ============ 状态分类 ============
status: active                 # 请根据实际情况修改
category: cli-tool-python      # 从 project_type 映射
project_type: cli-tool-python

# ============ 工作追踪 ============
current_focus: "创建三硬币起卦解卦程序"
next_steps: ""
branch: main

# ============ 项目描述 ============
brief: "请用一句话描述这个项目的目标"

# ============ 技术栈 ============
stack:
  - 语言/框架

---

## 本次会话概览
**会话主题**: 从 tangshi 项目热切换
**已完成工作**:
- ✅ 创建 iching.py
```

## 迁移后清单

迁移完成后，建议确认以下内容：

### 1. 确认状态

```bash
ctx update status active      # 根据实际情况选择
# 选项: active | paused | completed
```

### 2. 确认分类

```bash
# 保留原 project_type 作为 category
# 或根据实际情况修改：
ctx update category 探索性     # 探索性 | 产品 | 临时 | 学习
```

### 3. 添加项目描述

```bash
ctx update brief "AI 驱动的周易起卦解卦工具"
```

### 4. 验证结果

```bash
ctx status       # 检查状态显示
ctx ls          # 检查项目分类
```

## 批量迁移

如果要迁移所有项目：

```bash
# 方式 1: 手动逐个迁移
for dir in ~/workspace/*/.claude/context.md; do
    project=$(dirname $(dirname $dir))
    cd "$project"
    ~/.claude/skills/context-manager/ctx migrate
done

# 方式 2: 交互式迁移
repos           # 查看所有项目
# 然后对每个项目执行：
cd ~/workspace/project-name
ctx migrate
```

## 字段映射表

| 旧版字段 | 融合版字段 | 说明 |
|---------|-----------|------|
| `project_type` | `category` + `project_type` | 两者都保留 |
| - | `status` | 新增，默认为 active |
| - | `created` | 新增，默认为迁移日期 |
| - | `next_steps` | 新增，默认为空 |
| - | `brief` | 新增，需要手动填写 |
| `branch` | `branch` | 保留 |
| `session_count` | `session_count` | 保留 |
| `current_focus` | `current_focus` | 保留 |

## 常见问题

### Q: 迁移后我的内容会丢失吗？

A: **不会**。`ctx migrate` 会保留所有原有内容，包括：
- ✅ 所有 YAML 字段
- ✅ 会话记录
- ✅ 待办事项
- ✅ 笔记/决策
- ✅ 相关资源

### Q: 迁移后还能用旧版本吗？

A: **可以**。解析器支持双格式，但建议迁移到融合版以获得新功能。

### Q: 我不喜欢迁移后的格式怎么办？

A: 迁移会创建备份（如果使用 Git），你可以：
```bash
git checkout .claude/context.md  # 恢复旧版本
```

### Q: 迁移后需要手动修改什么？

A: 通常需要确认：
1. `status` - 项目当前状态
2. `brief` - 项目一句话描述（新增字段）
3. 删除迁移提示注释

### Q: 会话记录会保留吗？

A: **完全保留**。迁移时会话记录部分原封不动地保留在文件中。

## 高级迁移

### 自定义迁移模板

如果需要自定义迁移规则，编辑 `scripts/context_manager.py` 中的 `cmd_migrate` 函数。

### 部分迁移

如果只想添加部分字段，可以手动编辑：

```bash
# 手动添加这些字段到 frontmatter
created: 2025-01-27
status: active
category: 探索性
brief: "项目描述"
```

## 迁移检查清单

- [ ] 执行 `ctx migrate`
- [ ] 检查 `status` 字段是否正确
- [ ] 检查 `category` 字段是否正确
- [ ] 填写 `brief` 字段
- [ ] 删除迁移提示注释（可选）
- [ ] 验证 `ctx status` 显示正确
- [ ] 验证 `ctx ls` 分类正确
- [ ] 测试 `ctx update` 是否正常工作

## 需要帮助？

如果遇到问题：

1. 查看故障排除部分（SKILL.md）
2. 运行 `ctx status` 查看详细信息
3. 检查 `.claude/context.md` 文件内容
4. 提交 issue：https://github.com/your-repo/issues

## 迁移案例

### 案例 1: 简单项目

**迁移前**：
```yaml
---
project: simple-app
last_session: "2025-01-30"
current_focus: "初始化"
---
```

**迁移后**：
```yaml
---
# ============ 基本信息 ============
project: simple-app
created: 2026-02-03
last_session: 2026-02-03
session_count: 1

# ============ 状态分类 ============
status: active
category: unknown

# ============ 工作追踪 ============
current_focus: "初始化"
next_steps: ""
branch: main

# ============ 项目描述 ============
brief: "请用一句话描述这个项目的目标"

# ============ 技术栈 ============
stack:
  - 语言/框架

---
```

**后续操作**：
```bash
ctx update category 学习
ctx update brief "简单的学习项目"
```

### 案例 2: 复杂项目（有会话记录）

**迁移前**：
```yaml
---
project: complex-app
project_type: flask-api
last_session: "2025-01-30 16:40"
current_focus: "实现音频同步"
branch: feature/audio
session_count: 12
---

## 本次会话概览
**主题**: 音频同步

## 已完成工作
- ✅ 完成音频上传
- ✅ 实现同步逻辑
```

**迁移后**：
```yaml
---
# ============ 基本信息 ============
project: complex-app
created: 2026-02-03
last_session: 2026-02-03
session_count: 12

# ============ 状态分类 ============
status: active
category: flask-api
project_type: flask-api

# ============ 工作追踪 ============
current_focus: "实现音频同步"
next_steps: ""
branch: feature/audio

# ============ 项目描述 ============
brief: "请用一句话描述这个项目的目标"

# ============ 技术栈 ============
stack:
  - 语言/框架

---

## 本次会话概览
**主题**: 音频同步

## 已完成工作
- ✅ 完成音频上传
- ✅ 实现同步逻辑
```

**后续操作**：
```bash
ctx update category 产品
ctx update brief "音频同步 API"
```

## 总结

融合版迁移是**安全且向后兼容**的：

✅ **自动识别** - 无需手动判断格式
✅ **保留内容** - 不会丢失任何数据
✅ **智能映射** - 自动转换字段
✅ **可逆操作** - 使用 Git 可随时回退
✅ **渐进式** - 可以逐步迁移，不必一次性完成

开始享受融合版的强大功能吧！
