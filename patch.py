#!/usr/bin/env python3
import os
import sys
import subprocess
import threading
import time
import platform
import re
from openai import OpenAI, AuthenticationError, APITimeoutError, RateLimitError, APIConnectionError, APIError

stop_cursor = False

def validate_api_key(key):
    """Basic validation of OpenAI API key format."""
    if not key:
        return False
    if len(key) < 20:
        print('[!] Warning: API key seems too short. Please verify it.')
    return True

def get_api_key():
    key = os.environ.get('OPENAI_API_KEY')
    if not key:
        print('[!] OpenAI API key not found.')
        print('[!] Get your key at: https://platform.openai.com/api-keys')
        print('[!] Set it with: export OPENAI_API_KEY="your-key-here"')
        key = input('Enter your OpenAI API key: ').strip()
        if key:
            os.environ['OPENAI_API_KEY'] = key
    
    if not validate_api_key(key):
        print('[!] Invalid or missing API key.')
        print('[!] Script requires a valid OpenAI API key to function.')
        sys.exit(1)
    
    return key

def is_pipe_to_shell(cmd):
    """Detect if command pipes into shell interpreter (bash, sh, zsh)"""
    shell_pipes = ['| bash', '| sh', '| zsh']
    cmd_lower = cmd.lower().strip()
    for pipe in shell_pipes:
        if cmd_lower.endswith(pipe.lower()):
            return True
    return False

def is_interactive_command(cmd):
    """Detect if command requires interactive user input"""
    interactive_commands = [
        'adduser', 'useradd', 'passwd', 'chpasswd',
        'mysql', 'psql', 'sqlite3', 'mongosh', 'redis-cli',
        'vim', 'nano', 'vi', 'emacs',
        'less', 'more', 'top', 'htop',
        'ssh', 'telnet', 'ftp', 'sftp',
        'sudo apt-get install', 'sudo dnf install', 'sudo yum install',
    ]
    cmd_lower = cmd.lower()
    for base_cmd in interactive_commands:
        # Check if the base command is present (handle sudo, spaces)
        patterns = [
            f" {base_cmd} ",  # Command with spaces around
            f"^{base_cmd} ",   # Command at start
            f" {base_cmd}$",   # Command at end
            f" {base_cmd} ",   # Command in middle
        ]
        for pattern in patterns:
            if pattern.strip() in cmd_lower or cmd_lower.startswith(pattern.strip()):
                return True
    return False

def get_non_interactive_alternative(cmd):
    """Provide non-interactive alternatives for interactive commands"""
    cmd_lower = cmd.lower()
    alternatives = {
        'adduser': [
            'adduser --disabled-password --gecos "" {user}',
            'useradd -m {user}'
        ],
        'useradd': ['useradd -m {user}'],
        'mysql': ['mysql -e "{query}"', 'mysql -BNe "{query}"'],
        'psql': ['psql -c "{query}"'],
    }
    for base_cmd, alts in alternatives.items():
        if base_cmd in cmd_lower:
            return alts
    return None

def execute_command(cmd, check_for_sudo=False, force_interactive=False):
    print(f'\n$ {cmd}')
    
    # Check for sudo
    if check_for_sudo and cmd.startswith('sudo'):
        response = input('[!] Warning: This command uses sudo. Continue? (y/n): ')
        if response.lower() != 'y':
            print('[!] Aborted.')
            return None, None, False
    
    # Check for pipe-to-shell execution
    if is_pipe_to_shell(cmd):
        print('[!] WARNING: This command will execute a remote or local script through piped shell.')
        print('[!] Pattern detected: pipes to bash|sh|zsh')
        print('[!] The script will be downloaded and executed with full shell privileges.')
        response = input('[!] Continue anyway? (y/n): ')
        if response.lower() != 'y':
            print('[!] Aborted.')
            return None, None, False
    
    # Check for interactive command
    is_interactive = is_interactive_command(cmd)
    if is_interactive and not force_interactive:
        print('[!] WARNING: This command is INTERACTIVE and requires manual user input.')
        print('[!] The tool will not handle interactive prompts.')
        print('[!] You must interact with the command manually.')
        
        alternatives = get_non_interactive_alternative(cmd)
        if alternatives:
            print('\n[+] Non-interactive alternatives available:')
            for i, alt in enumerate(alternatives, 1):
                print(f'  [{i}] {alt}')
            print()
        
        response = input('[!] Continue anyway and handle prompts manually? (y/n): ')
        if response.lower() != 'y':
            print('[!] Aborted.')
            return None, None, False
    
    try:
        if is_interactive:
            # Interactive commands need to run without capturing output
            result = subprocess.run(cmd, shell=True, capture_output=False)
            return result.returncode, '', True  # is_interactive flag
        else:
            # Non-interactive commands: capture output for AI analysis
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode, result.stdout + result.stderr, False
    except Exception as e:
        return None, str(e), False

