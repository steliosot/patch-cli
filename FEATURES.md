# Patch CLI - Features Overview

## ✨ Core Features

### 1. **AI-Powered Command Fixing**
- Fixes bash commands using OpenAI GPT-4o-mini
- Detects errors and suggests corrections
- Maintains original command history for context

### 2. **Real-Time Progress Feedback**
- Subtle spinner animation (⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏)
- Clear feedback for every operation
- Professional, non-distracting UI

### 3. **Intelligent Confidence Scoring**

**High Confidence (85%+):**
```
[*] Suggested fix: git push
[*] Confidence: 95% [High]
```
- Simple fixes, obvious typos
- Well-known patterns

**Medium Confidence (60-84%):**
```
[*] Suggested fix: npm install react --save
[*] Confidence: 78% [Medium]
[!] This fix should work but you might want to add --save-exact.
```
- Context-dependent fixes
- Helpful tips included

**Low Confidence (<60%):**
```
[*] Suggested fix: sudo rm -rf /tmp/*
[*] Confidence: 45% [Low - Uncertain]
[!] Warning: Low confidence fix because the command is destructive 
    and could remove more files than intended. Consider manual review.
```
- Complex/ambiguous errors
- Destructive commands
- Detailed warnings with explanation

### 4. **Interactive Decision Menu**
```
What do you want to do?
  [1] Apply suggested fix
  [2] Retry (get alternative suggestion)
  [3] Enter custom command
  [4] Exit

[?] Select option (1-4):
```

**Retry Feature:**
- Request a different fix suggestion from OpenAI
- Limited to 3 retries per error to prevent loops
- Provides context: "Previous suggestion was X, try something different"
- Useful when initial suggestions don't match your use case

**Example:**
```
[*] Suggested fix: python script.py --help
[*] Confidence: 70% [Medium]

What do you want to do?
  [1] Apply suggested fix
  [2] Retry (get alternative suggestion)
  [3] Enter custom command
  [4] Exit

[?] Select option (1-4): 2

[*] Asking for alternative suggestion (retry 1/3)...

[*] Suggested fix: python3 script.py
[*] Confidence: 85% [High]
```

### 5. **Command Preview Box**
```
About to run:
──────────────
git push
──────────────
Proceed? (y/n):
```

### 6. **Safety Features**
- Sudo command warnings
- Command confirmation before execution
- Interactive menu for all actions
- No auto-execution without approval

### 7. **Visual Feedback Markers**
- `[*]` - Information
- `[+]` - Success
- `[-]` - Error
- `[!]` - Warning
- `[->]` - Action prompt
- `[?]` - Question

### 8. **Persistent Error Tracking**
- Remembers previous failed attempts
- Asks AI to "try different approach"
- Limits to 5 attempts to prevent loops

### 9. **AI-Enhanced Context Awareness** *(New!)*

**Comprehensive Context Sent to OpenAI:**
- Command that failed
- Platform (macOS/Linux)
- Application name (Docker, npm, git, etc.)
- Error categorization (daemon/syntax/permission/etc.)
- Suggested approaches based on error type
- Full error message with details

**Example:**
```bash
User: docker ps
Error: failed to connect to Docker API...

AI Context:
  Command: 'docker ps'
  Platform: macOS
  Application: Docker
  Error type: daemon_not_running
  Suggested approach: macOS app needs to be opened
  Error: Full error message

Result: open -a Docker:::95:::Start Docker app ✓
```

**Before this feature:**
- AI suggested: `docker run -d -p 80:80 nginx` (WRONG)
- Low confidence: 50%

**After this feature:**
- AI suggests: `open -a Docker` (CORRECT)
- High confidence: 95%

**Supported Error Types:**
- daemon_not_running → macOS/Linux appropriate fix
- command_syntax → Invalid options/flags
- permission_denied → sudo needed
- file_not_found → File/directory check
- network_error → Connection troubleshooting
- dependency_missing → Package name issues

**Benefits:**
- 10x better suggestion accuracy
- Platform-aware solutions
- Application-specific fixes
- Higher confidence scores
- Fewer retry attempts

