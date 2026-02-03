#!/bin/bash
# 显示当前项目的 context.md 内容

CONTEXT_FILE="$PWD/.claude/context.md"

if [ -f "$CONTEXT_FILE" ]; then
    echo "════════════════════════════════════════════════════════════════"
    echo "📂 项目上下文 - $(basename "$PWD")"
    echo "════════════════════════════════════════════════════════════════"
    
    # 提取项目名
    project=$(grep "^project:" "$CONTEXT_FILE" | cut -d: -f2 | xargs)
    
    # 提取状态和分类
    status=$(grep "^status:" "$CONTEXT_FILE" | cut -d: -f2 | xargs)
    category=$(grep "^category:" "$CONTEXT_FILE" | cut -d: -f2 | xargs)
    
    # 提取当前焦点
    focus=$(grep "^current_focus:" "$CONTEXT_FILE" | cut -d"'" -f2 | xargs)
    
    echo "📊 状态: $status | 分类: $category"
    echo "🎯 当前焦点: $focus"
    
    # 提取会话数
    session_count=$(grep "^session_count:" "$CONTEXT_FILE" | cut -d: -f2 | xargs)
    last_session=$(grep "^last_session:" "$CONTEXT_FILE" | cut -d: -f2 | xargs)
    echo "📅 会话 #$session_count | 最后工作: $last_session"
    
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    echo "💡 提示: 使用 'ctx' 查看完整上下文"
    echo ""
fi
SCRIPT

chmod +x /Users/lize/.claude/context-manager-skill/show-context.sh
echo "✅ 创建了显示脚本"
