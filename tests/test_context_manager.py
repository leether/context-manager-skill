"""Tests for context_manager.py"""

import os

import pytest

from scripts.context_manager import (
    get_context_dir,
    get_context_file,
    parse_context,
)


class TestParseContext:
    """测试 context.md 解析功能"""

    def test_parse_v2_format(self):
        """测试解析 v2 格式"""
        content = """---
project: test-project
created: 2024-01-01
last_session: "2024-01-05"
session_count: 5
status: active
category: 探索性
current_focus: "实现核心功能"
next_steps: "完成测试"
brief: "测试项目"
branch: main
---

## 待办事项
- [ ] 任务1
- [ ] 任务2
"""
        result = parse_context(content)

        assert result["project"] == "test-project"
        assert result["created"] == "2024-01-01"
        assert result["last_session"] == "2024-01-05"
        assert result["session_count"] == 5
        assert result["status"] == "active"
        assert result["category"] == "探索性"
        assert result["current_focus"] == "实现核心功能"
        assert result["next_steps"] == "完成测试"
        assert result["brief"] == "测试项目"
        assert result["branch"] == "main"
        assert result["format_version"] == "v2"

    def test_parse_v1_format(self):
        """测试解析 v1 格式（旧版）"""
        content = """---
project: old-project
project_type: flask-api
last_session: "2024-01-05"
current_focus: "旧项目"
branch: develop
session_count: 10
---
"""
        result = parse_context(content)

        assert result["project"] == "old-project"
        assert result["project_type"] == "flask-api"
        assert result["category"] == "flask-api"  # 从 project_type 映射
        assert result["current_focus"] == "旧项目"
        assert result["branch"] == "develop"
        assert result["session_count"] == 10
        assert result["format_version"] == "v1"

    def test_parse_minimal_format(self):
        """测试解析最小格式"""
        content = """---
project: minimal
---
"""
        result = parse_context(content)

        assert result["project"] == "minimal"
        assert result["status"] == "unknown"
        assert result["category"] == "unknown"
        assert result["session_count"] == 0
        assert result["format_version"] == "mixed"

    def test_parse_with_todos(self):
        """测试解析待办事项"""
        content = """---
project: todo-test
created: 2024-01-01
---

## 待办事项

### P0 [urgent]
- [ ] 紧急任务1
- [ ] 紧急任务2

### P1 [high]
- [ ] 高优先级任务

- [x] 已完成任务
"""
        result = parse_context(content)

        # 应该包含 2 个优先级标签 + 3 个待办任务 = 5 个元素
        assert len(result["todos"]) == 5
        assert "【P0 [urgent]】" in result["todos"]
        assert "紧急任务1" in result["todos"]
        assert "紧急任务2" in result["todos"]
        assert "【P1 [high]】" in result["todos"]
        assert "高优先级任务" in result["todos"]
        # 已完成任务不应该在待办列表中
        assert not any("已完成任务" in todo for todo in result["todos"])

    def test_parse_with_stack(self):
        """测试解析技术栈"""
        content = """---
project: stack-test
stack:
  - Python/Flask
  - Vue 3
  - PostgreSQL
---
"""
        result = parse_context(content)

        assert len(result["stack"]) == 3
        assert "Python/Flask" in result["stack"]
        assert "Vue 3" in result["stack"]
        assert "PostgreSQL" in result["stack"]

    def test_parse_with_session_records(self):
        """测试检测会话记录"""
        content = """---
project: session-test
---

## 会话记录

### 2024-01-01 (会话 #1)
**主题**: 初始化项目
**完成**:
- ✅ 创建项目结构
"""
        result = parse_context(content)

        assert result["has_sessions"] is True

    def test_parse_empty_content(self):
        """测试解析空内容"""
        result = parse_context("")

        assert result["project"] == "Unknown"
        assert result["status"] == "unknown"
        assert result["session_count"] == 0


class TestPathFunctions:
    """测试路径相关函数"""

    def test_get_context_dir(self, tmp_path):
        """测试获取 .claude 目录"""
        # 在临时目录中测试
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            context_dir = get_context_dir()
            assert context_dir == tmp_path / ".claude"
        finally:
            os.chdir(original_cwd)

    def test_get_context_file_not_exists(self, tmp_path):
        """测试获取不存在的 context 文件"""
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            context_file = get_context_file()
            assert context_file is None
        finally:
            os.chdir(original_cwd)

    def test_get_context_file_exists(self, tmp_path):
        """测试获取存在的 context 文件"""
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            claude_dir = tmp_path / ".claude"
            claude_dir.mkdir()
            context_file = claude_dir / "context.md"
            context_file.write_text("---\nproject: test\n---")

            result = get_context_file()
            assert result == context_file
        finally:
            os.chdir(original_cwd)


