# Error Handling in Patch CLI

## Overview

Patch CLI includes comprehensive error handling for all common OpenAI API issues, providing clear user guidance and direct links to solutions.

## Error Types Handled

### 1. Invalid API Key (AuthenticationError)
```bash
[*] Analyzing error ⠓
[!] Error: Invalid OpenAI API key.
[!] Please check your API key and try again.
[!] Set it with: export OPENAI_API_KEY="your-key-here"
[!] Get a new key at: https://platform.openai.com/api-keys
```

**When this happens:**
- Wrong API key entered
- API key not set in environment
- API key corrupted/malformed

**Solution:**
1. Get valid API key from https://platform.openai.com/api-keys
2. Set environment variable: `export OPENAI_API_KEY="sk-..."`
3. Restart the script

---

### 2. Rate Limit Exceeded (RateLimitError)
```bash
[*] Analyzing error ⠓
[!] Error: OpenAI API rate limit exceeded.
[!] You have reached your request limit or exceeded your quota.
[!] Please check your usage at: https://platform.openai.com/usage
[!] Ensure you have sufficient credits on your OpenAI account.
```

**When this happens:**
- Free tier limits reached
- Paid tier quota exceeded
- Too many requests in short time
- No credits remaining

**Solution:**
1. Check usage: https://platform.openai.com/usage
2. Add credits to your OpenAI account
3. Wait for quota reset (for rate limits)

---

### 3. Request Timeout (APITimeoutError)
```bash
[*] Analyzing error ⠓
[!] Error: OpenAI API request timed out.
[!] Please check your internet connection and try again.
```

**When this happens:**
- Network is slow or unstable
- OpenAI servers slow to respond
- Firewall blocking requests

**Solution:**
1. Check internet connection
2. Try again with better network
3. Check firewall settings

---

### 4. Connection Error (APIConnectionError)
```bash
[*] Analyzing error ⠓
[!] Error: Could not connect to OpenAI servers.
[!] Details: Connection refused
[!] Please check your internet connection and try again.
```

**When this happens:**
- No internet connection
- DNS resolution failure
- OpenAI servers down (rare)

**Solution:**
1. Verify internet connectivity
2. Test connection: `ping api.openai.com`
3. Check OpenAI status page

---

### 5. General API Error (APIError)
```bash
[*] Analyzing error ⠓
[!] Error: OpenAI API error occurred.
[!] Details: Insufficient quota
[!] This might be an issue with OpenAI services. Please try again later.
```

**When this happens:**
- Account suspended
- Model not available
- Quota issues
- Service outage

**Solution:**
1. Check OpenAI status
2. Review account status
3. Contact OpenAI support if needed

---

## Implementation Details

### Code Structure
```python
from openai import OpenAI, AuthenticationError, APITimeoutError, 
                     RateLimitError, APIConnectionError, APIError

try:
    response = client.chat.completions.create(...)
except AuthenticationError:
    # Handle invalid key
except RateLimitError:
    # Handle rate limits
except APITimeoutError:
    # Handle timeouts
except APIConnectionError:
    # Handle connection issues
except APIError:
    # Handle general errors
except Exception:
    # Handle unexpected errors
```

### Key Features

1. **Specific Error Messages**: Each error type has unique, actionable guidance
2. **User-Friendly**: Clear instructions without technical jargon
3. **Direct Links**: URLs to relevant OpenAI pages
4. **Exit Gracefully**: Clean exit after error, no confusing tracebacks
5. **API Key Validation**: Pre-flight check for obviously invalid keys

### Behavior

- Errors halt execution with helpful message (no confusing Python tracebacks)
- Each error suggests specific solution steps
- Includes links to relevant OpenAI platform pages
- Exits gracefully with code 1 (error status)

---

## Testing Error Handling

Run the error handling demo:
```bash
python3 demo_errors.py
```

This demonstrates all error scenarios and their solutions.

---

## Common Troubleshooting

| Issue | Check |
|-------|-------|
| API key not working | Verify it starts with `sk-` and is 51 chars |
| Rate limit errors | Check OpenAI Usage page |
| Connection issues | Test: `ping api.openai.com` |
| Timeout errors | Check network speed and stability |
| General errors | Try again later, check OpenAI status |

## Getting Help

- OpenAI Platform: https://platform.openai.com/
- API Keys: https://platform.openai.com/api-keys
- Usage: https://platform.openai.com/usage
- Status Page: https://status.openai.com/

## Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for API keys
3. **Check quota before intensive use**
4. **Monitor usage** to avoid surprises
5. **Have backup API keys** ready

