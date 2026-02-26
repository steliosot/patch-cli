#!/usr/bin/env python3
"""
Demo of medium confidence fix with reason
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

print('\n$ npm install react')
print('[-] Error (attempt 1/5):')
print('npm ERR! could not determine executable to run')
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

print('\n[*] Suggested fix: npm install react --save:::78:::')
print('[*] Confidence: 78% [Medium]')
print('[!] This fix should work but you might want to add --save-exact for exact version.')

print('\nWhat do you want to do?')
print('  [1] Apply suggested fix')
print('  [2] Retry (get alternative suggestion)')
print('  [3] Enter custom command')
print('  [4] Exit')
print('\n[?] Select option (1-4): 1')

print('\nAbout to run:')
print('──────────────')
print('npm install react --save')
print('──────────────')
print('Proceed? (y/n): y')

print('\n[*] Applying fix...')

print('\n$ npm install react --save')
print('[+] Success!')

print('\n[!] Done!')