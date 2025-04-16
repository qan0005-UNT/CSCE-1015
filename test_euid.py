import unittest
import random
import string
from euid_validator import validate_length, validate_contents, validate

class TestEUIDValidation(unittest.TestCase):
    def test_validate_length(self):
        
        # Test normal boundaries (0 to 7).
        for length in range(8):
            input = "x" * length
            if length in (6, 7):
                self.assertTrue(validate_length(input), f"Length {length} should be valid")
            else:
                self.assertFalse(validate_length(input),f"Length {length} should be invalid")
        
        # Edge cases for empty and None.
        self.assertFalse(validate_length(""))        # Empty string
        self.assertFalse(validate_length(None))      # None input
        
        # Fuzz testing with random large lengths.
        for _ in range(10_000):  # Test 10,000 different random lengths.
            # Generate random lengths between 8 and 10 million.
            length = random.randint(8, 10_000_000)
            input = "x" * length
            self.assertFalse(validate_length(input), f"Length {length} should be invalid")
            
        # Test with various problematic inputs.
        problematic = [
            "\0" * random.randint(1000, 10_000),     # Many null characters
            "\n" * random.randint(1000, 10_000),     # Many newlines
            "🔥" * random.randint(100, 10_000),       # Many emojis
            " " * random.randint(1000, 10_000),      # Many spaces
            string.printable * random.randint(100, 10_000),  # Many printable characters
            ("A" * random.randint(1, 10_000)) + "\0"  # Null character after content
        ]
        for input in problematic:
            self.assertFalse(validate_length(input), f"Length {len(input)} should be invalid")
            
    def test_validate_contents(self):

        # Basic valid cases.
        self.assertTrue(validate_contents("ab1234"))   # 2 letters + 4 numbers.
        self.assertTrue(validate_contents("abc1234"))  # 3 letters + 4 numbers.
        
        # Generate random invalid inputs with intentionally invalid patterns.
        invalid_patterns = [
            # Wrong character types in letter positions.
            lambda: ''.join(random.choices(string.digits + string.punctuation, k=2)) + "1234",
            lambda: ''.join(random.choices(string.ascii_uppercase + string.punctuation, k=2)) + "1234",
            lambda: ''.join(random.choices(string.digits + string.punctuation, k=3)) + "1234",
            
            # Wrong character types in number positions.
            lambda: "ab" + ''.join(random.choices(string.ascii_letters + string.punctuation, k=4)),
            lambda: "abc" + ''.join(random.choices(string.ascii_letters + string.punctuation, k=4)),
            
            # Mixed invalid characters.
            lambda: ''.join(random.choices(string.punctuation + "🔥★☀☂☻♠♣", k=random.randint(1, 10))),
            
            # Unicode letters in wrong positions.
            lambda: "αβ1234",
            lambda: "αβγ1234",
            
            # Control characters.
            lambda: "ab\0\0\0\0",
            lambda: "abc\0\0\0\0",
            
            # Whitespace injection.
            lambda: "ab 1234",
            lambda: "abc 1234",
            lambda: " ab1234",
            lambda: "ab1234 ",
            
            # Mixed case.
            lambda: "aB1234",
            lambda: "aBc1234",
        ]
        
        # Test each invalid pattern multiple times with variations.
        for pattern in invalid_patterns:
            input = pattern()
            self.assertFalse(validate_contents(input), f"Contents '{input}' should be invalid")
                
        # Random fuzz testing.
        for _ in range(10_000_000):
            # Generate valid lengths.
            length = random.randint(6, 7)
            # Generate string with all kinds of characters.
            chars = string.printable + "αβγδεζηθ★☀☂☻♠♣🦅"
            input = ''.join(random.choices(chars, k=length))
            
            # Skip the rare case of accidentally generating a valid EUID.
            if len(input) in (6, 7) and \
               ((len(input) == 6 and input[:2].islower() and input[2:].isdigit()) or \
                (len(input) == 7 and input[:3].islower() and input[3:].isdigit())):
                continue
                
            self.assertFalse(validate_contents(input),f"Contents '{input}' should be invalid")
            
if __name__ == '__main__':
    unittest.main()