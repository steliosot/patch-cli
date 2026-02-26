#!/usr/bin/env python3
"""
Demo of retry functionality - getting an alternative suggestion
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

print('\n$ python script.py')
print('[-] Error (attempt 1/5):')
print('python: can not open file script.py')
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

print('\n[*] Suggested fix: python script.py --help:::70:::')
print('[*] Confidence: 70% [Medium]')
print('[!] This might not be the right script name.')

print('\nWhat do you want to do?')
print('  [1] Apply suggested fix')
print('  [2] Retry (get alternative suggestion)')
print('  [3] Enter custom command')
print('  [4] Exit')
print('\n[?] Select option (1-4): 2')
print('\n[*] Asking for alternative suggestion (retry 1/3)...')

# Simulate alternative suggestion
print('\n[*] Analyzing error  ', end='', flush=True)

stop = False
cursor_thread = threading.Thread(target=cursor_loop)
cursor_thread.start()
time.sleep(1.5)
stop = True
cursor_thread.join()

print('\r[*] Analyzing error       ', end='', flush=True)
print('\n[+] Done\n')

print('\n[*] Suggested fix: python3 script.py:::85:::')
print('[*] Confidence: 85% [High]')

print('\nWhat do you want to do?')
print('  [1] Apply suggested fix')
print('  [2] Retry (get alternative suggestion)')
print('  [3] Enter custom command')
print('  [4] Exit')
print('\n[?] Select option (1-4): 1')

print('\nAbout to run:')
print('──────────────')
print('python3 script.py')
print('──────────────')
print('Proceed? (y/n): y')

print('\n[*] Applying fix...')

print('\n$ python3 script.py')
print('[+] Success!')

print('\n[!] Done!')