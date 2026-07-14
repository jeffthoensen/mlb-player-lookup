# mlb-player-lookup

A CLI tool that looks up an MLB player's season stats by name, using the [MLB Stats API](https://statsapi.mlb.com/).

Looks up the player's ID, then pulls pitching stats if they're a pitcher, hitting stats otherwise.

## Usage

```
pip install -r requirements.txt
python main.py "Shohei Ohtani"
```

Or run it without an argument and it'll prompt you for a name. Pass `--season 2024` to look up a different year (defaults to 2025).

## Tests

```
pytest
```

Tests mock the API calls, so they run without hitting the network.

---

Built by [Jeff Thoensen](https://jeffthoensen.com), a Context-Driven QA Engineer focused on automation, API testing, and exploratory testing.
