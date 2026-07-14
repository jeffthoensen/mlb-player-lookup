import os
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import PlayerLookupError, get_player_stats, search_player_id  # noqa: E402


def _mock_response(json_data, status_code=200):
    response = MagicMock()
    response.status_code = status_code
    response.json.return_value = json_data
    if status_code >= 400:
        response.raise_for_status.side_effect = Exception("HTTP error")
    else:
        response.raise_for_status.return_value = None
    return response


@patch("main.requests.get")
def test_search_player_id_returns_id_when_found(mock_get):
    mock_get.return_value = _mock_response({"people": [{"id": 660271, "fullName": "Shohei Ohtani"}]})

    assert search_player_id("Shohei Ohtani") == 660271


@patch("main.requests.get")
def test_search_player_id_raises_when_not_found(mock_get):
    mock_get.return_value = _mock_response({"people": []})

    with pytest.raises(PlayerLookupError):
        search_player_id("Not A Real Player")


@patch("main.requests.get")
def test_get_player_stats_returns_pitcher_stats(mock_get):
    pitching_response = _mock_response(
        {"stats": [{"splits": [{"stat": {"inningsPitched": "180.0", "era": "2.50"}}]}]}
    )
    mock_get.return_value = pitching_response

    role, stats = get_player_stats(12345)

    assert role == "Pitcher"
    assert stats["inningsPitched"] == "180.0"


@patch("main.requests.get")
def test_get_player_stats_falls_back_to_hitter_stats(mock_get):
    empty_pitching = _mock_response({"stats": [{"splits": [{"stat": {}}]}]})
    hitting_response = _mock_response(
        {"stats": [{"splits": [{"stat": {"homeRuns": "35", "atBats": "550"}}]}]}
    )
    mock_get.side_effect = [empty_pitching, hitting_response]

    role, stats = get_player_stats(12345)

    assert role == "Hitter"
    assert stats["homeRuns"] == "35"


@patch("main.requests.get")
def test_get_player_stats_raises_when_no_usable_stats(mock_get):
    empty_response = _mock_response({"stats": []})
    mock_get.return_value = empty_response

    with pytest.raises(PlayerLookupError):
        get_player_stats(12345)