def get_file_system_context(cmd):
    """Gather information about the current directory and file structure"""
    context = []
    
    try:
        # Current working directory
        cwd = os.getcwd()
        context.append(f"Current working directory: {cwd}")
        
        # List contents of current directory (first level only, max 20 items)
        try:
            result = subprocess.run(['ls', '-1'], capture_output=True, text=True, cwd=cwd)
            if result.returncode == 0:
                items = result.stdout.strip().split('\n')[:20]
                context.append(f"Contents of current directory ({len(items)} items shown):")
                context.extend([f"  - {item}" for item in items if item])
        except:
            pass
        
        # If command involves /home/, list /home/ to show available users
        if '/home/' in cmd.lower():
            try:
                result = subprocess.run(['ls', '-1', '/home/'], capture_output=True, text=True)
                if result.returncode == 0:
                    users = result.stdout.strip().split('\n')[:20]
                    context.append(f"Available users in /home/:")
                    context.extend([f"  - {user}" for user in users if user])
            except:
                pass
        
        # If command involves cd to a path, check if that directory exists
        if 'cd ' in cmd.lower():
            import shlex
            parts = shlex.split(cmd)
            for i, part in enumerate(parts):
                if part == 'cd' and i + 1 < len(parts):
                    target_path = parts[i + 1]
                    if os.path.isdir(target_path):
                        context.append(f"Target directory EXISTS: {target_path}")
                        try:
                            result = subprocess.run(['ls', '-1', target_path], capture_output=True, text=True)
                            if result.returncode == 0:
                                items = result.stdout.strip().split('\n')[:20]
                                context.append(f"Contents of {target_path}:")
                                context.extend([f"  - {item}" for item in items if item])
                        except:
                            pass
                    else:
                        context.append(f"Target directory DOES NOT EXIST: {target_path}")
                    break
        
        # If command involves accessing a file, check if parent directory exists
        import shlex
        parts = shlex.split(cmd)
        for part in parts:
            if os.path.isfile(part):
                context.append(f"File EXISTS: {part}")
            elif not part.startswith('-') and '/' in part:
                parent_dir = os.path.dirname(part)
                if parent_dir and os.path.isdir(parent_dir):
                    try:
                        result = subprocess.run(['ls', '-1', parent_dir], capture_output=True, text=True)
                        if result.returncode == 0:
                            items = result.stdout.strip().split('\n')[:20]
                            context.append(f"Contents of parent directory {parent_dir}:")
                            context.extend([f"  - {item}" for item in items if item])
                    except:
                        pass
        
    except Exception as e:
        context.append(f"Error gathering file system context: {str(e)}")
    
    return '\n'.join(context)

def show_blinking_cursor():
    cursor_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    i = 0
    while not stop_cursor:
        cursor = cursor_chars[i % len(cursor_chars)]
        print(f'\r[*] Analyzing error {cursor}   ', end='', flush=True)
        time.sleep(0.1)
        i += 1
    print('\r[*] Analyzing error       ', end='', flush=True)

def get_platform_info():
    """Detect platform information"""
    system = platform.system()
    if system == 'Darwin':
        return 'macOS'
    elif system == 'Linux':
        return 'Linux'
    elif system == 'Windows':
        return 'Windows'
    else:
        return system

