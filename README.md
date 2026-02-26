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

```bash
git clone https://github.com/steliosot/patch-cli.git && cd patch-cli && bash install.sh
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

### Basic Usage

```bash
# Fix a command
./patch.py "sudo systemctl start docker"

# Ask for help
./patch.py --help

# Run with verbose output
./patch.py --verbose "docker ps"
```

### Docker Build Testing

```bash
# Run Docker build tests (20 Dockerfiles)
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