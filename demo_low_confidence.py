#!/usr/bin/env python3
"""
Demo of low confidence fix scenario
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

print('\n$ sudo rm -rf /')
print('[-] Error (attempt 1/5):')
print('rm: /: Permission denied')
print('')
print('[*] Analyzing error  ', end='', flush=True)

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

print('\n[*] Suggested fix: sudo rm -rf /tmp/*:::45:::')
print('[*] Confidence: 45% [Low - Uncertain]')
print('[!] Warning: Low confidence fix because the command is destructive and could remove more files than intended. Consider manual review.')

print('\nWhat do you want to do?')
print('  [1] Apply suggested fix')
print('  [2] Retry (get alternative suggestion)')
print('  [3] Enter custom command')
print('  [4] Exit')
print('\n[?] Select option (1-4): 3')
print('[->] Enter new command: sudo rm -rf /tmp/cache/*')
print('\n[*] Trying new command...')

print('\n$ sudo rm -rf /tmp/cache/*')
print('[!] Warning: This command uses sudo. Continue? (y/n): y')

print('[+] Success!')

print('\n[!] Done!')