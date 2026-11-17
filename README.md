# CS449_Peg_Solitaire
Peg Solitaire desktop application developed in Python with PySide6 for UMKC CS 449, using object-oriented design, automated testing, and incremental development.

## Sprint Deliverables

### Sprint 1

- [Requirements document (Google Docs)](https://docs.google.com/document/d/1gtNmhjpZ8GOP1iy-_Pi74YuSBYM-okm2su7dUTFgHxI)

### Sprint 2

- [Implementation, testing, and verification document (Google Docs)](https://docs.google.com/document/d/18869oToBNmMGJ4UX1sziUcvazZLB5wOkpidrJdy6A8c/edit?usp=drivesdk)
- Gameplay engine and PySide6 interface; 19 passing automated tests including two AI-generated tests.
- [Narrated Sprint 2 demonstration video (YouTube)](https://youtu.be/kdn6kFun3tw).

### Sprint 3

- [Victor Olatunji — Sprint 3 implementation, testing, and design analysis (Google Docs)](https://docs.google.com/document/d/1TSSuqepqEouK6Dojwkq4Kw5mVtUCGJP3rduIVfxccWg/edit?usp=drivesdk)
- [Sprint 3 implementation branch](https://github.com/vonn4/CS449_Peg_Solitaire/tree/sprint3).
- Manual and automated gameplay on English, Hexagon, and Diamond boards; supported board sizes, game-over detection, and manual randomization.
- Game recording to JSON, recording validation, and replay through the PySide6 interface.
- 32 passing automated tests, including Sprint 2 regression coverage and Sprint 3 session/recording tests.
- **Narrated Sprint 3 demonstration video (YouTube):** link pending upload.

## Run Sprint 3

```powershell
python -m pip install -r requirements.txt
python -m solitaire.sprint3_gui
```

Run the full automated test suite:

```powershell
python -m unittest discover -s tests -v
```

**Note:** The Sprint 3 application and tests are on the `sprint3` branch. Check out that branch before running these commands. The recording feature saves and loads JSON files through the GUI.
