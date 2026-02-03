---
# ============ 基本信息 ============
project: context-manager-skill
created: 2026-02-03
last_session: 2026-02-04
session_count: 12

# ============ 状态分类 ============
status: active
category: 产品
project_type: cli-python-tool

# ============ 工作追踪 ============
current_focus: "完成 v0.2.0 - 区分工作区和项目 context"
next_steps: "准备发布 v0.2.0 到 PyPI"
branch: main

# ============ 项目描述 ============
brief: "工作区上下文管理工具 - 专为多项目并行开发设计，让你的大脑专注于创造而不是记忆"

# ============ 技术栈 ============
stack:
  - Python 3.9+
  - GitHub Actions
  - pytest
  - Claude Code Skill

---

## 📋 待办事项

### P0 [本周]
- [x] ✅ 完成项目初始化
- [x] ✅ 编写完整 README（1051行）
- [x] ✅ 配置 GitHub Actions CI/CD
- [x] ✅ 发布到 PyPI (ctxmgr v0.1.4)
- [x] ✅ 区分工作区和项目 context 模板
- [x] ✅ 实现 ctx init --workspace/--project 选项
- [ ] 发布 v0.2.0 到 PyPI

### P1 [本月]
- [ ] 增加测试覆盖率到 80%+
- [ ] 添加 ctx migrate 智能检测
- [ ] 实现会话记录自动生成
- [ ] 添加 shell 集成文档

## 📝 会话记录

### 2026-02-04 (会话 #13)
**主题**: 实现工作区和项目 context 区分
**分支**: main
**完成**:
- ✅ 添加 `ctx init --type` 选项
- ✅ 实现两种不同的模板生成函数
- ✅ 更新 SKILL.md 文档，添加详细说明
- ✅ 添加工作区 vs 项目 context 对比
- ✅ 创建项目自己的 context.md（吃自己的狗粮）
- ✅ 更新版本到 v0.2.0
**决策**:
- 区分元项目管理（工作区）和具体业务（项目）
- 自动检测：目录名包含 workspace → 工作区模板

### 2026-02-04 (会话 #12)
**主题**: 完成项目发布和文档优化
**分支**: main
**完成**:
- ✅ 重新组织 README 结构（场景驱动）
- ✅ 深度优化 Trade-off 分析
- ✅ 配置 GitHub Actions CI/CD
- ✅ 添加 GitHub Topics（15个）
- ✅ 发布 ctxmgr v0.1.4 到 PyPI
- ✅ 安装 skill 到本地 Claude Code
**决策**:
- 包名改为 ctxmgr（context-manager 已被占用）
- 使用密码认证而非 Trusted Publishing

### 2026-02-03 (会话 #1-11)
**主题**: 项目开发
**完成**:
- ✅ 实现 context_manager.py 核心功能
- ✅ 支持双格式解析（v1/v2）
- ✅ 添加 ctx ls, switch, update, migrate 命令
- ✅ 编写完整测试（26个测试用例）
- ✅ 创建 SKILL.md 文档

## 📝 笔记/决策

### 设计决策
1. **半结构化格式**：YAML frontmatter + Markdown，平衡结构和灵活性
2. **自动化优先**：session_count 自动递增，减少认知负荷
3. **双格式兼容**：向后兼容 v1，渐进式迁移
4. **工作区 vs 项目 context**：
   - 工作区 context：元项目管理（工具链、规范、跨项目任务）
   - 项目 context：具体业务（功能、待办、会话历史）

### TODO: 改进方向
- [ ] 添加 workspace 模板选项 ✅
- [ ] 实现智能格式检测和迁移建议
- [ ] 添加 context.md 验证命令
- [ ] 支持自定义模板

## 🔗 相关资源
- **GitHub**: https://github.com/leether/context-manager-skill
- **PyPI**: https://pypi.org/project/ctxmgr/
- **Issue Tracker**: https://github.com/leether/context-manager-skill/issues
- **文档**: SKILL.md, README.md, MIGRATION.md
