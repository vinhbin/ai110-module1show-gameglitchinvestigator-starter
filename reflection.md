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

**Bug #6: Secret number was being converted to string on even attempts** (found during code review)
- Expected: The secret should always be an integer so comparison works correctly on every guess.
- Actually happened: The code had `if attempts % 2 == 0: secret = str(secret)` which converted the secret to a string on even attempts. This caused type mismatches when comparing integer guesses to string secrets, requiring a hacky `try/except TypeError` workaround in the check_guess function.

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
- For Bug #6 (string conversion): I reviewed the code and realized the secret was being converted to a string on even attempts. Removing this line and simplifying check_guess means the function now handles all attempts the same way.
- I also wrote automated pytest tests to verify the fixes programmatically.

**Tests I ran:**
1. **Manual game play:** Played through Easy, Normal, and Hard. Confirmed difficulty progression makes sense. Also tested the hints give correct directions after each guess, including on even-numbered attempts.
2. **Pytest automated tests:** 
   - `test_hard_difficulty_range_larger_than_normal`: Verifies Hard range > Normal range ✓
   - `test_get_range_for_difficulty_returns_correct_bounds`: Confirms exact values (1,20), (1,100), (1,200) ✓
   - `test_hint_messages_are_correct`: Verifies hints tell you to go HIGHER when too low and LOWER when too high ✓
   - Plus 3 more existing tests all pass ✓
   - **Total: 6/6 tests passing** ✓

**How AI helped with testing:**
- Copilot suggested the specific assertions for the test cases. It also advised me to check "import paths" in pytest when the tests failed initially, which helped me fix the module import from logic_utils.py. When I found the hint messages were backwards, Copilot helped me write a clear test that would catch this bug. However, I also found additional bugs by reading the code carefully myself and asking critical questions about why certain things were being done.

---

## 4. What did you learn about Streamlit and state?

**Why the secret number kept changing:**
The secret number was changing because Streamlit reruns the entire Python script every time a user interacts with the app. Every button click, text input, or setting change triggers a full rerun from the top of the script. Without the `if "secret" not in st.session_state:` check, the code would execute `random.randint()` on every single rerun, creating a different secret each time. The game was essentially generating a brand new secret after every guess instead of keeping the same one throughout the game.

**Streamlit reruns and session state explained:**
Imagine Streamlit as a movie projector that restarts the film from the beginning every time someone touches a button. Without anything to "remember," all the settings reset. Session state is like a sticky note that survives the restart—it writes down values that need to stick around between reruns. So on the first run, you write down the secret number on your sticky note. On the second run (after the user clicks), you check the note first and say "oh, the secret is already here, skip generating a new one." This way the secret stays the same throughout the game.

**What made the secret number stable:**
The fix was using `if "secret" not in st.session_state: st.session_state.secret = random.randint(low, high)`. This checks if the secret already exists in session state. If it does, skip generating a new one. If it's the first time, create it and store it. By doing this only once at the start and never overwriting it during gameplay, the secret becomes stable and persists through all the reruns that happen as the player makes guesses.

---

## 5. Looking ahead: your developer habits

**One habit I want to reuse:**
Writing automated tests (pytest) alongside code fixes. In this project, every time I fixed a bug, I wrote a test to verify it worked and prevent regressions. This forced me to think clearly about what "correct" means and made me confident my fix actually solved the problem instead of just guessing. I'll use this habit in future projects because it catches bugs early and proves code works before showing it to anyone.

**One thing I'd do differently with AI next time:**
I would be more skeptical and ask more critical questions. When Copilot initially suggested the Hard difficulty ranges were "intentional design," I should have immediately asked "why would that make sense?" instead of accepting it. I found my best bug fixes (like Bug #6 with the string conversion) by reading the code myself and asking "why is this here?" rather than just running suggested code. Next time I'll trust my own critical thinking as much as AI suggestions.

**How this changed my thinking about AI code:**
AI can write syntactically perfect code that's logically broken—like hints that point in the wrong direction or difficulty ranges that are backwards. This taught me that AI is an incredible assistant for speed and boilerplate, but it's not a replacement for human judgment. Every AI-generated feature needs verification through testing and manual inspection, because "it compiles" doesn't mean "it's correct."
