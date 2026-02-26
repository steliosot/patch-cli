#!/usr/bin/env python3
"""
Demo of OpenAI error handling
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

print('\n$ git pus')
print('[-] Error (attempt 1/5):')
print('git: "pus" is not a git command. See "git --help".')

# Simulate error scenarios
print('\n[*] Analyzing error  ', end='', flush=True)

import time
import threading

cursor_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

def demo_error_handling(error_type):
    """Demo different error handling scenarios"""
    if error_type == 'auth':
        print('\n[!] Error: Invalid OpenAI API key.')
        print('[!] Please check your API key and try again.')
        print('[!] Set it with: export OPENAI_API_KEY="your-key-here"')
        print('[!] Get a new key at: https://platform.openai.com/api-keys')
    elif error_type == 'rate':
        print('\n[!] Error: OpenAI API rate limit exceeded.')
        print('[!] You have reached your request limit or exceeded your quota.')
        print('[!] Please check your usage at: https://platform.openai.com/usage')
        print('[!] Ensure you have sufficient credits on your OpenAI account.')
    elif error_type == 'timeout':
        print('\n[!] Error: OpenAI API request timed out.')
        print('[!] Please check your internet connection and try again.')
    elif error_type == 'network':
        print('\n[!] Error: Could not connect to OpenAI servers.')
        print('[!] Details: Connection refused')
        print('[!] Please check your internet connection and try again.')
    elif error_type == 'quota':
        print('\n[!] Error: OpenAI API error occurred.')
        print('[!] Details: Insufficient quota')
        print('[!] This might be an issue with OpenAI services. Please try again later.')

# Demo auth error
print('\n[*] Analyzing error ⠋    ', flush=True)
time.sleep(0.5)
print('\n[*] Analyzing error       ', flush=True)
print('\n[!] Error: Invalid OpenAI API key.')
print('[!] Please check your API key and try again.')
print('[!] Set it with: export OPENAI_API_KEY="your-key-here"')
print('[!] Get a new key at: https://platform.openai.com/api-keys')

print('\n[!] Scenario 1: Invalid API Key')
print('    Fix: Export correct key: export OPENAI_API_KEY="sk-..."')
print()

# Demo rate limit
print('[*] Retrying...')
print('\n[*] Analyzing error       ', flush=True)
print('\n[!] Error: OpenAI API rate limit exceeded.')
print('[!] You have reached your request limit or exceeded your quota.')
print('[!] Please check your usage at: https://platform.openai.com/usage')
print('[!] Ensure you have sufficient credits on your OpenAI account.')

print('\n[!] Scenario 2: Rate Limit / No Credits')
print('    Fix: Add credits to your OpenAI account')

print('\n' + '='*60)
print('Common Error Scenarios & Solutions:')
print('='*60)

print('\n1. Invalid API Key')
print('   Error: AuthenticationError')
print('   Solution: Set valid API key with export OPENAI_API_KEY="sk-..."')
print()

print('2. Rate Limit Exceeded')
print('   Error: RateLimitError')
print('   Solution: Check usage at https://platform.openai.com/usage')
print('             Add credits to your account')

print('3. Request Timeout')
print('   Error: APITimeoutError')
print('   Solution: Check internet connection and try again')

print('4. Connection Error')
print('   Error: APIConnectionError')
print('   Solution: Ensure you have internet access')

print('5. Insufficient Quota')
print('   Error: APIError (quota)')
print('   Solution: Upgrade your OpenAI plan or add credits')

print('\n[!] For more help, visit: https://platform.openai.com/')

print('\n[!] Done!')