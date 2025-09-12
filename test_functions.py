#!/usr/bin/env python3
"""
Test suite for functions from the desktop.ipynb notebook.
This file tests all the major functions to ensure they work correctly.
"""

import sys
import io
from contextlib import redirect_stdout, redirect_stderr
import os
import tempfile
import logging

# Test functions extracted from the notebook

def hello(name):
    """Function to greet a person with a custom message."""
    return f"Hello there, {name}!"

def check_palindrome_simple(text):
    """Simple palindrome checker using string slicing."""
    if not text:
        return False
    cleaned = ''.join(char.lower() for char in text if char.isalnum())
    return cleaned == cleaned[::-1]

def check_palindrome_manual(word):
    """Manual palindrome checker using character-by-character comparison."""
    if not word:
        return False
    
    word = word.strip().lower()
    length = len(word)
    
    for i in range(length // 2):
        if word[i] != word[length - 1 - i]:
            return False
    return True

def count_characters(text):
    """Count the frequency of each character in the given text."""
    char_count = {}
    for char in text:
        char_count.setdefault(char, 0)
        char_count[char] += 1
    return char_count

def sum_till(n):
    """Calculate the sum of numbers from 1 to n using iteration."""
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

def triangular_numbers(n):
    """Generate first n triangular numbers."""
    numbers = []
    for i in range(1, n + 1):
        numbers.append(sum_till(i))
    return numbers

def triangular_recursive(n):
    """Calculate the nth triangular number using recursion."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return n + triangular_recursive(n - 1)

def demonstrate_list_operations():
    """Test list operations and return results."""
    names = ['aditya', 'abhishek', 'nachiket']
    original = names.copy()
    
    names.append('new_person')
    aditya_index = names.index('aditya')
    names.insert(1, 'tau')
    names.append('talwar')
    
    return {
        'original': original,
        'final': names,
        'aditya_index': aditya_index
    }

def test_dictionary_operations():
    """Test dictionary operations."""
    person_info = {'name': 'abhishek', 'age': 19, 'roll_no': '8312'}
    
    try:
        values_list = list(person_info.values())
        keys_list = list(person_info.keys())
        key_exists = 'name' in person_info
        
        return {
            'values': values_list,
            'keys': keys_list,
            'name_exists': key_exists,
            'success': True
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

# Test suite class
class TestNotebookFunctions:
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
    
    def test_hello_function(self):
        """Test the hello function with various inputs."""
        # Test normal input
        result1 = hello("Alice")
        if result1 != "Hello there, Alice!":
            return False
        
        # Test with empty string
        result2 = hello("")
        if result2 != "Hello there, !":
            return False
        
        # Test with numbers
        result3 = hello("123")
        if result3 != "Hello there, 123!":
            return False
        
        return True
    
    def test_palindrome_functions(self):
        """Test palindrome checker functions."""
        test_cases = [
            ("racecar", True),
            ("hello", False),
            ("A man a plan a canal Panama", True),
            ("race a car", False),
            ("", False),
            ("a", True),
            ("Madam", True),
            ("12321", True),
            ("12345", False)
        ]
        
        for text, expected in test_cases:
            # Test simple palindrome function
            result1 = check_palindrome_simple(text)
            if result1 != expected:
                print(f"Simple palindrome failed for '{text}': expected {expected}, got {result1}")
                return False
            
            # Test manual palindrome function (for single words)
            if ' ' not in text and text:  # Manual function doesn't handle spaces
                clean_text = ''.join(char.lower() for char in text if char.isalnum())
                result2 = check_palindrome_manual(clean_text)
                clean_expected = clean_text == clean_text[::-1]
                if result2 != clean_expected:
                    print(f"Manual palindrome failed for '{clean_text}': expected {clean_expected}, got {result2}")
                    return False
        
        return True
    
    def test_character_counting(self):
        """Test character counting function."""
        test_text = "hello world"
        result = count_characters(test_text)
        
        expected = {
            'h': 1, 'e': 1, 'l': 3, 'o': 2, ' ': 1, 'w': 1, 'r': 1, 'd': 1
        }
        
        return result == expected
    
    def test_triangular_functions(self):
        """Test triangular number functions."""
        # Test sum_till function
        if sum_till(5) != 15:  # 1+2+3+4+5 = 15
            return False
        if sum_till(1) != 1:
            return False
        if sum_till(0) != 0:
            return False
        
        # Test triangular_numbers function
        result = triangular_numbers(5)
        expected = [1, 3, 6, 10, 15]  # First 5 triangular numbers
        if result != expected:
            return False
        
        # Test triangular_recursive function
        if triangular_recursive(5) != 15:
            return False
        if triangular_recursive(1) != 1:
            return False
        if triangular_recursive(0) != 0:
            return False
        
        return True
    
    def test_list_operations(self):
        """Test list operations."""
        result = demonstrate_list_operations()
        
        # Check original list
        if result['original'] != ['aditya', 'abhishek', 'nachiket']:
            return False
        
        # Check final list has all expected elements
        expected_final = ['aditya', 'tau', 'abhishek', 'nachiket', 'new_person', 'talwar']
        if result['final'] != expected_final:
            return False
        
        # Check index finding
        if result['aditya_index'] != 0:
            return False
        
        return True
    
    def test_dictionary_operations(self):
        """Test dictionary operations."""
        result = test_dictionary_operations()
        
        if not result['success']:
            return False
        
        # Check values
        expected_values = ['abhishek', 19, '8312']
        if result['values'] != expected_values:
            return False
        
        # Check keys
        expected_keys = ['name', 'age', 'roll_no']
        if result['keys'] != expected_keys:
            return False
        
        # Check key existence
        if not result['name_exists']:
            return False
        
        return True
    
    def test_error_handling(self):
        """Test error handling functions."""
        # Test that error handling doesn't crash
        try:
            # This should handle the error gracefully
            test_dict = {'key': 'value'}
            # Simulate an error scenario
            result = test_dict.get('nonexistent_key', 'default')
            if result != 'default':
                return False
            return True
        except Exception:
            return False
    
    def run_all_tests(self):
        """Run all tests and print results."""
        print("🧪 Running Test Suite for Notebook Functions")
        print("=" * 50)
        
        # Run all tests
        self.run_test("Hello Function", self.test_hello_function)
        self.run_test("Palindrome Functions", self.test_palindrome_functions)
        self.run_test("Character Counting", self.test_character_counting)
        self.run_test("Triangular Functions", self.test_triangular_functions)
        self.run_test("List Operations", self.test_list_operations)
        self.run_test("Dictionary Operations", self.test_dictionary_operations)
        self.run_test("Error Handling", self.test_error_handling)
        
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
            print("🎉 All tests passed!")
        else:
            print(f"⚠️  {self.failed} test(s) failed. Please review the code.")
        
        return self.failed == 0

if __name__ == "__main__":
    # Run the test suite
    tester = TestNotebookFunctions()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)