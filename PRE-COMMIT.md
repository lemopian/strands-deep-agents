# Pre-commit Hooks Guide

This project uses [pre-commit](https://pre-commit.com/) to automatically check and fix code before commits.

## Quick Setup

```bash
# Activate environment and install dependencies
source .venv/bin/activate
uv sync --group dev

# Install pre-commit and pre-push hooks
pre-commit install
pre-commit install --hook-type pre-push
```

## What Gets Checked

The pre-commit hooks automatically run on **changed files only** when you commit:

### Auto-Fixes (Applied Automatically)
- ✅ **Trailing whitespace** - Removes trailing spaces
- ✅ **End of file** - Ensures files end with a newline
- ✅ **Mixed line endings** - Standardizes to LF
- ✅ **Import sorting** - Orders imports with isort (black-compatible)
- ✅ **Code formatting** - Formats Python code with black (100 char line length)
- ✅ **Linting fixes** - Auto-fixes common issues with ruff

### Checks (Will Block Commit if Failed)
- 🔍 **YAML syntax** - Validates YAML files
- 🔍 **TOML syntax** - Validates TOML files
- 🔍 **Large files** - Blocks files > 500KB
- 🔍 **Merge conflicts** - Detects merge conflict markers
- 🔍 **Debug statements** - Finds leftover debug code
- 🔍 **Ruff linting** - Checks for code quality issues

### Pre-Push Checks (Will Block Push if Failed)
- 🧪 **All tests** - Runs complete pytest suite before push

## Usage

### Automatic (Default)

**On Commit** - Auto-fixes and checks run on staged files:
```bash
git add .
git commit -m "Your message"
# Auto-formatting and linting run automatically
```

**On Push** - All tests run before push:
```bash
git push
# All pytest tests run automatically before push
```

### Manual Runs

```bash
# Run commit hooks on all files
pre-commit run --all-files

# Run commit hooks on currently changed files
pre-commit run

# Run pre-push hooks manually
pre-commit run --hook-stage push

# Run all tests manually
pytest -v

# Run a specific hook
pre-commit run black --all-files

# Skip hooks (not recommended)
git commit --no-verify -m "Emergency fix"
git push --no-verify  # Skip tests (really not recommended)
```

## Configuration

- **Config file**: `.pre-commit-config.yaml`
- **Line length**: 100 characters (black, ruff, isort)
- **Python version**: 3.9+ compatibility
- **Import style**: black-compatible with isort

## Customization

### Enable Type Checking

To enable mypy type checking (currently disabled due to pre-existing issues):

1. Edit `.pre-commit-config.yaml`
2. Uncomment the mypy section
3. Run `pre-commit run --all-files` to see current issues

### Adjust Ruff Rules

Edit `.pre-commit-config.yaml` and modify the ruff args:

```yaml
args: ['--fix', '--line-length=100', '--ignore=F841,E501']
```

### Update Hooks

```bash
pre-commit autoupdate
```

## Troubleshooting

### Hooks fail on commit

1. Review the error messages
2. Auto-fixes are applied automatically - just commit again
3. For other issues, fix the code and commit again

### Install failed

```bash
# Clean and reinstall
rm -rf ~/.cache/pre-commit
pre-commit clean
pre-commit install
```

### Virtual environment issues

Ensure you're using the correct venv:

```bash
source .venv/bin/activate
which python  # Should point to .venv/bin/python
```

## Best Practices

1. **Let auto-fixes work**: If a commit fails, hooks may have fixed issues - just commit again
2. **Tests run on push**: All tests automatically run before push to ensure code quality
3. **Commit often**: Auto-formatting happens on commit, so commit frequently
4. **Keep hooks updated**: Run `pre-commit autoupdate` monthly
5. **Don't skip hooks**: Only use `--no-verify` in emergencies
6. **Local testing**: Run `pytest -v` locally before pushing to catch issues early
