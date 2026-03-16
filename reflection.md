# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

**Bug #1: Hard difficulty is easier than Normal**
- Expected: Hard difficulty should have the largest number range (most difficult to guess).
- Actually happened: Hard returns a range of 1-50, but Normal returns 1-100. Hard is actually easier to win at because there are fewer possible numbers.

**Bug #2: Range display doesn't match difficulty**
- Expected: The game should tell me the correct range for my chosen difficulty (1-20 for Easy, 1-100 for Normal, 1-50 for Hard).
- Actually happened: The game always displays "Guess a number between 1 and 100" no matter what difficulty I pick.

**Bug #3: "New Game" ignores the difficulty setting**
- Expected: When I click "New Game," the secret number should stay within the range I selected (e.g., 1-20 for Easy).
- Actually happened: The "New Game" button always generates a secret between 1-100, ignoring my difficulty choice.

**Bug #4: Hint messages are backwards** (found during testing)
- Expected: If I guess 59 and the secret is 50, it should say "Go LOWER" because 59 > 50.
- Actually happened: It said "Go HIGHER" when it should say "Go LOWER." The hint logic was completely inverted.

**Bug #5: Game over message doesn't disappear** (found during testing)
- Expected: When I click "New Game," the game should restart cleanly without any old messages.
- Actually happened: The "Game Over" error message stayed on screen even after clicking "New Game" because the game status wasn't being reset.

---

## 2. How did you use AI as a teammate?

**AI Tool Used:** Copilot Chat (using separate chat sessions per bug)

**Correct AI Suggestion:**
- **What the AI suggested:** When I described the Hard difficulty bug (range 1-50 vs Normal 1-100), Copilot immediately identified the logic error and suggested changing Hard to `return 1, 200` to make it properly harder. It also suggested fixing the dependent code (the "New Game" button and display text) to use the dynamic range values instead of hardcoding "1 and 100."
- **How I verified it:** I ran the updated game and played through multiple difficulties. Easy was fast to win (1-20), Normal took longer (1-100), and Hard took the most attempts (1-200). The difficulty scaling now makes sense. The tests I wrote confirmed the ranges are correct.

**Misleading/Incorrect AI Suggestion:**
- **What the AI suggested:** In the first chat about bug #1, Copilot initially suggested the ranges were "intentional design" for difficulty variants (like, maybe Hard was meant to be "precision hard" with fewer numbers). This was clearly wrong because the attempt limits showed Hard gets only 5 attempts vs Normal's 8, meaning fewer numbers to search through makes an easier game, not harder.
- **How I verified it:** I tested by playing through all difficulties and confirmed larger ranges = harder games. The UI also showed attempts left; matching that with range size made the bug obvious. Copilot corrected itself when I pushed back with evidence.

---

## 3. Debugging and testing your fixes

**How I decided if a bug was really fixed:**
- For Bug #1 (Hard range): I manually tested the game by playing all three difficulties and counting attempts needed to win. Hard now takes more guesses due to larger range, confirming the fix worked.
- For Bug #3 (New Game range): After selecting Easy mode and clicking "New Game," the secret now stays within 1-20 instead of jumping to random 1-100 numbers.
- For Bug #4 (backwards hints): I tested with specific numbers (guess 59 vs secret 50) to verify the hint now correctly says "Go LOWER."
- For Bug #5 (game over message): Played a game until "Game Over," then clicked "New Game" and verified the message disappeared and the game restarted cleanly.
- I also wrote automated pytest tests to verify the fixes programmatically.

**Tests I ran:**
1. **Manual game play:** Played through Easy, Normal, and Hard. Confirmed difficulty progression makes sense. Also tested the hints give correct directions after each guess.
2. **Pytest automated tests:** 
   - `test_hard_difficulty_range_larger_than_normal`: Verifies Hard range > Normal range ✓
   - `test_get_range_for_difficulty_returns_correct_bounds`: Confirms exact values (1,20), (1,100), (1,200) ✓
   - `test_hint_messages_are_correct`: Verifies hints tell you to go HIGHER when too low and LOWER when too high ✓
   - Plus 3 more existing tests all pass ✓
   - **Total: 6/6 tests passing** ✓

**How AI helped with testing:**
- Copilot suggested the specific assertions for the test cases. It also advised me to check "import paths" in pytest when the tests failed initially, which helped me fix the module import from logic_utils.py. When I found the hint messages were backwards, Copilot helped me write a clear test that would catch this bug.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
