# CS 449 — Sprint 3

Branch: `sprint3`. This extends the existing Sprint 2 engine without replacing `solitaire/game.py` or the original Sprint 0 rating preview.

## Launch and test
From the repository root, in an environment with PySide6 installed:

```powershell
python -m unittest discover -s tests -v
python -m solitaire.sprint3_gui
```

## Interface
Select English, Hexagon, or Diamond; choose a supported size and Manual or Automated mode; then click **New Game**. In Manual mode, click an occupied source hole then an empty legal destination. **Randomize** executes one randomly chosen legal move and records it. In Automated mode, **Autoplay** runs legal moves on a timer until none remain. **Stop** pauses autoplay/replay. **Save Recording** writes a JSON text file. **Load & Replay** validates a JSON recording and animates its recorded board states.

## Architecture
- `solitaire.game.SolitaireGame`: framework-independent board geometry, legal moves, game-over state.
- `solitaire.sprint3.GameSession`: mode-specific operations, randomization, history, JSON persistence and validation.
- `solitaire.sprint3_gui.SolitaireWindow`: PySide6 controls, board drawing, timed autoplay and replay.
- `tests/test_sprint3.py`: unit tests for manual and automated modes, JSON round-trip and corruption handling.

Manual and automated games share the same rules engine and session representation. Mode-specific methods guard which operations are allowed. This is composition rather than a ManualGame/AutomatedGame inheritance hierarchy.

## Verification and caveats
The existing 19 Sprint 2 tests passed in the user's local workspace before this branch was created. Sprint 3 tests and GUI must still be run in the user's environment; no GitHub Actions workflow is configured here. The implementation's randomization chooses one legal jump rather than shuffling arbitrary occupied holes; verify that interpretation against `CS449HomeworkOverview.docx`. Board sizes 7 and 9 are inherited from Sprint 2 and should likewise be checked against the overview.

## Safe local update
Do not discard local changes or force-reset the existing branch. Run `git status` first. If clean, run `git fetch origin` and `git switch --track origin/sprint3`. If not clean, preserve your local changes (commit or stash) before switching. Because local and remote main previously diverged, avoid merging main blindly.

## Demonstration
Video must be at most 5 minutes and include manual English until game-over, manual Hexagon until game-over, automated game until game-over, manual game with periodic randomization until game-over, manual unit tests, and automated unit tests. Show save/load replay as time permits. Submit GitHub link and ensure instructor access. Complete written mapping and design analysis using the actual Sprint 1 acceptance criteria and definitions supplied in class.
