#!/usr/bin/env python3
"""
Test suite for interactive functions from the notebook.
This tests functions that typically require user input by simulating input.
"""

import io
import sys
import random
import tempfile
import os
from unittest.mock import patch, mock_open

def number_guessing_game_logic(name, target_number, guesses):
    """
    Simulate the guessing game logic without input() calls.
    
    Args:
        name (str): Player name
        target_number (int): The number to guess
        guesses (list): List of guesses to make
    
    Returns:
        dict: Game results
    """
    max_attempts = 5
    
    for attempt, user_guess in enumerate(guesses[:max_attempts], 1):
        if not (1 <= user_guess <= 10):
            continue
            
        if user_guess == target_number:
            return {
                'success': True,
                'attempts': attempt,
                'message': f'Yes! You guessed correctly! It took you {attempt} attempt(s)'
            }
        elif user_guess < target_number:
            continue  # Would print "Enter a higher number"
        else:
            continue  # Would print "Enter a lower number"
    
    return {
        'success': False,
        'attempts': max_attempts,
        'message': f'Sorry {name}, you didn\'t guess the number {target_number} in {max_attempts} attempts.'
    }

def test_file_operations():
    """Test file operations using temporary files."""
    try:
        # Test file writing and reading
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_filename = temp_file.name
            temp_file.write("Test content for file operations")
        
        # Read the file back
        with open(temp_filename, 'r') as temp_file:
            content = temp_file.read()
        
        # Clean up
        os.unlink(temp_filename)
        
        return content == "Test content for file operations"
    
    except Exception as e:
        print(f"File operations test failed: {e}")
        return False

def test_string_operations():
    """Test various string operations from the notebook."""
    # Test string slicing
    str1 = 'name is abhishek'
    str2 = str1[0:3] + 'ely' + str1[4:12]
    expected = 'namely is abhi'
    
    if str2 != expected:
        return False
    
    # Test string methods
    text1 = 'hello world'
    if not text1.startswith('hello'):
        return False
    if not text1.endswith('world'):
        return False
    
    # Test string to list conversion
    string1 = "My name is abhishek ahirrao"
    words = string1.split()
    expected_words = ['My', 'name', 'is', 'abhishek', 'ahirrao']
    
    if words != expected_words:
        return False
    
    # Test join operation
    word_list = ["mumbai", "is", "in", "maharashtra"]
    joined = ','.join(word_list)
    expected_joined = "mumbai,is,in,maharashtra"
    
    if joined != expected_joined:
        return False
    
    return True

def test_list_copying():
    """Test list copying behavior (reference vs deep copy)."""
    # Test reference copying (should change both lists)
    list1 = [1, 2, 3, 4, 5, 6]
    list2 = list1  # Reference copy
    list2.append(70)
    
    if list1[-1] != 70:  # list1 should also be modified
        return False
    
    # Test proper copying using copy method
    list3 = list1.copy()  # Proper copy
    original_length = len(list1)
    list3.append(77)
    
    if len(list1) != original_length:  # list1 should not be modified
        return False
    
    if list3[-1] != 77:  # list3 should have the new element
        return False
    
    return True

def test_enumeration():
    """Test enumerate vs range(len()) approaches."""
    my_list = ['1', '2', '3']
    
    # Test range(len()) approach
    results1 = []
    for i in range(len(my_list)):
        results1.append((i, my_list[i]))
    
    # Test enumerate approach
    results2 = []
    for index, value in enumerate(my_list):
        results2.append((index, value))
    
    expected = [(0, '1'), (1, '2'), (2, '3')]
    
    return results1 == expected and results2 == expected

def test_dictionary_methods():
    """Test dictionary get method and error handling."""
    dic = {'class': 8, 'rank': 1, 'bhailog': 'yes'}
    
    # Test get method with existing key
    if dic.get('class', 'nahimila') != 8:
        return False
    
    # Test get method with non-existing key
    if dic.get('rude', 'nahimila') != 'nahimila':
        return False
    
    return True

def test_step_iteration():
    """Test for loop with step iteration."""
    count = 0
    expected_values = []
    
    for i in range(0, 10, 2):
        count += 1
        expected_values.append(count)
    
    # Should iterate through 0, 2, 4, 6, 8 (5 times)
    expected = [1, 2, 3, 4, 5]
    
    return expected_values == expected and count == 5

class TestInteractiveFunctions:
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
    
    def test_guessing_game_logic(self):
        """Test the number guessing game logic."""
        # Test successful guess
        result1 = number_guessing_game_logic("Alice", 5, [3, 5])
        if not result1['success'] or result1['attempts'] != 2:
            return False
        
        # Test failed guess (all wrong)
        result2 = number_guessing_game_logic("Bob", 5, [1, 2, 3, 4, 6])
        if result2['success']:
            return False
        
        # Test successful guess on last attempt
        result3 = number_guessing_game_logic("Carol", 7, [1, 2, 3, 4, 7])
        if not result3['success'] or result3['attempts'] != 5:
            return False
        
        return True
    
    def test_input_validation(self):
        """Test input validation scenarios."""
        # Test empty string handling
        empty_input = ""
        if empty_input.strip():  # Should be falsy after strip
            return False
        
        # Test number validation
        try:
            invalid_number = "abc"
            int(invalid_number)
            return False  # Should have raised ValueError
        except ValueError:
            pass  # Expected behavior
        
        # Test range validation
        test_number = 15
        if 1 <= test_number <= 10:  # Should be False
            return False
        
        return True
    
    def run_all_tests(self):
        """Run all interactive tests."""
        print("🎮 Running Interactive Functions Test Suite")
        print("=" * 50)
        
        # Run all tests
        self.run_test("Guessing Game Logic", self.test_guessing_game_logic)
        self.run_test("Input Validation", self.test_input_validation)
        self.run_test("File Operations", lambda: test_file_operations())
        self.run_test("String Operations", lambda: test_string_operations())
        self.run_test("List Copying", lambda: test_list_copying())
        self.run_test("Enumeration Methods", lambda: test_enumeration())
        self.run_test("Dictionary Methods", lambda: test_dictionary_methods())
        self.run_test("Step Iteration", lambda: test_step_iteration())
        
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
            print("🎉 All interactive tests passed!")
        else:
            print(f"⚠️  {self.failed} test(s) failed. Please review the code.")
        
        return self.failed == 0

if __name__ == "__main__":
    tester = TestInteractiveFunctions()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)