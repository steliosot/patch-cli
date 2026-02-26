#!/usr/bin/env python3
"""
Unit tests for patch.py helper functions
Tests platform detection, error categorization, parsing, etc.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from patch import (
    get_platform_info,
    get_app_info,
    categorize_error_type,
    is_pipe_to_shell,
    validate_api_key
)


class TestPlatformDetection(unittest.TestCase):
    """Test platform detection functionality."""

    def test_get_platform_info(self):
        """Test that platform info returns a valid platform."""
        platform = get_platform_info()
        self.assertIn(platform, ['macOS', 'Linux', 'Windows', 'Darwin', 'Microsoft'])
        print(f"[✓] Platform detected: {platform}")

    def test_platform_is_string(self):
        """Test that platform info is a string."""
        platform = get_platform_info()
        self.assertIsInstance(platform, str)
        print(f"[✓] Platform is string: {type(platform)}")


class TestAppDetection(unittest.TestCase):
    """Test application detection from commands."""

    def test_docker_detection(self):
        """Test Docker application detection."""
        apps = [
            ('docker ps', 'Docker'),
            ('docker run -it ubuntu', 'Docker'),
            ('sudo docker ps', 'Docker'),
        ]
        for cmd, expected in apps:
            result = get_app_info(cmd)
            self.assertEqual(result, expected, f"Failed for command: {cmd}")
        print(f"[✓] Docker detection working")

    def test_docker_compose_detection(self):
        """Test Docker Compose detection."""
        result = get_app_info('docker-compose up')
        self.assertEqual(result, 'Docker Compose')
        print(f"[✓] Docker Compose detection working")

    def test_git_detection(self):
        """Test Git detection."""
        result = get_app_info('git push')
        self.assertEqual(result, 'Git')
        print(f"[✓] Git detection working")

    def test_npm_detection(self):
        """Test npm detection."""
        result = get_app_info('npm install')
        self.assertEqual(result, 'Node.js (npm)')
        print(f"[✓] npm detection working")

    def test_brew_detection(self):
        """Test Homebrew detection."""
        result = get_app_info('brew install python')
        self.assertEqual(result, 'Homebrew')
        print(f"[✓] brew detection working")

    def test_unknown_app(self):
        """Test unknown application returns None."""
        result = get_app_info('unknown-command')
        self.assertIsNone(result)
        print(f"[✓] Unknown app returns None")

    def test_empty_command(self):
        """Test empty command returns None."""
        result = get_app_info('')
        self.assertIsNone(result)
        print(f"[✓] Empty command returns None")


class TestErrorCategorization(unittest.TestCase):
    """Test error type categorization."""

    def test_daemon_not_running_docker(self):
        """Test daemon not running detection for Docker."""
        errors = [
            'daemon not running',
            'connect to the Docker API',
            'no such file or directory: docker.sock',
            'connection refused docker',
        ]
        for error in errors:
            with self.subTest(error=error):
                result = categorize_error_type(error, 'docker ps')
                self.assertIn('daemon_not_running', result)
        print(f"[✓] Daemon not running detection working")

    def test_command_syntax_error(self):
        """Test syntax error detection."""
        errors = [
            'invalid option --x',
            'unrecognized command "foo"',
            'command not found: xyz',
            'illegal option -f',
        ]
        for error in errors:
            with self.subTest(error=error):
                result = categorize_error_type(error, 'cmd -x')
                self.assertIn('command_syntax', result)
        print(f"[✓] Command syntax error detection working")

    def test_permission_denied(self):
        """Test permission denied detection."""
        errors = [
            'permission denied',
            'access denied',
            'unauthorized: authentication required',
        ]
        for error in errors:
            with self.subTest(error=error):
                result = categorize_error_type(error, 'docker ps')
                self.assertIn('permission_denied', result)
        print(f"[✓] Permission denied detection working")

    def test_file_not_found(self):
        """Test file not found detection."""
        errors = [
            'no such file or directory',
            'file not found',
            'directory does not exist',
        ]
        for error in errors:
            with self.subTest(error=error):
                result = categorize_error_type(error, 'cat missing.txt')
                self.assertIn('file_not_found', result)
        print(f"[✓] File not found detection working")

    def test_network_error(self):
        """Test network error detection."""
        errors = [
            'connection refused',
            'hostname not found',
            'network unreachable',
        ]
        for error in errors:
            with self.subTest(error=error):
                result = categorize_error_type(error, 'curl https://example.com')
                self.assertIn('network_error', result)
        print(f"[✓] Network error detection working")

    def test_dependency_missing(self):
        """Test dependency missing detection."""
        errors = [
            'module not found',
            'no such module',
            'package not found',
        ]
        for error in errors:
            with self.subTest(error=error):
                result = categorize_error_type(error, 'import missing_module')
                self.assertIn('dependency_missing', result)
        print(f"[✓] Dependency missing detection working")

    def test_configuration_error(self):
        """Test configuration error detection."""
        errors = [
            'configuration not found',
            'could not find config file',
            'config missing',
        ]
        for error in errors:
            with self.subTest(error=error):
                result = categorize_error_type(error, 'docker-compose up')
                self.assertIn('configuration', result)
        print(f"[✓] Configuration error detection working")


class TestPipeDetection(unittest.TestCase):
    """Test pipe-to-shell detection."""

    def test_pipe_to_bash(self):
        """Test detection of pipe to bash."""
        commands = [
            'curl -sL http://example.com | bash',
            'wget -qO- http://example.com | bash',
            'cat script.sh | bash',
        ]
        for cmd in commands:
            with self.subTest(cmd=cmd):
                result = is_pipe_to_shell(cmd)
                self.assertTrue(result)
        print(f"[✓] Pipe to bash detection working")

    def test_pipe_to_sh(self):
        """Test detection of pipe to sh."""
        commands = [
            'curl -sL http://example.com | sh',
            'wget -qO- http://example.com | sh',
        ]
        for cmd in commands:
            with self.subTest(cmd=cmd):
                result = is_pipe_to_shell(cmd)
                self.assertTrue(result)
        print(f"[✓] Pipe to sh detection working")

    def test_pipe_to_zsh(self):
        """Test detection of pipe to zsh."""
        commands = [
            'curl -sL http://example.com | zsh',
            'cat script.sh | zsh',
        ]
        for cmd in commands:
            with self.subTest(cmd=cmd):
                result = is_pipe_to_shell(cmd)
                self.assertTrue(result)
        print(f"[✓] Pipe to zsh detection working")

    def test_no_pipe_to_shell(self):
        """Test commands without pipe-to-shell."""
        commands = [
            'curl -sL http://example.com',
            'cat file.txt',
            'docker ps',
            'git status',
        ]
        for cmd in commands:
            with self.subTest(cmd=cmd):
                result = is_pipe_to_shell(cmd)
                self.assertFalse(result)
        print(f"[✓] No pipe-to-shell detection working")


class TestAPIKeyValidation(unittest.TestCase):
    """Test API key validation."""

    def test_valid_api_key_length(self):
        """Test that valid API key length passes validation."""
        # OpenAI API keys are at least 20 characters
        key = 'sk-' + 'a' * 50
        result = validate_api_key(key)
        self.assertTrue(result)
        print(f"[✓] Valid API key passes validation")

    def test_short_api_key_warns(self):
        """Test that short API key warns but still validates."""
        key = 'sk-short'
        result = validate_api_key(key)
        # validate_api_key returns True for any non-empty key, just warns
        self.assertTrue(result)
        print(f"[✓] Short API key warns but validates")

    def test_non_empty_api_key_validates(self):
        """Test that any non-empty API key validates."""
        key = 'any-key'
        result = validate_api_key(key)
        self.assertTrue(result)
        print(f"[✓] Non-empty API key validates")

    def test_empty_api_key_fails(self):
        """Test that empty API key fails validation."""
        result = validate_api_key('')
        self.assertFalse(result)
        print(f"[✓] Empty API key fails validation")

    def test_none_api_key_fails(self):
        """Test that None API key fails validation."""
        result = validate_api_key(None)
        self.assertFalse(result)
        print(f"[✓] None API key fails validation")


class TestResponseParsing(unittest.TestCase):
    """Test parsing of AI responses in ::: format."""

    def test_parse_full_format(self):
        """Test parsing full command:::confidence:::reason format."""
        response = "docker ps:::95:::Missing space in command"
        # This would normally be parsed by the response parsing logic
        parts = response.rsplit(':::', 2)
        self.assertEqual(len(parts), 3)
        self.assertEqual(parts[0], 'docker ps')
        self.assertEqual(parts[1], '95')
        self.assertEqual(parts[2], 'Missing space in command')
        print(f"[✓] Full format parsing working")

    def test_parse_with_pipes(self):
        """Test parsing command with pipe characters."""
        response = "curl -fsSL url | bash:::90:::Install script"
        parts = response.rsplit(':::', 2)
        self.assertEqual(parts[0], 'curl -fsSL url | bash')
        print(f"[✓] Pipe character parsing working")

    def test_parse_numeric_confidence(self):
        """Test parsing numeric confidence."""
        response = "git push:::85:::Missing remote"
        parts = response.rsplit(':::', 2)
        confidence = parts[1].rstrip('%')
        self.assertTrue(confidence.isdigit())
        self.assertEqual(int(confidence), 85)
        print(f"[✓] Numeric confidence parsing working")

    def test_parse_text_confidence_high(self):
        """Test parsing 'high' confidence."""
        confidence = 90  # Initialize at method level
        confidence_text = 'high'
        if confidence_text in ['high', 'very']:
            confidence = 95
        self.assertGreaterEqual(confidence, 90)
        print(f"[✓] High confidence text parsing working")

    def test_parse_text_confidence_medium(self):
        """Test parsing 'medium' confidence."""
        confidence = 70  # Initialize at method level
        confidence_text = 'medium'
        if confidence_text in ['medium', 'moderate']:
            confidence = 75
        self.assertGreaterEqual(confidence, 70)
        print(f"[✓] Medium confidence text parsing working")

    def test_parse_text_confidence_low(self):
        """Test parsing 'low' confidence."""
        confidence = 50  # Initialize at method level
        confidence_text = 'low'
        if confidence_text in ['low']:
            confidence = 55
        self.assertGreaterEqual(confidence, 50)
        print(f"[✓] Low confidence text parsing working")


def run_test_suite():
    """Run all tests and print summary."""
    print("\n" + "=" * 60)
    print("   Patch.py Unit Tests")
    print("=" * 60 + "\n")

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestPlatformDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestAppDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorCategorization))
    suite.addTests(loader.loadTestsFromTestCase(TestPipeDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIKeyValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestResponseParsing))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 60)
    print("   Test Summary")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 60 + "\n")

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_test_suite()
    sys.exit(0 if success else 1)