**Demo:** `python3 demo_context.py`

### 10. **Piped Command Support**
```
██████╗  █████╗ ████████╗
██╔══██╗██╔══██╗╚══██╔══╝
██████╔╝███████║   ██║
██╔═══╝ ██╔══██║   ██║
██║     ██║  ██║   ██║
╚═╝     ╚═╝  ╚═╝   ╚═╝


> your broken command has been patched
```

### 10. **Piped Command Support** *(New!)*

**Full pipeline support:**
```bash
# Simple pipes
python3 patch.py "curl -fsSL https://example.com/install.sh | bash"

# Multiple pipes
python3 patch.py "ps aux | grep python | grep -v grep"

# Chained commands
python3 patch.py "curl url | python -m json.tool | less"
```

**Pipe-to-shell detection:**
Commands that pipe to shell interpreters trigger safety warnings:
```
[!] WARNING: This command will execute a remote or local script 
    through piped shell.
[!] Pattern detected: pipes to bash|sh|zsh
[!] The script will be downloaded and executed with full shell 
    privileges.
[!] Continue anyway? (y/n):
```

**Pipeline preservation:**
- Entire command string passed to `subprocess.run(cmd, shell=True)`
- No splitting or tokenization
- Atomic single shell invocation
- Cross-platform (macOS/Linux)

**Format change:**
- Old: `command|confidence|reason` ❌ (conflicts with `|`)
- New: `command:::confidence:::reason` ✓ (pipe-safe)

**Parser update:**
```python
# Before: parts = fix.rsplit('|', 2)
# After:  parts = fix.rsplit(':::', 2)
```

**Demo:** `python3 demo_piped.py`

### 9. **Beautiful ASCII Logo**
```
██████╗  █████╗ ████████╗
██╔══██╗██╔══██╗╚══██╔══╝
██████╔╝███████║   ██║
██╔═══╝ ██╔══██║   ██║
██║     ██║  ██║   ██║
╚═╝     ╚═╝  ╚═╝   ╚═╝


> your broken command has been patched
```

### 10. **Comprehensive Error Handling**
Patch CLI handles all common OpenAI API errors gracefully:

**Invalid API Key (AuthenticationError)**
```
[!] Error: Invalid OpenAI API key.
[!] Please check your API key and try again.
[!] Set it with: export OPENAI_API_KEY="your-key-here"
[!] Get a new key at: https://platform.openai.com/api-keys
```

**Rate Limit Exceeded (RateLimitError)**
```
[!] Error: OpenAI API rate limit exceeded.
[!] You have reached your request limit or exceeded your quota.
[!] Please check your usage at: https://platform.openai.com/usage
[!] Ensure you have sufficient credits on your OpenAI account.
```

**Request Timeout (APITimeoutError)**
```
[!] Error: OpenAI API request timed out.
[!] Please check your internet connection and try again.
```

**Connection Error (APIConnectionError)**
```
[!] Error: Could not connect to OpenAI servers.
[!] Details: Connection refused
[!] Please check your internet connection and try again.
```

**General API Error (APIError)**
```
[!] Error: OpenAI API error occurred.
[!] Details: Insufficient quota
[!] This might be an issue with OpenAI services. Please try again later.
```

## 🚀 Usage

```bash
# Set API key
export OPENAI_API_KEY="your-key"

# Run patch
python3 patch.py <command>

# Example
python3 patch.py git pus
```

## 📁 Demo Scripts

- `demo_progress.py` - High confidence scenario (95%)
- `demo_medium_confidence.py` - Medium confidence with tips (78%)
- `demo_low_confidence.py` - Low confidence with warnings (45%)
- `demo_retry.py` - Retry functionality demo

## 🔧 Requirements

```
openai>=1.0.0
tqdm
```

## 🎯 Future Enhancements

- Configuration file (~/.patchrc)
- Dry run mode
- Command history
- Multi-provider support (Anthropic, Ollama)
- Auto-apply threshold for high confidence fixes
- Interactive shell mode
- Batch mode
