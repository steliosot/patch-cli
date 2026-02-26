# Piped Command Support in Patch CLI

## Overview

Patch CLI now fully supports piped and chained shell commands, including complex pipelines with multiple operations.

## Supported Command Types

### Simple Pipes
```bash
python3 patch.py "curl -fsSL https://example.com/install.sh | bash"
python3 patch.py "ps aux | grep python"
python3 patch.py "cat file.txt | grep pattern"
```

### Multiple Pipes
```bash
python3 patch.py "ps aux | grep python | grep -v grep"
python3 patch.py "ls -la | grep pattern | head -10"
python3 patch.py "curl url | python -m json.tool | less"
```

### Chained Commands
```bash
python3 patch.py "curl -fsSL https://example.com/install.sh | bash && echo Done"
python3 patch.py "cmd1 | cmd2; cmd3 | cmd4"
```

### Pipes with Redirects
```bash
python3 patch.py "curl -fsSL https://example.com/data.json 2>&1 | jq .key > output.txt"
python3 patch.py "ls -la | grep txt 2>/dev/null | wc -l"
```

---

## Pipe-to-Shell Detection

Patch CLI automatically detects when a command pipes to a shell interpreter and shows safety warnings.

### Detected Patterns
- `| bash` - Execute downloaded script in bash
- `| sh` - Execute downloaded script in sh
- `| zsh` - Execute downloaded script in zsh

### Warning Display
```bash
$ curl -fsSL https://openclaw.ai/install.sh | bash

[!] WARNING: This command will execute a remote or local script 
    through piped shell.
[!] Pattern detected: pipes to bash|sh|zsh
[!] The script will be downloaded and executed with full shell 
    privileges.
[!] Continue anyway? (y/n):
```

### Harmless Pipes (No Warning)
```bash
$ ps aux | grep python        # No warning
$ curl url | jq .key          # No warning
$ cat file | wc -l            # No warning
```

---

## Technical Implementation

### Command Preservation

The tool captures the full command string exactly as entered:
```python
original_cmd = ' '.join(sys.argv[1:])
```

**With quotes:** `python3 patch.py "curl ... | bash"`
- `sys.argv[1:] = ["curl ... | bash"]` → Joined as-is
- Piped command preserved exactly

### Format Separator Change

**Why change?** The old format `command|confidence|reason` conflicted with shell pipelines.

**Old format:**
```python
# AI returns: "curl -fsSL url | bash|95|good"
# Parsing breaks: pipe mistaken for separator!
parts = rsplit('|', 2)  # ❌ WRONG
```

**New format:**
```python
# AI returns: "curl -fsSL url | bash:::95:::good"
# Parsing works: ::: never conflicts
parts = rsplit(':::', 2)  # ✓ CORRECT
```

**System prompt update:**
```python
system_prompt = 'Return: "command:::confidence:::reason"'
system_prompt += 'IMPORTANT: Use ::: as separator'
system_prompt += 'Shell commands may contain | characters'
```

### Parser Update

```python
# Old (broken for pipes)
if '|' in fix and fix.count('|') >= 2:
    parts = fix.rsplit('|', 2)

# New (works with pipes)
if ':::' in fix and fix.count(':::') >= 2:
    parts = fix.rsplit(':::', 2)
```

### Atomic Execution

Piped commands executed as single shell invocation:

```python
result = subprocess.run(
    cmd,  # Full command string (no splitting)
    shell=True,  # Use shell for pipes
    capture_output=True,
    text=True
)
```

**Why atomic?** Breaking pipeline into separate subprocess calls would break pipe chains:
```python
# WRONG - would break pipes
subprocess.run('curl -fsSL url')  # Command 1
subprocess.run('bash')             # Command 2 (loses stdin!)

# RIGHT - preserves pipe
subprocess.run('curl -fsSL url | bash', shell=True)
```

---

## Cross-Platform Compatibility

### Shell Selection
The tool relies on `/bin/bash` or `/bin/sh` which exists on both macOS and Linux.

```python
# Platform-agnostic shell selection
shell = '/bin/bash' if os.path.exists('/bin/bash') else '/bin/sh'
subprocess.run(cmd, shell=True, executable=shell)
```

### Tested Platforms
- **macOS**: 12.x, 13.x, 14.x
- **Linux**: Ubuntu, Debian, CentOS, Fedora

### Test Commands

