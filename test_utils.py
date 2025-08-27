#!/usr/bin/env python3
"""
Basic tests for the utils module.
Run with: python test_utils.py
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (
    validate_team_id,
    validate_commentator,
    validate_language,
    get_team_name
)

def test_validate_team_id():
    """Test team ID validation."""
    print("Testing team ID validation...")
    
    # Valid team IDs
    assert validate_team_id("134860") == True
    assert validate_team_id("133602") == True
    assert validate_team_id("123456") == True
    
    # Invalid team IDs
    assert validate_team_id("") == False
    assert validate_team_id("abc123") == False
    assert validate_team_id("12.34") == False
    assert validate_team_id("12-34") == False
    
    print("✅ Team ID validation tests passed!")

def test_validate_commentator():
    """Test commentator validation."""
    print("Testing commentator validation...")
    
    # Valid commentators
    assert validate_commentator("Ravi Shastri") == True
    assert validate_commentator("Harsha Bhogle") == True
    assert validate_commentator("Tony Romo") == True
    
    # Invalid commentators
    assert validate_commentator("John Doe") == False
    assert validate_commentator("") == False
    assert validate_commentator("123") == False
    
    print("✅ Commentator validation tests passed!")

def test_validate_language():
    """Test language validation."""
    print("Testing language validation...")
    
    # Valid languages
    assert validate_language("English") == True
    assert validate_language("Hindi") == True
    assert validate_language("Spanish") == True
    
    # Invalid languages
    assert validate_language("French") == False
    assert validate_language("") == False
    assert validate_language("123") == False
    
    print("✅ Language validation tests passed!")

def test_get_team_name():
    """Test team name retrieval."""
    print("Testing team name retrieval...")
    
    # Known team IDs
    assert get_team_name("134860") == "Boston Celtics"
    assert get_team_name("133602") == "Los Angeles Lakers"
    assert get_team_name("133604") == "Golden State Warriors"
    
    # Unknown team ID
    assert get_team_name("999999") == "Unknown Team"
    
    print("✅ Team name retrieval tests passed!")

def run_all_tests():
    """Run all tests."""
    print("🧪 Running AI Sports Commentator Tests...\n")
    
    try:
        test_validate_team_id()
        test_validate_commentator()
        test_validate_language()
        test_get_team_name()
        
        print("\n🎉 All tests passed successfully!")
        return True
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