def get_app_info(command):
    """Detect application/service from command"""
    command_parts = command.lower().strip().split()
    if not command_parts:
        return None
    
    app_mapping = {
        'docker-compose': 'Docker Compose',
        'docker': 'Docker',
        'kubernetes': 'Kubernetes',
        'kubectl': 'Kubernetes (kubectl)',
        'git': 'Git',
        'npm': 'Node.js (npm)',
        'pip': 'Python (pip)',
        'aws': 'AWS CLI',
        'gcloud': 'Google Cloud CLI',
        'az': 'Azure CLI',
        'brew': 'Homebrew',
        'apt': 'apt (package manager)',
        'yum': 'yum (package manager)',
        'dnf': 'dnf (package manager)'
    }
    
    # Skip common prefixes like sudo
    prefixes_to_skip = ['sudo', 'time', 'env']
    
    for part in command_parts:
        if part in prefixes_to_skip:
            continue
        for key, value in app_mapping.items():
            # Check for exact match first
            if part == key:
                return value
    
    # If no exact match, try substring matches
    for part in command_parts:
        if part in prefixes_to_skip:
            continue
        for key, value in app_mapping.items():
            # Docker-compose check - make sure we don't match just 'docker'
            if key in part and (key == 'docker' and not part.startswith('docker-')):
                return value
            # Normal substring match
            if key in part:
                return value
    
    return None

def categorize_error_type(error_message, command):
    """Categorize the type of error to provide better context"""
    error_lower = error_message.lower()
    
    # Daemon/service not running
    daemon_patterns = [
        'daemon not running',
        'connect to the.*api',
        'no such file or directory.*docker.sock',
        'connection refused.*docker',
        'could not connect to server'
    ]
    for pattern in daemon_patterns:
        if re.search(pattern, error_lower):
            if 'macOS' in get_platform_info():
                return 'daemon_not_running: macOS: Use open -a Docker app'
            else:
                return 'daemon_not_running: Linux: Use systemctl start docker'
    
    # Permission/access denied (check before syntax)
    if re.search(r'permission denied|access denied|unauthorized', error_lower):
        return 'permission_denied: User lacks required permissions'
    
    # Connection/refused errors specific to Docker daemon
    if re.search(r'connection refused.*docker|cannot connect.*docker', error_lower):
        return 'daemon_not_running: Docker daemon not running'
    
    # Network issues
    if re.search(r'connection refused|cannot connect|connection failed|failed to connect|unable to connect', error_lower):
        return 'network_error: Cannot connect to remote host'
    if re.search(r'hostname|servname|network.*unreachable', error_lower):
        return 'network_error: Cannot connect to remote host'
    
    # Package/dependency issues
    if re.search(r'module.*not.*found|no.*such.*module|modulenotfounderror', error_lower):
        return 'dependency_missing: Required package not available'
    if re.search(r'package not found|package.*could.*not.*be.*found', error_lower):
        return 'dependency_missing: Required package not available'
    
    # Configuration issues
    if re.search(r'configuration.*not.*found|config.*file', error_lower):
        return 'configuration: Configuration or file not found'
    
    # File/directory not found (check last - most generic)
    if re.search(r'no such file or directory|file not found', error_lower):
        return 'file_not_found: File or directory does not exist'
    
    # Syntax/command error (check last - most generic)
    if re.search(r'invalid option|unrecognized command|command not found|illegal option|unknown option|usage:|is not a', error_lower):
        return 'command_syntax: Invalid command syntax or options'
    
    return 'other: General error'

