import requests

def search_player_id(name):
    url = f"https://statsapi.mlb.com/api/v1/people/search?name={name}"
    response = requests.get(url)
    data = response.json()
    people = data.get("people", [])
    if not people:
        print("Player not found.")
        return None
    return people[0]["id"]

def get_player_stats(player_id):
    season = "2025"
    base_url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats"

    # First, try to get pitching stats
    pitching_url = f"{base_url}?stats=season&season={season}&group=pitching"
    response = requests.get(pitching_url)
    data = response.json()
    stats_list = data.get("stats", [])
    if stats_list and stats_list[0].get("splits"):
        stats = stats_list[0]["splits"][0].get("stat", {})
        if "inningsPitched" in stats:
            return "Pitcher", stats

    # Then, try hitting stats
    hitting_url = f"{base_url}?stats=season&season={season}&group=hitting"
    response = requests.get(hitting_url)
    data = response.json()
    stats_list = data.get("stats", [])
    if stats_list and stats_list[0].get("splits"):
        stats = stats_list[0]["splits"][0].get("stat", {})
        if "homeRuns" in stats or "atBats" in stats:
            return "Hitter", stats

    return None, None

def main():
    name = input("Enter player name: ")
    player_id = search_player_id(name)
    if not player_id:
        return

    role, stats = get_player_stats(player_id)
    if not stats:
        print("No usable stats available for 2025.")
        return

    print(f"\n{role} Stats for 2025:\n")
    for key, value in stats.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
