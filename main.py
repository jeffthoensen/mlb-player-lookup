import argparse
import sys

import requests

BASE_URL = "https://statsapi.mlb.com/api/v1"
DEFAULT_SEASON = "2025"


class PlayerLookupError(Exception):
    """Raised when a player or their stats can't be found."""


def search_player_id(name):
    response = requests.get(f"{BASE_URL}/people/search", params={"name": name}, timeout=10)
    response.raise_for_status()
    people = response.json().get("people", [])
    if not people:
        raise PlayerLookupError(f"No player found matching '{name}'.")
    return people[0]["id"]


def _fetch_stat_group(player_id, season, group):
    url = f"{BASE_URL}/people/{player_id}/stats"
    response = requests.get(
        url, params={"stats": "season", "season": season, "group": group}, timeout=10
    )
    response.raise_for_status()
    stats_list = response.json().get("stats", [])
    if stats_list and stats_list[0].get("splits"):
        return stats_list[0]["splits"][0].get("stat", {})
    return {}


def get_player_stats(player_id, season=DEFAULT_SEASON):
    pitching = _fetch_stat_group(player_id, season, "pitching")
    if "inningsPitched" in pitching:
        return "Pitcher", pitching

    hitting = _fetch_stat_group(player_id, season, "hitting")
    if "homeRuns" in hitting or "atBats" in hitting:
        return "Hitter", hitting

    raise PlayerLookupError(f"No usable stats available for {season}.")


def lookup(name, season=DEFAULT_SEASON):
    player_id = search_player_id(name)
    return get_player_stats(player_id, season)


def main():
    parser = argparse.ArgumentParser(description="Look up an MLB player's season stats.")
    parser.add_argument("name", nargs="?", help="Player name, e.g. 'Shohei Ohtani'")
    parser.add_argument(
        "--season", default=DEFAULT_SEASON, help=f"Season year (default: {DEFAULT_SEASON})"
    )
    args = parser.parse_args()

    name = args.name or input("Enter player name: ")

    try:
        role, stats = lookup(name, args.season)
    except (PlayerLookupError, requests.RequestException) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"\n{role} Stats for {args.season}:\n")
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