def ask_openai_for_fix(error, cmd, previous_error=None, previous_fix=None):
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    
    platform_info = get_platform_info()
    app_info = get_app_info(cmd)
    error_type = categorize_error_type(error, cmd)
    
    # Gather file system context
    file_system_context = get_file_system_context(cmd)
    
    system_prompt = """You are a helpful CLI assistant. Fix shell commands based on errors.

IMPORTANT CONTEXT RULES:
1. ALWAYS read the provided: Platform, Application, Error type, and File system context
2. ALWAYS suggest PLATFORM-APPROPRIATE fixes:
   - macOS: Use open-a, launchctl, brew for packages
   - Linux: Use systemctl, service, apt, yum, dnf for services
   - DO NOT suggest macOS fixes for Linux or vice versa
3. Application-specific commands:
   - Docker: macOS uses open-a Docker Desktop app, Linux uses systemctl start docker
   - Git: Platform-agnostic (works everywhere)
   - Package managers: Use platform-appropriate tools
   4. If retrying a previously failed suggestion, CLEARLY state it did NOT work
5. CRITICAL: Use the file system context to understand:
   - Where the user currently is (current working directory)
   - What directories/files actually exist
   - What is available in the current and target directories
   - For path-related errors (cd, ls, file access), check if the path exists and suggest:
     * Correct path if directory exists
     * Suggest creating directory if it doesn't exist make sense
     * Suggest using current directory or parent directory if target doesn't exist

Return ONLY the fixed command, confidence percentage (1-100), reason, and explanation in this exact format: command:::confidence:::reason:::explanation.

IMPORTANT: Explanation should be 4-5 simple sentences in plain English explaining what the error is and its impact.

IMPORTANT: Use ::: as separators because shell commands may contain pipe characters |. Do not include any labels like FIXED_COMMAND:.
Example: git push:::95:::typo fix:::You typed git push incorrectly, which caused this error. The command failed because a typo prevented it from running properly. This means your changes were not uploaded to the remote repository. You need to fix the command to successfully push your code."""

    if previous_error and previous_fix and error == previous_error:
        # RETRY case: previous suggestion failed with same error
        context_parts = [
            f"PREVIOUS SUGGESTION THAT FAILED: {previous_fix}\n",
            f"This fix DID NOT WORK and produced the SAME ERROR.\n",
            f"Command attempted: {cmd}\n",
            f"Platform: {platform_info}\n",
        ]
        if app_info:
            context_parts.append(f"Application: {app_info}\n")
        if error_type != 'other':
            context_parts.append(f"Error type: {error_type}\n")
        
        # Platform-specific guidance
        context_parts.append("CRITICAL INSTRUCTION: You suggested a tool/command that does not exist on this platform.\n")
        context_parts.append(f"Platform is {platform_info}. See the error message above.\n")
        context_parts.append("REQUIRE: Suggest a DIFFERENT approach using platform-appropriate tools.\n")
        context_parts.append(f"Do NOT suggest {previous_fix} or similar Linux/Unix commands.\n")
        context_parts.append("Platform-specific guidance:\n")
        if 'macOS' in platform_info:
            context_parts.append("  - macOS: Use open-a to open apps, brew for packages, launchctl for services\n")
        elif 'Linux' in platform_info:
            context_parts.append("  - Linux: Use systemctl, apt, yum, dnf for services and packages\n")
        
        context_parts.append(f"Error message: {error}\n")
        context_parts.append("Please suggest a DIFFERENT, platform-appropriate solution.\n")
        context_parts.append(f"\n--- FILE SYSTEM CONTEXT ---\n{file_system_context}\n")
        user_msg = "".join(context_parts)
    else:
        # FIRST attempt: no previous suggestions
        context_parts = [
            f"Command that failed: {cmd}\n",
            f"Platform: {platform_info}\n",
            f"Error: {error}\n",
        ]
        if app_info:
            context_parts.append(f"Application: {app_info}\n")
        if error_type != 'other':
            context_parts.append(f"Error type: {error_type}\n")
            context_parts.append("Suggested approach: Focus on error type related issues.\n")
        context_parts.append(f"\n--- FILE SYSTEM CONTEXT ---\n{file_system_context}\n")
        user_msg = "".join(context_parts)
    
    global stop_cursor
    stop_cursor = False
    cursor_thread = threading.Thread(target=show_blinking_cursor)
    cursor_thread.start()
    
    response = None
    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_msg}
            ],
            temperature=0.3
        )
    except AuthenticationError:
        stop_cursor = True
        cursor_thread.join()
        print('\r[*] Analyzing error       ', end='', flush=True)
        print('\n[!] Error: Invalid OpenAI API key.')
        print('[!] Please check your API key and try again.')
        print('[!] Set it with: export OPENAI_API_KEY="your-key-here"')
        print('[!] Get a new key at: https://platform.openai.com/api-keys')
        sys.exit(1)
    except RateLimitError:
        stop_cursor = True
        cursor_thread.join()
        print('\r[*] Analyzing error       ', end='', flush=True)
        print('\n[!] Error: OpenAI API rate limit exceeded.')
        print('[!] You have reached your request limit or exceeded your quota.')
        print('[!] Please check your usage at: https://platform.openai.com/usage')
        print('[!] Ensure you have sufficient credits on your OpenAI account.')
        sys.exit(1)
    except APITimeoutError:
        stop_cursor = True
        cursor_thread.join()
        print('\r[*] Analyzing error       ', end='', flush=True)
        print('\n[!] Error: OpenAI API request timed out.')
        print('[!] Please check your internet connection and try again.')
        sys.exit(1)
    except APIConnectionError as e:
        stop_cursor = True
        cursor_thread.join()
        print('\r[*] Analyzing error       ', end='', flush=True)
        print(f'\n[!] Error: Could not connect to OpenAI servers.')
        print(f'[!] Details: {str(e)}')
        print('[!] Please check your internet connection and try again.')
        sys.exit(1)
    except APIError as e:
        stop_cursor = True
        cursor_thread.join()
        print('\r[*] Analyzing error       ', end='', flush=True)
        print(f'\n[!] Error: OpenAI API error occurred.')
        print(f'[!] Details: {str(e)}')
        print('[!] This might be an issue with OpenAI services. Please try again later.')
        sys.exit(1)
    except Exception as e:
        stop_cursor = True
        cursor_thread.join()
        print('\r[*] Analyzing error       ', end='', flush=True)
        print(f'\n[!] Unexpected error: {str(e)}')
        print('[!] Please try again or check your setup.')
        sys.exit(1)
    finally:
        if not stop_cursor:
            stop_cursor = True
            cursor_thread.join()
            print('\r[*] Analyzing error       ', end='', flush=True)
            print('\n[+] Done')
    
    content = response.choices[0].message.content
    fix = content.strip() if content else ''
    confidence = 50
    reason = ''
    explanation = ''
    
    if not fix or not fix.strip():
        return '', '50', '', ''
    
    # Parse "command:::confidence:::reason:::explanation" format - supports pipes
    
    if ':::' in fix and fix.count(':::') >= 3:
        # New 4-field format: command:::confidence:::reason:::explanation
        parts = fix.rsplit(':::', 3)
        command_part = parts[0].strip()
        confidence_part = parts[1].strip()
        reason = parts[2].strip() if len(parts) > 2 else ''
        explanation = parts[3].strip() if len(parts) > 3 else ''
        
        for prefix in ['FIXED_COMMAND:', 'Command:', 'Fix:', 'command:']:
            if command_part.startswith(prefix):
                command_part = command_part[len(prefix):].strip()
        fix = command_part
        
        if confidence_part:
            confidence_part = confidence_part.rstrip('%').strip()
            if confidence_part.isdigit():
                confidence = int(confidence_part)
            else:
                conf_lower = confidence_part.lower()
                if 'high' in conf_lower or 'very' in conf_lower:
                    confidence = 90
                elif 'medium' in conf_lower or 'moderate' in conf_lower:
                    confidence = 70
                elif 'low' in conf_lower:
                    confidence = 50
                else:
                    confidence = 50
    elif ':::' in fix and fix.count(':::') >= 2:
        # Old 3-field format for backward compatibility: command:::confidence:::reason
        parts = fix.rsplit(':::', 2)
        command_part = parts[0].strip()
        confidence_part = parts[1].strip()
        reason = parts[2].strip() if len(parts) > 2 else ''
        
        for prefix in ['FIXED_COMMAND:', 'Command:', 'Fix:', 'command:']:
            if command_part.startswith(prefix):
                command_part = command_part[len(prefix):].strip()
        fix = command_part
        
        if confidence_part:
            confidence_part = confidence_part.rstrip('%').strip()
            if confidence_part.isdigit():
                confidence = int(confidence_part)
            else:
                conf_lower = confidence_part.lower()
                if 'high' in conf_lower or 'very' in conf_lower:
                    confidence = 90
                elif 'medium' in conf_lower or 'moderate' in conf_lower:
                    confidence = 70
                elif 'low' in conf_lower:
                    confidence = 50
                else:
                    confidence = 50
    elif ':::' in fix and fix.count(':::') >= 1:
        # Backward compatibility for old format
        parts = fix.rsplit(':::', 1)
        command_part = parts[0].strip()
        confidence_part = parts[-1].strip()
        
        # Clean up command_part
        for prefix in ['FIXED_COMMAND:', 'Command:', 'Fix:', 'command:']:
            if command_part.startswith(prefix):
                command_part = command_part[len(prefix):].strip()
        fix = command_part
        
        if confidence_part:
            confidence_part = confidence_part.rstrip('%').strip()
            if confidence_part.isdigit():
                confidence = int(confidence_part)
            else:
                conf_lower = confidence_part.lower()
                if 'high' in conf_lower or 'very' in conf_lower:
                    confidence = 90
                elif 'medium' in conf_lower or 'moderate' in conf_lower:
                    confidence = 70
                elif 'low' in conf_lower:
                    confidence = 50
                else:
                    confidence = 50
    
    return fix, str(confidence), reason, explanation

