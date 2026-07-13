# mlb-player-lookup

A small CLI tool that looks up a current-season MLB player's stats by name.

Enter a player's name and it queries the [MLB Stats API](https://statsapi.mlb.com/) to find their player ID, then pulls their 2025 season stats — pitching stats if they're a pitcher, hitting stats otherwise.

## Usage

```
pip install -r requirements.txt
python main.py
```

You'll be prompted for a player name, then the script prints their stats for the season.
