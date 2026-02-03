#!/usr/bin/env python3
"""
Context Manager Enhanced v2.0 - 工作区上下文管理（融合版）
支持双格式解析，自动迁移，会话追踪
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# ============ 配置 ============
WORKSPACE_ROOT = Path.home() / "workspace"


# ============ 工具函数 ============


def get_workspace_root() -> Path:
    """获取 workspace 根目录"""
    root = Path.cwd()
    # 向上查找直到找到 workspace 目录
    while root != Path("/"):
        if root.name == "workspace" or (root / "workspace").exists():
            if root.name == "workspace":
                return root
            return root / "workspace"
        root = root.parent
    # 默认返回 ~/workspace
    return WORKSPACE_ROOT


def get_context_dir() -> Path:
    """获取当前项目的 .claude 目录"""
    cwd = Path.cwd()
    return cwd / ".claude"


def get_context_file() -> Path | None:
    """获取当前项目的 context.md 路径"""
    context_file = get_context_dir() / "context.md"
    return context_file if context_file.exists() else None


def list_projects() -> list[dict]:
    """列出 workspace 下所有有 context.md 的项目"""
    workspace = get_workspace_root()
    projects = []

    for item in workspace.iterdir():
        if not item.is_dir() or item.name.startswith("."):
            continue

        context_file = item / ".claude" / "context.md"
        if context_file.exists():
            try:
                content = context_file.read_text(encoding="utf-8")
                info = parse_context(content)
                info["path"] = item.name
                projects.append(info)
            except Exception as e:
                print(f"⚠️  警告: 无法读取 {item.name}/.claude/context.md: {e}", file=sys.stderr)

    return projects


def parse_context(content: str) -> dict:
    """解析 context.md 内容（双格式兼容）"""
    result = {
        "project": "Unknown",
        "created": "Unknown",
        "last_session": "Unknown",
        "session_count": 0,
        "status": "unknown",
        "category": "unknown",
        "project_type": "",
        "current_focus": "Unknown",
        "next_steps": "",
        "brief": "",
        "branch": "",
        "stack": [],
        "todos": [],
        "has_sessions": False,
        "format_version": "unknown",
    }

    lines = content.split("\n")
    in_frontmatter = False
    in_todos = False
    in_stack = False
    in_sessions = False

    for line in lines:
        # 解析 YAML frontmatter
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
            continue

        if in_frontmatter:
            # 新版字段
            if line.startswith("project:"):
                result["project"] = line.split(":", 1)[1].strip()
            elif line.startswith("created:"):
                result["created"] = line.split(":", 1)[1].strip()
            elif line.startswith("last_session:"):
                result["last_session"] = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("status:"):
                result["status"] = line.split(":", 1)[1].strip()
            elif line.startswith("category:"):
                result["category"] = line.split(":", 1)[1].strip()
            elif line.startswith("current_focus:"):
                result["current_focus"] = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("next_steps:"):
                result["next_steps"] = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("brief:"):
                result["brief"] = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("branch:"):
                result["branch"] = line.split(":", 1)[1].strip()
            elif line.startswith("session_count:"):
                result["session_count"] = int(line.split(":", 1)[1].strip())
            # 旧版字段兼容
            elif line.startswith("project_type:"):
                result["project_type"] = line.split(":", 1)[1].strip()
                if result["category"] == "unknown":
                    result["category"] = result["project_type"]
            elif line.startswith("stack:"):
                in_stack = True
            elif in_stack and line.startswith("  - "):
                result["stack"].append(line.replace("  - ", "").strip())
            elif in_stack and not line.startswith(" "):
                in_stack = False

        # 解析 TODO 列表
        if "## 待办事项" in line or "## 待办" in line:
            in_todos = True
            in_sessions = False
            continue

        # 检测会话记录
        if "## 会话记录" in line or "## 本次会话概览" in line or "## 已完成工作" in line:
            in_sessions = True
            result["has_sessions"] = True
            in_todos = False
            continue

        if in_todos and line.startswith("## ") and "待办" not in line:
            in_todos = False
            continue

        if in_sessions and line.startswith("## ") and "会话" not in line and "完成" not in line:
            in_sessions = False
            continue

        if not in_todos:
            continue

        if "- [ ]" in line:
            todo_text = line.split("- [ ]")[1].strip()[:60]
            result["todos"].append(todo_text)
        elif "- [x]" in line:
            # 已完成的待办，不加入待办列表
            pass
        elif line.strip().startswith("### P"):
            prio = line.strip().replace("### ", "")
            result["todos"].append(f"【{prio}】")

    # 检测格式版本
    if result["created"] != "Unknown" and result["status"] in ["active", "paused", "completed"]:
        result["format_version"] = "v2"
    elif result["project_type"] or result["session_count"] > 0 or result["branch"]:
        result["format_version"] = "v1"
    else:
        result["format_version"] = "mixed"

    return result


# ============ 显示函数 ============


def display_context(context: dict):
    """显示工作区上下文摘要"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    🧠 工作区记忆已恢复                            ║
