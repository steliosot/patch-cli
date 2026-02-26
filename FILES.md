# Patch CLI - File Overview

## Core Files

### patch.py
Main application file that implements all features:
- AI-powered command fixing
- Error handling for OpenAI API
- Interactive menu system
- Confidence scoring
- Retry functionality
- Command preview
- Sudo warnings

**Usage:**
```bash
export OPENAI_API_KEY="your-key-here"
python3 patch.py <command>
```

---

## Demo Scripts

### demo_progress.py
Demonstrates high confidence fix scenario:
- Error: `git pus` typo
- Suggestion: `git push` with 95% confidence [High]
- Shows normal flow with apply fix option

**Run:** `python3 demo_progress.py`

### demo_medium_confidence.py
Demonstrates medium confidence with tips:
- Error: `npm install react`
- Suggestion: `npm install react --save` with 78% confidence [Medium]
- Shows helpful tip: "This fix should work but..."

**Run:** `python3 demo_medium_confidence.py`

### demo_low_confidence.py
Demonstrates low confidence with warnings:
- Error: `sudo rm -rf /`
- Suggestion: `sudo rm -rf /tmp/*` with 45% confidence [Low - Uncertain]
- Shows detailed warning explaining uncertainty

**Run:** `python3 demo_low_confidence.py`

### demo_retry.py
Demonstrates retry functionality:
- First suggestion lower confidence
- User requests alternative via retry
- Second suggestion higher confidence

**Run:** `python3 demo_retry.py`

### demo_piped.py *(New!)*
Demonstrates piped command support:
- Piped commands with pipe-to-shell warnings
- Multiple pipe support
- Pipeline preservation
- Full command execution
- Cross-platform compatibility

**Run:** `python3 demo_piped.py`

### demo_context.py *(New!)*
Demonstrates enhanced AI context awareness:
- Command, platform, application detection
- Error categorization
- Before/after comparison
- Platform-specific solutions
- Better AI suggestions with more context

**Run:** `python3 demo_context.py`

### demo_errors.py

---

## Documentation

### README.md
Getting started guide:
- Installation instructions
- Basic usage
- Menu options
- Error handling overview

### FEATURES.md
Comprehensive feature documentation:
- All core features
- Confidence scoring levels
- Retry functionality
- Error handling details
- Visual feedback system

### CHANGELOG.md
Version history:
- Initial release features
- Feature list
- Future enhancements

### ERROR_HANDLING.md
Detailed error handling guide:
- All error types explained
- Solutions for each error
- Testing procedures
- Best practices

### PIPED_COMMANDS.md *(New!)*
Comprehensive piped command guide:
- All supported pipe types
- Pipe-to-shell detection
- Technical implementation
- Safety features
- Cross-platform compatibility
- Testing procedures
- Best practices

### FILES.md
This file - file overview and structure

---

## Configuration Files

### requirements.txt
Python package dependencies:
```
openai>=1.0.0
tqdm
```

---

## Project Structure

```
test-local-1/
├── patch.py                    # Main application
├── demo_progress.py            # High confidence demo
├── demo_medium_confidence.py  # Medium confidence demo
├── demo_low_confidence.py      # Low confidence demo
├── demo_retry.py               # Retry functionality demo
├── demo_errors.py              # Error handling demo
├── demo_piped.py               # Piped commands demo *(New!)*
├── README.md                   # Getting started
├── FEATURES.md                 # Feature documentation
├── CHANGELOG.md                # Version history
├── ERROR_HANDLING.md           # Error handling guide
├── PIPED_COMMANDS.md           # Piped commands guide *(New!)*
├── FILES.md                    # file overview
└── requirements.txt            # Dependencies
```

---

## Development Notes

### Code Organization
- Imports and setup at top
- Utility functions first
- Core logic sections
- Main() function at bottom

### Key Functions
- `get_api_key()` - Retrieves/validates OpenAI API key
- `execute_command()` - Runs commands with sudo checks
- `show_blinking_cursor()` - Animation while analyzing
- `ask_openai_for_fix()` - Calls OpenAI with error handling
- `interactive_menu()` - Menu selection system
- `show_logo()` - ASCII logo display
- `main()` - Main application flow

### Error Handling Strategy
- Specific exception types for each error
- User-friendly error messages
- Clean exits (no confusing tracebacks)
- Links to relevant OpenAI pages
- Pre-flight API key validation

### Future File Additions
- `.patchrc` - Configuration file
- `patch_history.txt` - Command history log
- `setup.py` - Installation package
- `tests/` - Unit test directory

---

## Quick Reference

| File | Purpose | Run Command |
|------|---------|-------------|
| patch.py | Main app | `python3 patch.py <cmd>` |
| demo_progress.py | High conf demo | `python3 demo_progress.py` |
| demo_medium_confidence.py | Medium conf demo | `python3 demo_medium_confidence.py` |
| demo_low_confidence.py | Low conf demo | `python3 demo_low_confidence.py` |
| demo_retry.py | Retry demo | `python3 demo_retry.py` |
| demo_errors.py | Error handling demo | `python3 demo_errors.py` |
| demo_piped.py | Piped commands demo | `python3 demo_piped.py` |

---

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Set API key: `export OPENAI_API_KEY="your-key"`
3. Run: `python3 patch.py <command>`
4. Or try demos to understand features

Enjoy using Patch CLI!
