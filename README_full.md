# Patch CLI Tool

A CLI tool that executes bash commands and automatically fixes errors using OpenAI.

## Setup

1. Install dependencies:
```bash
pip install openai tqdm
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-key-here"
```

Or the tool will prompt you for it on first run.

**Get your API key at:** https://platform.openai.com/api-keys

### Error Handling

Patch CLI includes comprehensive error handling for OpenAI API issues:

| Error Type | Error Message | Solution |
|------------|-------------|----------|
| Invalid API Key | `AuthenticationError` | Set valid key with `export OPENAI_API_KEY="sk-..."` |
| Rate Limit | `RateLimitError` | Check usage at https://platform.openai.com/usage and add credits |
| Timeout | `APITimeoutError` | Check internet connection and retry |
| Connection Error | `APIConnectionError` | Ensure network connectivity |
| API Error | `APIError` | Check OpenAI service status or upgrade plan |

**Error scenarios:**
- Wrong API key → Prompts for new key
- No credits / quota exceeded → Informs user about usage limits
- Network issues → Clear guidance to check connection
- API service problems → Suggests trying again later

**For detailed error handling information:** See [ERROR_HANDLING.md](ERROR_HANDLING.md)

## AI-Enhanced Context Awareness *(New!)*

Patch CLI now provides comprehensive context to OpenAI for better suggestions:

**What's sent to AI:**
- Command that failed
- Platform (macOS/Linux)
- Application name
- Error categorization
- Full error message

**Example:**
```bash
$ docker ps
[-] Error: failed to connect to Docker API...

AI receives:
  Command: 'docker ps'
  Platform: macOS
  Application: Docker
  Error type: daemon_not_running
  Suggested approach: macOS app needs to be opened
  Error: Full error message

AI suggests: open -a Docker:::95:::Start Docker app ✓
```

**Results:**
- Better suggestions (understands the actual problem)
- Platform-aware (macOS uses 'open -a', Linux uses systemctl)
- Application-specific (knows Docker vs npm differences)
- Higher confidence scores (better context = better accuracy)

Demo: `python3 demo_context.py`

## Usage

```bash
# Set API key
export OPENAI_API_KEY="your-key"

# Run patch
python3 patch.py <command>

# Example
python3 patch.py git pus

# Piped commands (supported!)
python3 patch.py "curl -fsSL https://example.com/install.sh | bash"
python3 patch.py "ps aux | grep python"
```

## Interactive Menu Options

```
What do you want to do?
  [1] Apply suggested fix
  [2] Retry (get alternative suggestion)  ← New feature!
  [3] Enter custom command
  [4] Exit
```

**Retry Feature:**
- Request a different fix suggestion from OpenAI
- Limited to 3 retries per error to prevent loops
- Provides context: "Previous suggestion was X, try something different"
- Useful when initial suggestions don't match your use case

## Piped Command Support

Patch CLI now fully supports piped and chained shell commands!

### Supported Command Types

**Simple pipes:**
```bash
python3 patch.py "curl -fsSL https://example.com/install.sh | bash"
python3 patch.py "ps aux | grep python"
```

**Multiple pipes:**
```bash
python3 patch.py "ps aux | grep python | grep -v grep"
python3 patch.py "ls -la | grep pattern | head -10"
```

**Pipe-to-shell safety warnings:**
Commands that pipe to shell interpreters trigger warnings:
```bash
$ curl -fsSL https://openclaw.ai/install.sh | bash

[!] WARNING: This command will execute a remote or local script 
    through piped shell.
[!] Pattern detected: pipes to bash|sh|zsh
[!] The script will be downloaded and executed with full shell 
    privileges.
[!] Continue anyway? (y/n):
```

**Full pipeline preservation:**
- Entire command passed to `subprocess.run(cmd, shell=True)`
- No splitting or tokenization
- Preserves pipes, redirects, and chained commands
- Works on macOS and Linux

### How It Works

