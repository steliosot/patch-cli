#!/usr/bin/env python3
"""
Demo of piped command support - curl ... | bash
"""

logo = r"""
██████╗  █████╗ ████████╗ ██████╗██╗  ██╗
██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║  ██║
██████╔╝███████║   ██║   ██║     ███████║
██╔═══╝ ██╔══██║   ██║   ██║     ██╔══██║
██║     ██║  ██║   ██║   ╚██████╗██║  ██║
╚═╝     ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝


> your broken command has been patched
"""
print(logo)

# Demo 1: Piped command with bash
print('\n$ curl -fsSL https://openclaw.ai/install.sh | bash')
print('[-] Error (attempt 1/5):')
print('curl: (6) Could not resolve host: openclaw.ai')

# Simulate error analysis
print('\n[*] Analyzing error  ', end='', flush=True)

import time
import threading

cursor_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
stop = False

def cursor_loop():
    i = 0
    while not stop:
        cursor = cursor_chars[i % len(cursor_chars)]
        print(f'\r[*] Analyzing error {cursor}   ', end='', flush=True)
        time.sleep(0.1)
        i += 1

cursor_thread = threading.Thread(target=cursor_loop)
cursor_thread.start()
time.sleep(1.5)
stop = True
cursor_thread.join()

print('\r[*] Analyzing error       ', end='', flush=True)
print('\n[+] Done\n')

print('\n[*] Suggested fix: curl -fsSL https://example.com/install.sh | bash:::95:::')
print('[*] Confidence: 95% [High]')

print('\nWhat do you want to do?')
print('  [1] Apply suggested fix')
print('  [2] Retry (get alternative suggestion)')
print('  [3] Enter custom command')
print('  [4] Exit')
print('\n[?] Select option (1-4): 1')

# Show pipe-to-shell warning
print('\n[!] WARNING: This command will execute a remote or local script through piped shell.')
print('[!] Pattern detected: pipes to bash|sh|zsh')
print('[!] The script will be downloaded and executed with full shell privileges.')
print('[!] Continue anyway? (y/n): y')

print('\nAbout to run:')
print('──────────────────────────────────────────────')
print('curl -fsSL https://example.com/install.sh | bash')
print('──────────────────────────────────────────────')
print('Proceed? (y/n): y')

print('\n[*] Applying fix...')

print('\n$ curl -fsSL https://example.com/install.sh | bash')
print('[+] Success!')

print()
print('='*60)
print('   Demo 2: Multiple pipes')
print('='*60)

print('\n$ ps aux | grep python | grep -v grep')
print('[+] Success!')
print('   Output correctly shows Python processes')

print()
print('='*60)
print('   Pipe-to-Shell Detection')
print('='*60)

print('\n[!] Pattern detection for:')
print('  - | bash  ──> Remote/local script execution')
print('  - | sh    ──> Script execution')
print('  - | zsh   ──> Script execution')

print('\n[*] Other pipes (| grep, | awk, etc.) execute without warning:')
print('  - ps aux | grep python')
print('  - cat file.txt | grep pattern')
print('  - curl url | jq .')

print()
print('='*60)
print('   Pipeline Preservation')
print('='*60)

print('\n[*] Features:')
print('✓  Full command passed to subprocess.run(cmd, shell=True)')
print('✓  No splitting or tokenization')
print('✓  Preserves pipes, redirects, and chained commands')
print('✓  Cross-platform compatibility (macOS/Linux')

print('\n[*] Example commands supported:')
print('  - curl -fsSL url | bash')
print('  - cmd1 | cmd2 | cmd3')
print('  - ls -la | grep pattern | head -10')
print('  - curl url | python -m json.tool | less')

print('\n[!] Done!')