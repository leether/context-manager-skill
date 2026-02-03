#!/bin/bash
# Context Manager Setup

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SKILL_DIR/.venv"

echo "🧠 Context Manager Setup"
echo "========================"

# 创建虚拟环境
if [ ! -d "$VENV_DIR" ]; then
    uv venv "$VENV_DIR" --python 3.12
fi

# 创建 wrapper
cat > "$SKILL_DIR/ctx" << 'EOF'
#!/bin/bash
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SKILL_DIR/.venv/bin/python" "$SKILL_DIR/scripts/context_manager.py" "$@"
EOF

chmod +x "$SKILL_DIR/ctx"

echo "✅ 安装完成"
echo ""
echo "使用: ./ctx"
