#!/bin/bash

# Pre-commit setup script for strands-deep-agents

set -e

echo "🔧 Setting up pre-commit hooks..."

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv .venv
    source .venv/bin/activate
fi

# Install/update dev dependencies with uv
echo "📦 Installing dev dependencies..."
uv sync --group dev

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
pre-commit install

# Optional: Run pre-commit on all files to verify setup
echo "✅ Running pre-commit on all files (initial check)..."
pre-commit run --all-files || echo "⚠️  Some checks failed. This is normal on first run. Auto-fixes have been applied."

echo ""
echo "✨ Pre-commit hooks installed successfully!"
echo ""
echo "📝 Usage:"
echo "  - Hooks will run automatically on 'git commit'"
echo "  - To manually run on all files: pre-commit run --all-files"
echo "  - To manually run on changed files: pre-commit run"
echo "  - To skip hooks (not recommended): git commit --no-verify"
