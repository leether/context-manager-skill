# 自动显示项目上下文

## 🎯 功能说明

这个脚本会在每次新开终端时自动显示项目的关键信息，让你快速了解当前项目的状态。

## 📦 文件位置

- **脚本**: `show-context.sh`
- **配置示例**: `auto-display-example.sh`

## 🚀 快速配置

### 方法 1: 自动配置（推荐）

在 `~/.zshrc` 或 `~/.bashrc` 中添加：

```bash
# Context Manager - 自动显示项目上下文
if [ -f ~/.claude/context-manager-skill/show-context.sh ]; then
    ~/.claude/skills/context-manager-skill/show-context.sh
fi
```

### 方法 2: 从项目安装

```bash
# 复制脚本到技能目录
cp /path/to/context-manager-skill/show-context.sh ~/.claude/context-manager-skill/

# 然后按方法1配置
```

### 方法 3: 从项目配置文件

```bash
# 复制配置文件
cp /path/to/context-manager-skill/auto-display-example.sh ~/.claude/context-manager-skill/auto-display.sh

# 在 shell 配置中 source
echo "source ~/.claude/context-manager-skill/auto-display.sh" >> ~/.zshrc
```

## 📊 显示内容

脚本会自动从 `.claude/context.md` 提取并显示：

- 📂 项目名称
- 📊 状态（active/paused/completed）
- 🏷️ 分类
- 🎯 当前焦点
- 📅 会话数和最后工作日期

## 🔧 自定义显示

如果需要自定义显示格式，可以编辑 `show-context.sh` 中的 `echo` 语句。

## ✅ 验证安装

```bash
# 测试脚本
~/.claude/context-manager-skill/show-context.sh

# 如果看到项目上下文信息，说明配置成功
```

## 💡 提示

- 确保项目目录下有 `.claude/context.md` 文件
- 如果没有 context.md，脚本会静默退出
- 可以手动运行脚本查看上下文：`~/.claude/context-manager-skill/show-context.sh`
