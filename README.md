# Patch CLI Tool - Fix Broken Shell Commands using AI

A command-line tool that automatically fixes broken shell commands using OpenAI GPT-4o-mini.

**Features:**
- Automatic error analysis and command suggestions
- Confidence scoring (High/Medium/Low)
- Platform-aware fixes (macOS/Linux)
- Piped command support with security detection
- Docker build testing suite
- Comprehensive test coverage (71 tests)

---

## Quick Install

### Option 1: Install via pip (Recommended - Run from anywhere)

Install from GitHub:
```bash
pip install --break-system-packages git+https://github.com/steliosot/patch-cli.git
```

Note: On Debian/Ubuntu/Mint with externally-managed Python environments, use `--break-system-packages` flag.

Or install in editable mode (for development):
```bash
git clone https://github.com/steliosot/patch-cli.git
cd patch-cli
pip install -e . --break-system-packages
```

Then run it from any directory:
```bash
patch "sudo adduser yoda"
patch "docker ps"
patch --help
```

### Option 2: Git clone and local install

```bash
git clone https://github.com/steliosot/patch-cli.git && cd patch-cli && bash install.sh
```

### Option 3: Development install (for contributors)

```bash
git clone https://github.com/steliosot/patch-cli.git
cd patch-cli
pip install -e .
```

---

## Update patch-cli

When new features are added, update easily:

```bash
pip install --upgrade --break-system-packages git+https://github.com/steliosot/patch-cli.git
```

---

## What You Need to Install

### Required

1. **Python 3.8+**
   - Install: `brew install python3` (macOS) or `apt install python3` (Linux)
   - Check: `python3 --version`

2. **OpenAI API Key**
   - Get from: https://platform.openai.com/api-keys
   - Set as env var: `export OPENAI_API_KEY='sk-...'`

3. **Pip (Python package manager)**
   - Included with Python
   - Update: `python3 -m pip install --upgrade pip`

### Optional (for Docker testing)

4. **Docker Desktop**
   - Install: `brew install docker-desktop --cask` (macOS)
   - Start: `open /Applications/Docker.app`
   - Download: https://www.docker.com/products/docker-desktop

---

---

## Installation Methods Explained

### pip install (Recommended)
- **Pros**: Run `patch` command from any directory, easy updates with `pip --upgrade`, cleaner installation
- **Cons**: Requires internet for installation, requires pip setup

```bash
pip install patch-cli
```

### Git clone
- **Pros**: Full source code, can modify locally, works offline after clone
- **Cons**: Can only run from the cloned directory, manual updates required

```bash
git clone https://github.com/steliosot/patch-cli.git && cd patch-cli && bash install.sh
```

---

## Prerequisites Check

```bash
# Check Python version
python3 --version

# Check pip
python3 -m pip --version

# Check Docker (optional)
docker --version

# Install dependencies
python3 -m pip install openai tqdm
```

---

## Usage

If you installed via pip, use the `patch` command. If you cloned via git, use `./patch.py`.

### Basic Usage

```bash
# Fix a command
patch "sudo systemctl start docker"

# Ask for help
patch --help

# Run with a command
patch "docker ps"
```

### Docker Build Testing

```bash
# Run Docker build tests (20 Dockerfiles) - from cloned repo only
python3 docker_test_suite.py

# Run all test suites
python3 run_all_tests.py
```

### Test Suites

```bash
# Unit tests (31 tests)
python3 test_unit.py

# Integration tests (16 tests)
python3 test_integration.py

# Scenario tests (24 tests)
python3 test_scenarios.py

# Piped command tests (24 tests)
python3 test_piped_comprehensive.py
```

---

## Environment Variables

```bash
# Required
export OPENAI_API_KEY="sk-..."

# Optional
export PATCH_VERBOSE=0
export Patch_MAX_RETRIES=3
export Patch_TIMEOUT=30
```

---

## Documentation

- **README.md** - This file
- **FEATURES.md** - Feature documentation
- **CHANGELOG.md** - Version history
- **ERROR_HANDLING.md** - Error handling guide
- **FILES.md** - File overview

---

## Testing

```bash
# Quick test
python3 run_all_tests.py

# Comprehensive test
python3 -m pytest test_*.py -v

# LSP/syntax check
python3 lsp_checker.py
```

---

## Troubleshooting

### "externally-managed-environment" Error (Debian/Ubuntu/Mint)

Debian-based systems protect Python environments. To install:

```bash
pip install --break-system-packages git+https://github.com/steliosot/patch-cli.git
```

Alternative: Use a virtual environment:
```bash
python3 -m venv ~/.patch-venv
source ~/.patch-venv/bin/activate
pip install git+https://github.com/steliosot/patch-cli.git
```

### "permission denied" Error

Add `--break-system-packages` flag to pip install commands (Debian/Ubuntu/Mint).

### "patch: command not found"

Use `patch` (not `patch.py`) if installed via pip. Or reinstall:
```bash
pip install -e . --break-system-packages
```

### OpenAI API Key Not Found

Set your OpenAI API key:
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

Get your key at: https://platform.openai.com/api-keys

---

## Support

- **Issues:** https://github.com/[username]/patch/issues
- **Discussions:** https://github.com/[username]/patch/discussions

---

## License

MIT License - See LICENSE file for details

---

**Installation Summary:**
1. Python 3.8+ Required
2. OpenAI API Key Required
3. Dependencies: `openai`, `tqdm`
4. Docker (optional, for real builds)