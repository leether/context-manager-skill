#!/bin/bash
# 自动显示项目上下文 - 示例配置文件
#
# 将此文件复制到 ~/.claude/context-manager-skill/auto-display.sh
# 然后在 ~/.zshrc 中添加: source ~/.claude/context-manager-skill/auto-display.sh

show_context() {
    local CONTEXT_FILE="$PWD/.claude/context.md"

    if [ ! -f "$CONTEXT_FILE" ]; then
        return
    fi

    # 提取关键信息
    local project=$(grep "^project:" "$CONTEXT_FILE" | cut -d: -f2 | xargs 2>/dev/null || echo "Unknown")
    local status=$(grep "^status:" "$CONTEXT_FILE" | cut -d: -f2 | xargs 2>/dev/null || echo "Unknown")
    local category=$(grep "^category:" "$CONTEXT_FILE" | cut -d: -f2 | xargs 2>/dev/null || echo "Unknown")
    local focus=$(grep "^current_focus:" "$CONTEXT_FILE" | sed 's/^current_focus: *//' | sed 's/["'"'"'"]//g' | head -1)
    local session_count=$(grep "^session_count:" "$CONTEXT_FILE" | cut -d: -f2 | xargs 2>/dev/null || echo "0")
    local last_session=$(grep "^last_session:" "$CONTEXT_FILE" | cut -d: -f2 | xargs 2>/dev/null || echo "Unknown")

    # 只有在项目目录（非工作区根）时才显示
    # 可以根据需要调整此逻辑
    if [ "$project" != "workspace" ]; then
        echo "══════════════════════════════════════════════════════════════"
        echo "📂 项目: $project"
        echo "══════════════════════════════════════════════════════════════"
        echo "📊 状态: $status | 分类: $category"
        echo "🎯 焦点: $focus"
        echo "📅 会话 #$session_count | 最后: $last_session"
        echo "══════════════════════════════════════════════════════════════"
        echo ""
    fi
}

# 在每次显示提示符前调用
if [ "$BASH_VERSION" ]; then
    PROMPT_COMMAND="show_context; $PROMPT_COMMAND"
elif [ "$ZSH_VERSION" ]; then
    precmd() { show_context }
fi