╠══════════════════════════════════════════════════════════════════╣""")
    print(f"║  项目: {context['project']:<52} ║")
    print(f"║  上次: {context['last_session']:<52} ║")
    if context["session_count"] > 0:
        print(f"║  会话: #{context['session_count']:<51} ║")
    if context["branch"]:
        print(f"║  分支: {context['branch']:<52} ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    print(f"║  当前焦点: {context['current_focus'][:40]:<46} ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    print("║  📋 待办列表:                                                    ║")

    for todo in context["todos"][:10]:
        todo_clean = todo.replace("• •", "  ").replace("  [", "[").replace("• [", "[")
        todo_text = todo_clean[:46]
        print(f"║  {todo_text:<50} ║")

    if len(context["todos"]) > 10:
        remaining = len(context["todos"]) - 10
        print(f"║  ... 还有 {remaining} 项{'':<37} ║")

    print("╚══════════════════════════════════════════════════════════════════╝")


def show_status():
    """显示当前项目简要状态（紧凑版）"""
    context_file = get_context_file()
    if not context_file:
        print("⚠️  当前项目没有 context.md")
        return

    content = context_file.read_text(encoding="utf-8")
    info = parse_context(content)

    status_icon = {"active": "🟢", "paused": "🟡", "completed": "✅", "unknown": "⚪"}.get(
        info["status"], "⚪"
    )

    branch_info = f" | {info['branch']}" if info["branch"] else ""
    session_info = f" | 会话#{info['session_count']}" if info["session_count"] > 0 else ""

    print(f"""
📊 {status_icon} {info['project']}
   ├─ 状态: {info['status']} | 分类: {info['category']}{branch_info}
   ├─ 焦点: {info['current_focus'][:50]}
   └─ 待办: {len(info['todos'])} 项{session_info} | 上次: {info['last_session']}
""")


# ============ 命令函数 ============


def cmd_ls(_args):
    """列出所有项目"""
    projects = list_projects()

    if not projects:
        print("📭 workspace 下还没有任何项目记录")
        return

    # 按状态分组
    active = [p for p in projects if p["status"] == "active"]
    paused = [p for p in projects if p["status"] == "paused"]
    completed = [p for p in projects if p["status"] == "completed"]
    others = [p for p in projects if p["status"] not in ["active", "paused", "completed"]]

    print(f"\n📁 Workspace 项目概览 ({len(projects)} 个项目)\n")

    if active:
        print("🟢 进行中")
        for p in sorted(active, key=lambda x: x["last_session"], reverse=True):
            focus = (
                p["current_focus"][:35] + "..."
                if len(p["current_focus"]) > 35
                else p["current_focus"]
            )
            session_tag = f" #{p['session_count']}" if p["session_count"] > 0 else ""
            print(f"   {p['path']:<25} | {focus}{session_tag}")
        print()

    if paused:
        print("🟡 已暂停")
        for p in sorted(paused, key=lambda x: x["last_session"], reverse=True):
            print(f"   {p['path']:<25} | {p['last_session']}")
        print()

    if completed:
        print("✅ 已完成")
        for p in sorted(completed, key=lambda x: x["last_session"], reverse=True):
            print(f"   {p['path']:<25} | {p['last_session']}")
        print()

    if others:
        print("⚪ 其他")
        for p in sorted(others, key=lambda x: x["last_session"], reverse=True):
            print(f"   {p['path']:<25} | {p['status']}")
        print()


def cmd_status(_args):
    """显示当前项目状态"""
    show_status()


def cmd_init(_args):
    """初始化新项目（融合版模板）"""
    context_dir = get_context_dir()
    context_file = context_dir / "context.md"

    if context_file.exists():
        print(f"⚠️  {context_file} 已存在")
        return

    # 创建 .claude 目录
    context_dir.mkdir(exist_ok=True)

    # 生成融合版模板
    project_name = Path.cwd().name
    today = datetime.now().strftime("%Y-%m-%d")

    template = f"""---
