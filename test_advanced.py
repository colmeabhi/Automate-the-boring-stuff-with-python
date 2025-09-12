#!/usr/bin/env python3
"""
Test suite for advanced operations including regex, os operations, and logging.
"""

import re
import os
import tempfile
import logging
import sys
from io import StringIO
from contextlib import redirect_stderr

def test_regex_operations():
    """Test regular expression operations from the notebook."""
    # Test phone number regex
    regex_object = re.compile(r"\d\d-\d\d\d\d\d\d\d\d\d\d")
    text = "my phone number is +91-8928335999 and my phone no. is not +91-7774815152"
    matches = regex_object.findall(text)
    expected = ['91-8928335999', '91-7774815152']
    
    if matches != expected:
        print(f"Phone regex failed: expected {expected}, got {matches}")
        return False
    
    # Test grouped regex
    regex_obj = re.compile(r"(\(\d\d\))-(\(\d\d\d\d\d\d\d\d\d\d\))")
    text2 = "my phone number is +(91)-(8928335999) and my phone no. is not +91-7774815152"
    match = regex_obj.search(text2)
    
    if not match:
        print("Grouped regex failed: no match found")
        return False
    
    groups = match.group(1, 2)
    expected_groups = ('(91)', '(8928335999)')
    if groups != expected_groups:
        print(f"Grouped regex failed: expected {expected_groups}, got {groups}")
        return False
    
    # Test alternation regex
    regex_obj3 = re.compile(r"Bat(mobile|rat|man|agator)")
    text3 = "Sasha where is my Batmobile as well as my Batagator"
    match3 = regex_obj3.search(text3)
    
    if not match3 or match3.group() != "Batmobile":
        print(f"Alternation regex failed: expected 'Batmobile', got {match3.group() if match3 else None}")
        return False
    
    return True

def test_os_operations():
    """Test OS module operations."""
    # Test path joining
    joined_path = os.path.join("folder1", "folder2", "app.js")
    # The exact format depends on the OS, but it should contain all parts
    if "folder1" not in joined_path or "folder2" not in joined_path or "app.js" not in joined_path:
        return False
    
    # Test path separator
    sep = os.sep
    if not isinstance(sep, str) or len(sep) == 0:
        return False
    
    # Test current working directory
    cwd = os.getcwd()
    if not isinstance(cwd, str) or len(cwd) == 0:
        return False
    
    # Test absolute path
    abs_path = os.path.abspath('test_file.txt')
    if not os.path.isabs(abs_path):
        return False
    
    # Test path components
    dirname = os.path.dirname('/folder1/folder2/app.js')
    if dirname not in ['/folder1/folder2', '\\folder1\\folder2']:  # Handle different OS
        # More flexible check
        if 'folder1' not in dirname or 'folder2' not in dirname:
            return False
    
    basename = os.path.basename('app.js')
    if basename != 'app.js':
        return False
    
    return True

def test_file_size_operations():
    """Test file size operations using temporary files."""
    try:
        # Create a temporary file with known content
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_filename = temp_file.name
            test_content = "This is test content for size calculation."
            temp_file.write(test_content)
        
        # Test file size calculation
        file_size = os.path.getsize(temp_filename)
        expected_size = len(test_content.encode('utf-8'))  # Size in bytes
        
        # Clean up
        os.unlink(temp_filename)
        
        # File size should match content size
        return file_size == expected_size
    
    except Exception as e:
        print(f"File size test failed: {e}")
        return False

def test_string_case_operations():
    """Test string case operations."""
    text = 'abhishek'
    
    # Test membership
    if 'abhi' not in text:
        return False
    
    # Test upper case
    if text.upper() != 'ABHISHEK':
        return False
    
    # Test character type checking
    if not text.isalpha():
        return False
    
    if not text.isalnum():
        return False
    
    # Test string checking functions
    text2 = 'hello world'
    if not text2.startswith('hello'):
        return False
    
    if not text2.endswith('world'):
        return False
    
    return True

def test_logging_functionality():
    """Test logging functionality with temporary log file."""
    try:
        # Create a temporary log file
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.log') as temp_log:
            temp_log_name = temp_log.name
        
        # Configure logging to use the temporary file
        logging.basicConfig(
            filename=temp_log_name,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            force=True  # Override any existing configuration
        )
        
        # Write test log messages
        logging.debug("Test debug message")
        logging.info("Test info message")
        logging.warning("Test warning message")
        logging.error("Test error message")
        logging.critical("Test critical message")
        
        # Force flush
        logging.shutdown()
        
        # Read the log file
        with open(temp_log_name, 'r') as log_file:
            log_content = log_file.read()
        
        # Clean up
        os.unlink(temp_log_name)
        
        # Check that all log levels were written
        required_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        for level in required_levels:
            if level not in log_content:
                print(f"Logging test failed: {level} not found in log")
                return False
        
        return True
    
    except Exception as e:
        print(f"Logging test failed: {e}")
        return False

def test_error_handling():
    """Test error handling scenarios."""
    try:
        # Test try-except with specific exception
        try:
            raise ValueError("Test error")
        except ValueError as e:
            if str(e) != "Test error":
                return False
        
        # Test try-except with generic exception
        try:
            result = 1 / 0
        except ZeroDivisionError:
            pass  # Expected
        else:
            return False  # Should have raised exception
        
        # Test assert statement
        try:
            assert 1 == 2, "This should fail"
        except AssertionError:
            pass  # Expected
        else:
            return False  # Should have raised exception
        
        return True
    
    except Exception as e:
        print(f"Error handling test failed: {e}")
        return False

class TestAdvancedOperations:
    def __init__(self):
        self.test_results = []
        self.passed = 0
        self.failed = 0
    
    def run_test(self, test_name, test_func):
        """Run a single test and record the result."""
        try:
            result = test_func()
            if result:
                self.test_results.append(f"✅ {test_name}: PASSED")
                self.passed += 1
            else:
                self.test_results.append(f"❌ {test_name}: FAILED")
                self.failed += 1
        except Exception as e:
            self.test_results.append(f"❌ {test_name}: ERROR - {str(e)}")
            self.failed += 1
    
    def run_all_tests(self):
        """Run all advanced operation tests."""
        print("🔬 Running Advanced Operations Test Suite")
        print("=" * 50)
        
        # Run all tests
        self.run_test("Regex Operations", test_regex_operations)
        self.run_test("OS Operations", test_os_operations)
        self.run_test("File Size Operations", test_file_size_operations)
        self.run_test("String Case Operations", test_string_case_operations)
        self.run_test("Logging Functionality", test_logging_functionality)
        self.run_test("Error Handling", test_error_handling)
        
        # Print results
        print("\n📊 Test Results:")
        print("-" * 30)
        for result in self.test_results:
            print(result)
        
        print(f"\n📈 Summary:")
        print(f"Tests Passed: {self.passed}")
        print(f"Tests Failed: {self.failed}")
        print(f"Total Tests: {self.passed + self.failed}")
        
        if self.failed == 0:
            print("🎉 All advanced operation tests passed!")
        else:
            print(f"⚠️  {self.failed} test(s) failed. Please review the code.")
        
        return self.failed == 0

if __name__ == "__main__":
    tester = TestAdvancedOperations()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)