class TestIntegration:
    """集成测试"""

    def test_full_workflow(self, tmp_path):
        """测试完整的工作流"""
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # 创建 .claude 目录和 context.md
            claude_dir = tmp_path / ".claude"
            claude_dir.mkdir()

            context_file = claude_dir / "context.md"
            content = """---
project: integration-test
created: 2024-01-01
last_session: 2024-01-05
session_count: 3
status: active
category: 测试
current_focus: "集成测试"
branch: main
---

## 待办事项
- [ ] 测试任务1
- [ ] 测试任务2
"""
            context_file.write_text(content)

            # 验证文件存在
            assert get_context_file() == context_file

            # 验证解析结果
            result = parse_context(content)
            assert result["project"] == "integration-test"
            assert result["session_count"] == 3
            assert len(result["todos"]) == 2

        finally:
            os.chdir(original_cwd)


@pytest.fixture
def temp_workspace(tmp_path):
    """创建临时 workspace 用于测试"""
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    # 创建几个测试项目
    for i in range(3):
        project_dir = workspace / f"project-{i}"
        project_dir.mkdir()
        claude_dir = project_dir / ".claude"
        claude_dir.mkdir()

        context_file = claude_dir / "context.md"
        context_file.write_text(f"""---
project: project-{i}
created: 2024-01-0{i+1}
last_session: 2024-01-0{i+1}
session_count: {i+1}
status: {"active" if i == 0 else "paused"}
category: 测试
current_focus: "项目{i}的焦点"
---
""")

    return workspace


class TestParseContextEdgeCases:
    """测试 parse_context 的边界情况"""

    def test_parse_with_quotes(self):
        """测试带引号的字段值"""
        content = """---
project: test
current_focus: "quoted value"
next_steps: "another quoted"
brief: "value with spaces"
---
"""
        result = parse_context(content)

        assert result["current_focus"] == "quoted value"
        assert result["next_steps"] == "another quoted"
        assert result["brief"] == "value with spaces"

    def test_parse_multiline_stack(self):
        """测试多行 stack"""
        content = """---
project: test
stack:
  - Python
  - JavaScript
  - SQL
  - Docker
---
"""
        result = parse_context(content)

        assert len(result["stack"]) == 4
        assert "Python" in result["stack"]
        assert "Docker" in result["stack"]

    def test_parse_empty_fields(self):
        """测试空字段"""
        content = """---
project: test
branch: ""
brief: ""
---
"""
        result = parse_context(content)

        # 空字符串带引号会被保留
        assert result["branch"] == '""'
        # brief 字段会 strip 双引号
        assert result["brief"] == ""

    def test_parse_with_special_characters(self):
        """测试特殊字符"""
        content = """---
project: test-project_v2.0
current_focus: "实现 API / 接口"
next_steps: "完成 @todo 标记"
---
"""
        result = parse_context(content)

        assert result["project"] == "test-project_v2.0"
        assert "/" in result["current_focus"]
        assert "@" in result["next_steps"]


class TestCommands:
    """测试命令函数"""

    def test_cmd_init(self, tmp_path):
        """测试初始化命令"""
        import argparse

        from scripts.context_manager import cmd_init

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # 创建 namespace 对象模拟 args
            args = argparse.Namespace()

            # 执行初始化
            cmd_init(args)

            # 验证文件创建
            context_file = tmp_path / ".claude" / "context.md"
            assert context_file.exists()

            # 验证内容
            content = context_file.read_text()
            assert "project:" in content
            assert tmp_path.name in content
            assert "status: active" in content

        finally:
            os.chdir(original_cwd)

    def test_cmd_update(self, tmp_path):
        """测试更新命令"""
        import argparse

        from scripts.context_manager import cmd_update

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # 创建初始 context.md
            claude_dir = tmp_path / ".claude"
            claude_dir.mkdir()
            context_file = claude_dir / "context.md"
            context_file.write_text("""---
project: test
created: 2024-01-01
last_session: 2024-01-01
session_count: 1
status: active
category: 探索性
current_focus: "旧焦点"
branch: main
---
""")

            # 更新字段
            args = argparse.Namespace(field="current_focus", value="新焦点")
            cmd_update(args)

            # 验证更新
            content = context_file.read_text()
            assert "新焦点" in content
            assert "session_count: 2" in content  # 应该自动增加

        finally:
            os.chdir(original_cwd)

    def test_cmd_update_status(self, tmp_path):
        """测试更新状态"""
        import argparse

        from scripts.context_manager import cmd_update

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            claude_dir = tmp_path / ".claude"
            claude_dir.mkdir()
            context_file = claude_dir / "context.md"
            context_file.write_text("""---
project: test
status: active
---
""")

            args = argparse.Namespace(field="status", value="paused")
            cmd_update(args)

            content = context_file.read_text()
            assert "status: paused" in content

        finally:
            os.chdir(original_cwd)

    def test_cmd_update_branch(self, tmp_path):
        """测试更新分支"""
        import argparse

        from scripts.context_manager import cmd_update

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            claude_dir = tmp_path / ".claude"
            claude_dir.mkdir()
            context_file = claude_dir / "context.md"
            context_file.write_text("""---
project: test
branch: main
---
""")

            args = argparse.Namespace(field="branch", value="feature/new")
            cmd_update(args)

            content = context_file.read_text()
            assert "branch: feature/new" in content

        finally:
            os.chdir(original_cwd)

    def test_cmd_migrate_v1_to_v2(self, tmp_path):
        """测试从 v1 迁移到 v2"""
        import argparse

        from scripts.context_manager import cmd_migrate

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # 创建 v1 格式的 context.md
            claude_dir = tmp_path / ".claude"
            claude_dir.mkdir()
            context_file = claude_dir / "context.md"
            context_file.write_text("""---
project: old-project
project_type: flask-api
last_session: "2024-01-05"
current_focus: "旧项目"
branch: develop
session_count: 5
---

## 会话记录
### 2024-01-05
完成了一些工作
""")

            args = argparse.Namespace()
            cmd_migrate(args)

            # 验证迁移后的内容
            content = context_file.read_text()
            assert "# ============ 基本信息 ============" in content
            assert "status: active" in content
            assert "category: flask-api" in content
            assert "branch: develop" in content
            assert "session_count: 5" in content
            # 验证保留了原有内容
            assert "会话记录" in content
            assert "完成了一些工作" in content

        finally:
            os.chdir(original_cwd)

    def test_cmd_migrate_already_v2(self, tmp_path, capsys):
        """测试已经是 v2 格式时的迁移"""
        import argparse

        from scripts.context_manager import cmd_migrate

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            claude_dir = tmp_path / ".claude"
            claude_dir.mkdir()
            context_file = claude_dir / "context.md"
            context_file.write_text("""---
# ============ 基本信息 ============
project: test
created: 2024-01-01
status: active
category: 测试
---
""")

            args = argparse.Namespace()
            cmd_migrate(args)

            captured = capsys.readouterr()
            assert "已经是融合版" in captured.out

        finally:
            os.chdir(original_cwd)