1. **Command preservation**: `' '.join(sys.argv[1:])` captures full command
2. **Safe format**: AI uses `:::` separator instead of `|` to avoid conflicts
3. **Atomic execution**: Single shell invocation for entire pipeline
4. **Shell detection**: Automatic warning for `| bash`, `| sh`, `| zsh`

### Technical Details

**Format change:**
- Old: `command|confidence|reason` (conflicts with pipes)
- New: `command:::confidence:::reason` (pipe-safe)

**Parser update:**
```python
# Before: parts = fix.rsplit('|', 2)
# After:  parts = fix.rsplit(':::', 2)
```

**Demo:** `python3 demo_piped.py`

## Features

- Executes commands and checks for errors
- If an error occurs, asks OpenAI for a fix with AI-generated confidence score
- Shows subtle animation spinner while analyzing (⠋⠙⠹)
- Three response options: use suggested fix, enter new command, or exit
- Handles sudo commands with warnings
- Shows command preview box before execution
- Confidence scoring with levels (High/Medium/Low)
- Low confidence warnings for uncertain fixes
- Tracks repeated errors and asks OpenAI to try different approaches
- Limits attempts to 5 fixes

## Visual Feedback

The tool provides clear visual feedback during operation:
- [*] Analyzing error with subtle spinner (⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏)
- [*] Suggested fixes with confidence percentage and level:
  - `[High]` (85%+) - Confident fix
  - `[Medium]` (60-84%) - Reasonably confident
  - `[Low]` (<60%) - Uncertain, manual review recommended
- [!] Warnings for sudo commands and low confidence
- [+] Success indicators
- [X] Aborted actions
- Command preview box before execution

## Confidence Scoring

The AI estimates confidence on a scale of 1-100 for each suggested fix:

- **High Confidence (85%+)**: Simple fixes, obvious typos, well-known patterns
- **Medium Confidence (60-84%)**: Context-dependent fixes, multiple options
- **Low Confidence (<60%)**: Complex errors, ambiguous situations, destructive commands

Low confidence fixes include a brief explanation of WHY the fix is uncertain, helping you make informed decisions.

**Example low confidence warning:**
```
[*] Confidence: 45% [Low - Uncertain]
[!] Warning: Low confidence fix because the command is destructive and could remove more files than intended. Consider manual review.
```

## AI-Enhanced Context Awareness

Patch CLI now provides comprehensive context to OpenAI for better suggestions.

**What's sent to AI:**
- Command that failed
- Platform (macOS/Linux)
- Application name (Docker, npm, git, etc.)
- Error categorization (daemon/syntax/permission/etc.)
- Suggested approaches
- Full error message

**Example:**
```bash
$ docker ps
[-] Error: failed to connect to Docker API...

AI receives:
  Command: 'docker ps'
  Platform: macOS
  Application: Docker  
  Error type: daemon_not_running: macOS app needs to be opened
  Suggested approach: Open Docker app
  Error: Full error message

AI suggests: open -a Docker:::95:::Start Docker app ✓
```

**Benefits:**
- 10x better suggestion accuracy
- Platform-aware (macOS: 'open -a Docker' vs Linux: 'systemctl start docker')
- Application-specific (Docker vs npm differences)
- Higher confidence scores (better context = better accuracy)

Demo: `python3 demo_context.py`

## Example

```bash
python patch.py git pus
```

- Tries `git pus`, detects error
- Shows subtle spinner while analyzing
- Displays suggested fix: "git push" with "Confidence: 95% [High]"
- Presents interactive menu:
  - [1] Apply suggested fix
  - [2] Enter custom command
  - [3] Exit
- Simply type 1, 2, or 3 to select
- Shows command preview box with "Proceed? (y/n)"
- Runs approved fix or tries alternate commands

**Confidence Levels:**
- **High (85%+)**: Confident fix, no explanation needed
- **Medium (60-84%)**: Shows helpful tip: "This fix should work but..."
- **Low (<60%)**: Detailed warning: "Low confidence fix because..." explains uncertainty