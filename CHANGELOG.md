# Changelog

## Version 1.0.0 - Initial Release

### Core Features
- A
### Piped Command Support *(New!)*
- Full support for piped and chained shell commands
- Simple pipes: `curl -fsSL url | bash`
- Multiple pipes: `cmd1 | cmd2 | cmd3`
- Pipe-to-shell detection (`| bash`, `| sh`, `| zsh`)
- Safety warnings for script execution
- Format separator changed to `:::` from `|`
- Atomic single shell invocation
- Full pipeline preservation
- Cross-platform (macOS/Linux)
- Command passed unchanged: `' '.join(sys.argv[1:])`
- Parser updated: `rsplit(':::', 2)` instead of `rsplit('|', 2)`
- Backward compatible parser
- Retry system preserves pipelines
- Pipe-to-shell warnings require confirmation
- Demo script: `demo_piped.py`
- Documentation: `PIPED_COMMANDS.md`

### Demo Scripts *(Updated!)*
- `demo_progress.py` - High confidence (95%)
- `demo_medium_confidence.py` - Medium confidence with tips (78%)
- `demo_low_confidence.py` - Low confidence with warnings (45%)
- `demo_retry.py` - Retry functionality demonstration
- `demo_errors.py` - Error handling demonstration
- `demo_piped.py` - **NEW**: Piped commands demonstrationI-powered command fixing using OpenAI GPT-4o-mini
- Real-time progress feedback with spinner animation
- Intelligent confidence scoring (High/Medium/Low)
- Interactive decision menu with multiple options
- Command preview box before execution
- Sudo command warnings
- Persistent error tracking
- ASCII logo branding

### Menu Options
- [1] Apply suggested fix
- [2] Retry (get alternative suggestion) *(New!)*
- [3] Enter custom command
- [4] Exit

### Retry Feature
- Request alternative suggestions from OpenAI
- Limited to 3 retries per error
- Context-aware: "Previous suggestion X didn't work, try different approach"
- Useful when initial fix doesn't match use case

### Confidence Scoring
- **High (85%+)**: Simple fixes, obvious typos
- **Medium (60-84%)**: Context-dependent with helpful tips
- **Low (<60%)**: Detailed warnings with explanations of uncertainty

### Visual Feedback
- `[*]` - Information
- `[+]` - Success
- `[-]` - Error
- `[!]` - Warning
- `[->]` - Action prompt
- `[?]` - Question

### Safety Features
- No auto-execution without approval
- Command confirmation before run
- Interactive menu for all actions
- Sudo command warnings
- 5 attempt maximum to prevent loops

### Demo Scripts
- `demo_progress.py` - High confidence (95%)
- `demo_medium_confidence.py` - Medium confidence with tips (78%)
- `demo_low_confidence.py` - Low confidence with warnings (45%)
- `demo_retry.py` - Retry functionality demonstration

### Requirements
- Python 3.9+
- openai>=1.0.0
- tqdm

### Error Handling
- Invalid API key detection with helpful instructions *(New!)*
- Rate limit exceeded warnings with usage check link
- Request timeout handling
- Network connection error handling
- General API error handling
- Clear user-friendly error messages
- Direct links to OpenAI platform for resolution

### Future Enhancements
- Configuration file (~/.patchrc)
- Dry run mode
- Command history
- Multi-provider support (Anthropic, Ollama)
- Auto-apply threshold for high confidence fixes
- Interactive shell mode
- Batch mode