class TestDisplayFunctions:
    """测试显示函数"""

    def test_show_status(self, tmp_path, capsys):
        """测试显示状态"""
        import argparse

        from scripts.context_manager import cmd_status

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            claude_dir = tmp_path / ".claude"
            claude_dir.mkdir()
            context_file = claude_dir / "context.md"
            context_file.write_text("""---
project: test-project
created: 2024-01-01
last_session: 2024-01-05
session_count: 3
status: active
category: 测试
current_focus: "当前焦点"
branch: main
---
""")

            args = argparse.Namespace()
            cmd_status(args)

            captured = capsys.readouterr()
            output = captured.out

            assert "test-project" in output
            assert "active" in output
            assert "当前焦点" in output
            assert "会话#3" in output

        finally:
            os.chdir(original_cwd)

    def test_display_context(self, capsys):
        """测试显示完整上下文"""
        from scripts.context_manager import display_context

        context = {
            "project": "test",
            "last_session": "2024-01-01",
            "session_count": 5,
            "branch": "main",
            "current_focus": "焦点",
            "todos": ["任务1", "任务2"],
        }

        display_context(context)

        captured = capsys.readouterr()
        output = captured.out

        assert "test" in output
        assert "2024-01-01" in output
        assert "#5" in output
        assert "main" in output
        assert "焦点" in output
        assert "任务1" in output


class TestCmdSwitch:
    """测试 switch 命令"""

    def test_cmd_switch_nonexistent_project(self, tmp_path, capsys):
        """测试切换到不存在的项目"""
        import argparse

        import scripts.context_manager
        from scripts.context_manager import cmd_switch

        original_root = scripts.context_manager.WORKSPACE_ROOT
        scripts.context_manager.WORKSPACE_ROOT = tmp_path

        try:
            args = argparse.Namespace(project="nonexistent")
            cmd_switch(args)

            captured = capsys.readouterr()
            output = captured.out

            assert "不存在" in output or "not exist" in output.lower()

        finally:
            scripts.context_manager.WORKSPACE_ROOT = original_root


class TestCmdShow:
    """测试 show 命令"""

    def test_cmd_show_without_context(self, tmp_path, capsys):
        """测试没有 context.md 时显示提示"""
        import argparse

        from scripts.context_manager import cmd_show

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args = argparse.Namespace()
            cmd_show(args)

            captured = capsys.readouterr()
            output = captured.out

            assert "未检测到工作区记忆" in output or "context.md" in output

        finally:
            os.chdir(original_cwd)

    def test_cmd_show_with_context(self, tmp_path, capsys):
        """测试有 context.md 时显示内容"""
        import argparse

        from scripts.context_manager import cmd_show

        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            claude_dir = tmp_path / ".claude"
            claude_dir.mkdir()
            (claude_dir / "context.md").write_text("""---
project: show-test
last_session: 2024-01-01
session_count: 1
current_focus: "测试显示"
branch: main
---

## 待办事项
- [ ] 任务1
""")

            args = argparse.Namespace()
            cmd_show(args)

            captured = capsys.readouterr()
            output = captured.out

            assert "show-test" in output
            assert "工作区记忆已恢复" in output or "项目" in output

        finally:
            os.chdir(original_cwd)
