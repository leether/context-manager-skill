#!/bin/bash
# Context Manager Shell 集成
# 将此文件内容添加到 ~/.bashrc 或 ~/.zshrc

# 项目快速切换函数
repos() {
    echo ""
    echo "📁 Workspace 项目列表"
    echo "────────────────────────────────────"
    ls -1 ~/workspace 2>/dev/null | grep -v "^\." | nl
    echo ""
}

go() {
    local project=$1
    local workspace=~/workspace

    if [ -z "$project" ]; then
        echo "用法: go <项目名>"
        echo "示例: go podcast-app"
        repos
        return 1
    fi

    if [ ! -d "$workspace/$project" ]; then
        echo "❌ 项目不存在: $project"
        repos
        return 1
    fi

    cd "$workspace/$project" || return 1

    # 自动显示项目状态
    if [ -f ".claude/context.md" ]; then
        ~/.claude/skills/context-manager/ctx status
    else
        echo "✅ 已切换到: $project"
        echo "   (该项目还没有 context.md，使用 'ctx init' 创建)"
    fi
}

# ctx 命令快捷方式
alias ctx='~/.claude/skills/context-manager/ctx'

# Tab 补全支持 (bash)
if [ -n "$BASH_VERSION" ]; then
    _go_complete() {
        local cur=${COMP_WORDS[COMP_CWORD]}
        local projects=$(ls ~/workspace 2>/dev/null | grep -v "^\.")
        COMPREPLY=($(compgen -W "$projects" -- "$cur"))
    }
    complete -F _go_complete go

    _ctx_complete() {
        local cur=${COMP_WORDS[COMP_CWORD]}
        local cmds="ls status init switch update"
        COMPREPLY=($(compgen -W "$cmds" -- "$cur"))
    }
    complete -F _ctx_complete ctx
fi

# Tab 补全支持 (zsh)
if [ -n "$ZSH_VERSION" ]; then
    _go() {
        local -a projects
        projects=(~/workspace/*(N:t))
        _describe 'projects' projects
    }
    compdef _go go

    _ctx() {
        local -a cmds
        cmds=(ls status init switch update)
        _describe 'commands' cmds
    }
    compdef _ctx ctx
fi