def interactive_menu():
    options = ['Apply suggested fix', 'Retry (get alternative suggestion)', 'Enter custom command', 'Explain the error', 'Exit']
    
    while True:
        print('\nWhat do you want to do?')
        for i, option in enumerate(options):
            print(f'  [{i+1}] {option}')
        
        try:
            choice = input('[?] Select option (1-5): ').strip()
            if choice.isdigit() and 1 <= int(choice) <= 5:
                return int(choice) - 1
            print('[!] Invalid selection. Please try again.')
        except (KeyboardInterrupt, EOFError):
            print('\n[!] Exiting.')
            sys.exit(0)

def show_logo():
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

def main():
    show_logo()
    
    api_key = get_api_key()
    if not api_key:
        print('[!] OpenAI API key required')
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print('[!] Usage: python patch.py <command>')
        sys.exit(1)
    
    original_cmd = ' '.join(sys.argv[1:])
    cmd = original_cmd
    max_attempts = 5
    max_retries = 3
    attempt = 0
    retry_count = 0
    previous_error = None
    previous_fix = None
    
    while attempt < max_attempts:
        attempt += 1
        returncode, output, is_interactive = execute_command(cmd, check_for_sudo=True)
        
        # If user aborted early (returncode is None or output is None), exit
        if returncode is None or output is None:
            print('[!] Command aborted by user.')
            return
        
        if returncode == 0:
            print('[+] Success!')
            if output:
                print(output)
            return
        
        # For interactive commands, we can't analyze the output safely
        if is_interactive:
            print('[!] Interactive command failed or was interrupted.')
            print('[!] Cannot automatically fix interactive commands.')
            response = input('[!] Try a non-interactive alternative? (y/n): ')
            if response.lower() == 'y':
                alternatives = get_non_interactive_alternative(cmd)
                if alternatives:
                    print('\n[+] Available alternatives:')
                    for i, alt in enumerate(alternatives, 1):
                        print(f'  [{i}] {alt}')
                    choice = input('[?] Select alternative (or Enter custom): ')
                    if choice.isdigit() and 1 <= int(choice) <= len(alternatives):
                        cmd = alternatives[int(choice) - 1]
                        continue
                    else:
                        cmd = choice
                        continue
            print('[!] Exiting.')
            return
        
        print(f'\n[-] Error (attempt {attempt}/{max_attempts}):')
        print(output)
        
        if attempt >= max_attempts:
            print('[!] Max attempts reached.')
            return
        
        fix, confidence, reason, explanation = ask_openai_for_fix(output, cmd, previous_error, previous_fix)
        print(f'\n[*] Suggested fix: {fix}')
        print(f'[*] Confidence: {confidence}%')
        
        if int(confidence) >= 85:
            print('[*] Confidence: [High]')
        elif int(confidence) >= 60:
            print('[*] Confidence: [Medium]')
        else:
            print('[*] Confidence: [Low - Uncertain]')
            if reason:
                print(f'[!] Warning: Low confidence fix because {reason}. Consider manual review.')
            else:
                print('[!] Warning: Low confidence fix. Consider manual review.')
        
        choice = interactive_menu()
        
        if choice == 4:
            print('[!] Exiting.')
            return
        
        if choice == 3:
            print('\n[*] Error Explanation:')
            print('────────────────────────')
            print(explanation if explanation else 'No explanation available.')
            print('────────────────────────')
            input('\n[Press Enter to continue...] ')
            continue
        
        if choice == 2:
            cmd = input('[->] Enter new command: ')
            previous_error = None
            previous_fix = None
            print('\n[*] Trying new command...')
            continue
        
        # choice == 0: Apply suggested fix
        previous_error = output
        previous_fix = fix
        cmd = fix
        
        # Show command preview
        print('\nAbout to run:')
        print('──────────────')
        print(f'{fix}')
        print('──────────────')
        
        response = input('Proceed? (y/n): ')
        if response.lower() != 'y':
            print('[!] Aborted.')
            return
        
        print('\n[*] Applying fix...')
    
    print('[!] Could not fix the command.')

if __name__ == '__main__':
    main()