# ============ 基本信息 ============
project: {project_name}
created: {today}
last_session: {today}
session_count: 1

# ============ 状态分类 ============
status: active                 # active | paused | completed
category: 探索性               # 探索性 | 产品 | 临时 | 学习
project_type:                  # 技术类型（可选）

# ============ 工作追踪 ============
current_focus: "初始化项目"
next_steps: "完成项目设置"
branch: main                   # 当前 Git 分支

# ============ 项目描述 ============
brief: "请用一句话描述这个项目的目标"

# ============ 技术栈 ============
stack:
  - 语言/框架
  - 主要工具

---

## 📋 待办事项

### P0 [本周]
- [ ] 完成项目初始化
- [ ] 编写 README

### P1 [本月]
- [ ] 实现核心功能
- [ ] 编写测试

## 📝 会话记录

### {today} (会话 #1)
**主题**: 初始化项目
**开始**: {datetime.now().strftime("%H:%M")}
**完成**:
- ✅ 创建 context.md
- ✅ 配置开发环境

## 📝 笔记/决策
<!-- 重要决策、问题记录 -->

## 🔗 相关资源
<!-- 链接、文档等 -->
"""

    context_file.write_text(template, encoding="utf-8")
    print(f"✅ 已创建 {context_file}")
    print(f"\n📝 项目: {project_name}")
    print("   请编辑 context.md 填写项目信息\n")


def cmd_switch(args):
    """切换到指定项目"""
    project_name = args.project
    workspace = get_workspace_root()
    target_path = workspace / project_name

    if not target_path.exists():
        print(f"❌ 项目不存在: {project_name}")
        print(f"   路径: {target_path}")
        return

    if not target_path.is_dir():
        print(f"❌ 不是目录: {project_name}")
        return

    # 打印切换命令供用户复制
    print(f"\n🔄 切换到项目: {project_name}")
    print(f"\n   请执行: cd {target_path}\n")

    # 显示项目状态
    context_file = target_path / ".claude" / "context.md"
    if context_file.exists():
        os.chdir(target_path)
        content = context_file.read_text(encoding="utf-8")
        info = parse_context(content)
        display_context(info)
    else:
        print("⚠️  该项目还没有 context.md")


def cmd_update(args):
    """更新字段"""
    context_file = get_context_file()
    if not context_file:
        print("❌ 当前项目没有 context.md")
        return

    content = context_file.read_text(encoding="utf-8")

    # 简单的字段更新
    field = args.field
    value = args.value

    # 支持的字段
    valid_fields = [
        "project",
        "status",
        "category",
        "project_type",
        "current_focus",
        "next_steps",
        "brief",
        "branch",
    ]

    if field in valid_fields:
        # 更新或添加字段
        if f"{field}:" in content:
            content = content.replace(f"{field}:", f"{field}: {value}", 1)
        else:
            # 在 created 后添加
            content = content.replace("created: ", f"created: \n{field}: {value}\nlast_session: ")
    else:
        print(f"❌ 不支持的字段: {field}")
        print(f"   支持的字段: {', '.join(valid_fields)}")
        return

    # 更新 last_session 和 session_count
    today = datetime.now().strftime("%Y-%m-%d")
    content = re.sub(r"last_session:.*", f"last_session: {today}", content)

    # 增加 session_count（如果存在）
    if "session_count:" in content:
        content = re.sub(
            r"session_count: (\d+)", lambda m: f"session_count: {int(m.group(1)) + 1}", content
        )

    context_file.write_text(content, encoding="utf-8")
    print(f"✅ 已更新 {field}: {value}")


def cmd_migrate(_args):
    """迁移旧版 context.md 到融合版"""
    context_file = get_context_file()
    if not context_file:
        print("❌ 当前项目没有 context.md")
        return

    content = context_file.read_text(encoding="utf-8")
    info = parse_context(content)

    # 检查是否需要迁移
    if info["format_version"] == "v2":
        print("✅ 已经是融合版格式，无需迁移")
        return

    print(f"📦 检测到格式版本: {info['format_version']}")
    print("🔄 开始迁移到融合版...\n")

    # 构建新版 frontmatter
    new_frontmatter = f"""---