```bash
# Simple pipe
python3 patch.py "ls -la | grep txt"

# Multiple pipes
python3 patch.py "ps aux | grep python | head -5"

# Pipe-to-shell
python3 patch.py "curl -fsSL url | bash"

# Redirects + pipes
python3 patch.py "curl url 2>&1 | grep -v timeout | tee output.txt"
```

---

## Retry System with Piped Commands

### Retries Preserve Pipeline
When a piped command fails and you retry:

1. First attempt: `curl bad-url | bash` → FAIL
2. Retry asks AI for alternative
3. AI suggests: `curl good-url | bash` ✓ PIPED COMMAND PRESERVED
4. Second attempt: Execute full pipeline

### Example Flow
```bash
$ curl -fsSL https://bad-url.com/install.sh | bash

[-] Error: curl: (6) Could not resolve host: bad-url.com

[*] Suggested fix: curl -fsSL https://good-url.com/install.sh | bash
[*] Confidence: 95% [High]

[?] Select option (1-4): 2  # Retry

[*] Asking for alternative suggestion (retry 1/3)...

[*] Suggested fix: curl -fsSL https://good-url.com/install.sh | bash
[*] Confidence: 95% [High]

[?] Select option (1-4): 1

About to run:
────────────────────────────────────────────
curl -fsSL https://good-url.com/install.sh | bash
────────────────────────────────────────────
Proceed? (y/n): y

[+] Success!
```

---

## Safety Features

### Sudo + Pipe Detection
Both warnings combined:
```bash
$ sudo curl -fsSL url | bash

[!] Warning: This command uses sudo. Continue? (y/n):
[!] WARNING: Piped shell execution detected!

[!] This command will execute a remote script with sudo privileges
[!] Pattern: pipes to bash|sh|zsh with sudo
[!] Continue anyway? (y/n):
```

### Confirmation Required
Always asks before executing piped shell commands:
- Even with auto-accept enabled
- Even with high confidence fixes
- User must explicitly approve

---

## Common Piped Command Scenarios

### 1. Script Installation
```bash
python3 patch.py "curl -fsSL https://raw.githubusercontent.com/.../install.sh | bash"

# Detection: | bash pattern
# Warning: Script execution
# Confirmation: Required
```

### 2. Log Processing
```bash
python3 patch.py "tail -100 /var/log/syslog | grep error | cut -d: -f4 | sort | uniq"

# Detection: No | bash|sh|zsh
# Warning: None (data processing only)
# Confirmation: Normal
```

### 3. Pipeline Debugging
```bash
python3 patch.py "curl -s https://api.example.com/data | jq .key | grep value"

# Detection: No | bash|sh|zsh
# Warning: None (data transformation)
# Confirmation: Normal
```

---

## Edge Cases

### Quoted Arguments
```bash
# Correct way
python3 patch.py "curl -fsSL 'https://example.com/install.sh' | bash"

# Wrong (shell parses quotes)
python3 patch.py curl -fsSL 'https://example.com/install.sh' | bash
```

### Nested Pipes
```bash
python3 patch.py "docker exec container sh -c 'cat file | grep pattern'"

# Outer pipes: shell handles
# Inner pipes: in quotes, part of sh -c command
# Detection: Works correctly
```

### Heredocs with Pipes
```bash
python3 patch.py "cat <<EOF | bash
command1
command2
EOF"

# Detection: | bash pattern
# Warning: Script execution (from heredoc)
# Correctly preserved
```

---

## Testing Piped Commands

### Run the Demo
```bash
python3 demo_piped.py
```

This demonstrates:
1. Simple piped command
2. Pipe-to-shell warning
3. Multiple pipe support
4. Pipeline preservation
5. Cross-platform compatibility

### Manual Testing
```bash
# Test 1: Simple pipe
python3 patch.py "echo hello | rev"

# Test 2: Multiple pipes  
python3 patch.py "ps aux | grep patch | head -1"

# Test 3: Pipe-to-shell (check warning)
python3 patch.py "curl -fsSL https://example.com/test.sh | bash"

# Test 4: Redirects + pipes
python3 patch.py "curl -s https://api.example.com/data 2>&1 | jq . > out.json"
```

---

## Troubleshooting

### Pipe Character Lost
**Problem:** Piped command works manually but breaks in patch.py

