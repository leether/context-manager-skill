# Contributing to Context Manager

感谢你有兴趣为 Context Manager 项目做出贡献！本文档将指导你如何参与项目开发。

## 📋 目录

- [行为准则](#行为准则)
- [开发环境设置](#开发环境设置)
- [代码规范](#代码规范)
- [提交信息规范](#提交信息规范)
- [Pull Request 流程](#pull-request-流程)
- [测试指南](#测试指南)
- [报告问题](#报告问题)

## 🤝 行为准则

参与此项目即表示你同意遵守我们的行为准则：

- 尊重所有贡献者
- 欢迎不同观点和建设性反馈
- 专注于对社区最有利的事情
- 对其他社区成员表示同理心

## 🛠️ 开发环境设置

### 1. Fork 和 Clone

```bash
# Fork 仓库，然后 clone
git clone https://github.com/YOUR_USERNAME/context-manager.git
cd context-manager

# 添加上游仓库
git remote add upstream https://github.com/original-author/context-manager.git
```

### 2. 创建虚拟环境

```bash
# 使用 venv
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 或使用 uv
uv venv
source .venv/bin/activate
```

### 3. 安装开发依赖

```bash
# 安装项目及开发依赖
pip install -e ".[dev]"

# 或使用 uv
uv pip install -e ".[dev]"
```

### 4. 运行测试

```bash
# 运行所有测试
pytest

# 运行带覆盖率的测试
pytest --cov=scripts --cov-report=html

# 运行特定测试
pytest tests/test_context_manager.py
```

### 5. 代码检查

```bash
# 运行 linting
ruff check scripts/

# 自动修复问题
ruff check --fix scripts/

# 格式化代码
black scripts/
isort scripts/
```

## 📐 代码规范

### Python 代码风格

我们遵循以下代码规范：

- **PEP 8**: Python 代码风格指南
- **Black**: 代码格式化工具
- **Ruff**: 快速的 Python linter
- **isort**: import 排序
- **Type Hints**: 使用类型注解

### 命名约定

- **函数和变量**: `snake_case`
- **类名**: `PascalCase`
- **常量**: `UPPER_SNAKE_CASE`
- **私有方法**: `_leading_underscore`
- **命令行参数**: `kebab-case`

### 文档字符串

使用 Google 风格的文档字符串：

```python
def parse_context(content: str) -> dict:
    """解析 context.md 内容（双格式兼容）。

    Args:
        content: context.md 文件内容

    Returns:
        包含解析结果的字典，包括项目信息、状态、分类等字段

    Examples:
        >>> info = parse_context(file_content)
        >>> print(info['project'])
        'my-project'
    """
    pass
```

### 代码组织

- 保持函数简短（< 50 行）
- 每个函数只做一件事
- 使用描述性的变量名
- 添加注释说明复杂逻辑

## 📝 提交信息规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

### 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型 (type)

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 代码重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具链相关
- `ci`: CI/CD 相关

### 示例

```bash
git commit -m "feat(parser): 支持多行 YAML 值解析

- 添加多行字符串解析逻辑
- 更新单元测试覆盖边界情况

Closes #123"
```

## 🔄 Pull Request 流程

### 1. 创建功能分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/bug-description
```

### 2. 进行更改

- 编写代码
- 添加测试
- 更新文档
- 运行测试和 linting

### 3. 提交更改

```bash
git add .
git commit -m "feat: add your feature"
```

### 4. 同步上游更改

```bash
git fetch upstream
git rebase upstream/main
```

### 5. 推送到你的 fork

```bash
git push origin feature/your-feature-name
```

### 6. 创建 Pull Request

在 GitHub 上创建 PR，包含：

- 清晰的标题
- 详细的描述
- 关联的 Issue
- 截图（如适用）
- 测试说明

### PR 标题模板

```
<type>: <short description>

### 描述
详细说明你的更改

### 更改类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 破坏性更改
- [ ] 文档更新

### 测试
描述你如何测试这些更改

### 检查清单
- [ ] 代码遵循项目规范
- [ ] 添加了必要的测试
- [ ] 所有测试通过
- [ ] 更新了相关文档
- [ ] 添加了 CHANGELOG 条目（如适用）
```

## 🧪 测试指南

### 编写测试

使用 `pytest` 编写测试：

```python
# tests/test_context_manager.py
import pytest
from scripts.context_manager import parse_context

def test_parse_context_with_v2_format():
    """测试 v2 格式解析"""
    content = """---
project: test-project
created: 2024-01-01
status: active
category: 探索性
---
"""
    result = parse_context(content)
    assert result["project"] == "test-project"
    assert result["status"] == "active"
    assert result["category"] == "探索性"

def test_parse_context_with_missing_fields():
    """测试缺少字段的处理"""
    content = """---
project: minimal
---
"""
    result = parse_context(content)
    assert result["project"] == "minimal"
    assert result["status"] == "unknown"
```

### 运行特定测试

```bash
# 运行特定文件
pytest tests/test_context_manager.py

# 运行特定测试
pytest tests/test_context_manager.py::test_parse_context_with_v2_format

# 运行匹配关键字的测试
pytest -k "parse_context"

# 显示打印输出
pytest -s
```

### 测试覆盖率

```bash
# 生成覆盖率报告
pytest --cov=scripts --cov-report=html

# 在浏览器中查看
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
```

## 🐛 报告问题

### 报告 Bug

使用 [Bug Report 模板](.github/ISSUE_TEMPLATE/bug.md) 并包含：

1. **问题描述**: 清晰描述问题
2. **复现步骤**: 详细说明如何复现
3. **期望行为**: 你期望发生什么
4. **实际行为**: 实际发生了什么
5. **环境信息**:
   - 操作系统
   - Python 版本
   - 项目版本
6. **截图/日志**: 如果适用

### 功能请求

使用 [Feature Request 模板](.github/ISSUE_TEMPLATE/feature.md) 并说明：

1. **功能描述**: 你想要什么功能
2. **使用场景**: 为什么需要这个功能
3. **建议方案**: 你认为应该如何实现
4. **替代方案**: 你考虑过的其他方案

## 📚 资源

- [项目文档](README.md)
- [API 文档](SKILL.md)
- [迁移指南](MIGRATION.md)
- [变更日志](CHANGELOG.md)
- [问题追踪](https://github.com/YOUR_USERNAME/context-manager/issues)
- [讨论区](https://github.com/YOUR_USERNAME/context-manager/discussions)

## 💬 获取帮助

如果你有任何问题：

1. 查看 [文档](README.md) 和 [FAQ](#)
2. 搜索 [已有 Issues](https://github.com/YOUR_USERNAME/context-manager/issues)
3. 在 [Discussions](https://github.com/YOUR_USERNAME/context-manager/discussions) 中提问
4. 加入我们的社区聊天室（如有）

## 🌟 成为维护者

活跃的贡献者可能会被邀请成为项目维护者。维护者负责：

- 审查和合并 PR
- 回答问题和讨论
- 发布新版本
- 引导新贡献者

感谢你的贡献！🎉