# ============ 基本信息 ============
project: {info['project']}
created: {info['created'] if info['created'] != 'Unknown' else datetime.now().strftime('%Y-%m-%d')}
last_session: {datetime.now().strftime('%Y-%m-%d')}
session_count: {info['session_count'] if info['session_count'] > 0 else 1}

# ============ 状态分类 ============
status: active                 # 请根据实际情况修改: active | paused | completed
category: {info['category'] if info['category'] != 'unknown' else '探索性'}
project_type: {info['project_type'] if info['project_type'] else ''}

# ============ 工作追踪 ============
current_focus: "{info['current_focus']}"
next_steps: ""
branch: {info['branch'] if info['branch'] else 'main'}

# ============ 项目描述 ============
brief: {info['brief'] if info['brief'] else '"请用一句话描述这个项目的目标"'}

# ============ 技术栈 ============
stack:
"""

    # 添加 stack
    if info["stack"]:
        for item in info["stack"]:
            new_frontmatter += f"  - {item}\n"
    else:
        new_frontmatter += "  - 语言/框架\n"

    new_frontmatter += "---\n\n"

    # 保留原有内容（移除旧的 frontmatter）
    lines = content.split("\n")
    in_old_frontmatter = False
    content_part = []

    for line in lines:
        if line.strip() == "---":
            if not in_old_frontmatter and not content_part:
                in_old_frontmatter = True
                continue
            elif in_old_frontmatter:
                in_old_frontmatter = False
                continue
        if not in_old_frontmatter:
            content_part.append(line)

    # 合并
    new_content = new_frontmatter + "\n".join(content_part)

    # 写入
    context_file.write_text(new_content, encoding="utf-8")

    print("✅ 迁移完成！")
    print(f"\n📝 请检查并编辑: {context_file}")
    print("   特别注意确认:")
    print("   - status (active/paused/completed)")
    print("   - category (探索性/产品/临时/学习)")
    print("   - brief (项目目标描述)\n")


def cmd_show(_args):
    """显示完整上下文（默认命令）"""
    context_file = get_context_file()

    if context_file:
        content = context_file.read_text(encoding="utf-8")
        context = parse_context(content)
        display_context(context)
    else:
        cwd = Path.cwd()
        print(f"""
📂 当前目录: {cwd}

⚠️  未检测到工作区记忆 (.claude/context.md)

使用命令:
  ctx init    - 创建 context.md 并开始跟踪
  ctx ls      - 查看所有项目
  ctx switch  - 切换到其他项目
  ctx migrate - 迁移旧格式到融合版
""")


# ============ 主函数 ============


def main():
    parser = argparse.ArgumentParser(
        description="Context Manager Enhanced v2.0 - 工作区上下文管理",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  ctx              显示当前项目上下文
  ctx status       显示简要状态
  ctx ls           列出所有项目
  ctx switch <名>  切换到指定项目
  ctx init         初始化新项目（融合版）
  ctx migrate      迁移旧格式到融合版
  ctx update status paused  更新状态
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # ls 命令
    subparsers.add_parser("ls", help="列出所有项目")

    # status 命令
    subparsers.add_parser("status", help="显示简要状态")

    # init 命令
    subparsers.add_parser("init", help="初始化新项目")

    # switch 命令
    switch_parser = subparsers.add_parser("switch", help="切换到指定项目")
    switch_parser.add_argument("project", help="项目名称")

    # update 命令
    update_parser = subparsers.add_parser("update", help="更新字段")
    update_parser.add_argument("field", help="字段名")
    update_parser.add_argument("value", help="新值")

    # migrate 命令
    subparsers.add_parser("migrate", help="迁移旧格式到融合版")

    # 解析参数
    args = parser.parse_args()

    # 执行命令
    if args.command == "ls":
        cmd_ls(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "init":
        cmd_init(args)
    elif args.command == "switch":
        cmd_switch(args)
    elif args.command == "update":
        cmd_update(args)
    elif args.command == "migrate":
        cmd_migrate(args)
    else:
        # 默认命令：显示上下文
        cmd_show(args)


if __name__ == "__main__":
    main()
