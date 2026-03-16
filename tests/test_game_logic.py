import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from logic_utils import check_guess, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# FIX: Bug #1 — Hard difficulty should be harder than Normal
def test_hard_difficulty_range_larger_than_normal():
    """Verify that Hard difficulty has a larger range than Normal."""
    easy_low, easy_high = get_range_for_difficulty("Easy")
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")
    
    # Hard should have more possible values than Normal
    hard_range = hard_high - hard_low
    normal_range = normal_high - normal_low
    assert hard_range > normal_range, f"Hard range ({hard_range}) should be > Normal range ({normal_range})"


# FIX: Bug #3 — get_range_for_difficulty should return correct bounds
def test_get_range_for_difficulty_returns_correct_bounds():
    """Verify each difficulty returns the correct (low, high) tuple."""
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 200)


# FIX: Bug with hints being backwards
def test_hint_messages_are_correct():
    """Verify hints tell you the right direction to guess."""
    # If you guess 59 and secret is 50, you need to go LOWER
    outcome, message = check_guess(59, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in hint but got: {message}"
    
    # If you guess 1 and secret is 50, you need to go HIGHER
    outcome, message = check_guess(1, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in hint but got: {message}"