**Solution:** Use quotes around the command:
```bash
# Wrong
python3 patch.py curl http://example.com | bash

# Right
python3 patch.py "curl http://example.com | bash"
```

### AI Returns Broken Format
**Problem:** AI uses `|` instead of `:::`

**Solution:** System prompt updated - AI returns:
```
curl -fsSL url | bash:::95:::good fix
```

### Pipe-to-Shell Not Detected
**Problem:** No warning for dangerous pipes

**Solution:** Detection patterns:
- `| bash` (with/without space)
- `| sh`
- `| zsh`

### macOS vs Linux Command Differences
**Problem:** Same command fails on different systems

**Solution:** Use POSIX-compliant commands. Patch doesn't modify commands, so differences are expected.

---

## Migration from Old Format

### Commands You've Used
All existing commands work the same - no migration needed!

### AI Response Format
- **Old:** `"git push|95|obvious"`
- **New:** `"git push:::95:::obvious"`

### Parser Handles Both
```python
# Backward兼容性
if ':::' in fix:
    # New format
    parts = rsplit(':::', 2)
elif '|' in fix:
    # Old format (still works)
    parts = rsplit('|', 2)
```

---

## Performance Considerations

### Piped Command Overhead
- Minimal: Single shell invocation
- Same as running command manually
- No additional subprocess calls

### Memory Usage
- Captures stdout/stderr (same as normal)
- No additional memory allocation

### Security
- Same security as running command manually in shell
- No additional attack surface

---

## Best Practices

### 1. Always Quote Piped Commands
```bash
# OK
python3 patch.py "cmd1 | cmd2 | cmd3"

# BAD
python3 patch.py cmd1 | cmd2 | cmd3
```

### 2. Review Pipe-to-Shell Commands
```bash
# Before accepting
[!] WARNING: This command will execute a remote script...

# Check: Is this script trusted?
# Only accept if you verified the source
```

### 3. Test Piped Commands Separately
```bash
# Test outside patch.py first
curl -fsSL url | cat | head -10

# If works, then use patch.py
python3 patch.py "curl -fsSL url | cat | head -10"
```

### 4. Use Multi-Pipe for Debugging
```bash
# Add | head -10 to limit output
curl -fsSL url | bash | head -10

# Add | tee to save and display
curl -fsSL url | bash | tee install.log
```

---

## Limitations

### Platform Scope
- **Supported:** macOS, Linux (bash/zsh)
- **Not supported:** Windows (PowerShell/cmd.exe)

### Shell Requirements
- Requires `subprocess.run(cmd, shell=True)` support
- Works with `/bin/bash` and `/bin/sh`

### Command Length
- Same as shell: up to ARG_MAX limitation
- Typically 128KB-2MB depending on system

### Escaped Quotes
- Patch.py doesn't modify quoting
- Relies on shell quote handling
- Use single quotes in outer command: `python3 patch.py "cmd 'arg'"`

---

## Future Enhancements

### Planned Features
- [ ] Windows PowerShell support
- [ ] Interactive pipe preview
- [ ] Pipe optimization suggestions
- [ ] Command templates for common pipelines

### Requested Features
- [ ] Pipeline visualization
- [ ] Pipe timing analysis
- [ ] Piped command history
- [ ] Pipeline debugging mode

---

## Summary

Patch CLI now provides **complete piped command support**:

✓ Simple and multi-pipe commands  
✓ Pipe-to-shell detection and warnings  
✓ Full pipeline preservation  
✓ Atomic single shell execution  
✓ Cross-platform (macOS/Linux)  
✓ Format separator change: `:::` instead of `|`  
✓ Backward compatible parser  
✓ Retry system preserves pipelines  
✓ Safety warnings for dangerous operations  

For testing, run: `python3 demo_piped.py`

---

## Quick Reference

| Feature | Command | Example |
|---------|---------|---------|
| **Simple pipe** | Any | `cat file | grep pat` |
| **Multiple pipes** | Any | `ps aux | grep python | head` |
| **Pipe-to-shell warning** | `| bash\|sh\|zsh` | `curl ... \| bash` |
| **No warning** | Non-shell | `ps aux \| grep` |
| **Preserved** | All pipes | Full command string |
| **Execution** | Atomic | Single shell call |
| **Format** | New | `cmd:::conf:::reason` |

---

**For more information:**
- See `README.md` for usage
- See `FEATURES.md` for all features  
- See `demo_piped.py` for interactive demo