#!/usr/bin/env python3
"""
Demo of Patch CLI visual features without API key
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

# Simulate command execution
print('\n$ git pus')
print('[-] Error (attempt 1/5):')
print('git: "pus" is not a git command. See "git --help".')
print('')
print('The most similar commands are')
print('\tpush')
print('\tpull')

# Simulate analyzing with subtle animation spinner
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

print('\n[*] Suggested fix: git push:::95:::')
print('[*] Confidence: 95% [High]')
print('\nWhat do you want to do?')
print('  [1] Apply suggested fix')
print('  [2] Retry (get alternative suggestion)')
print('  [3] Enter custom command')
print('  [4] Exit')
print('\n[?] Select option (1-4): 1')

print('\nAbout to run:')
print('──────────────')
print('git push')
print('──────────────')
print('Proceed? (y/n): y')

print('\n[*] Applying fix...')

print('\n$ git push')
print('[+] Success!')

print('\n[!] Done!')