import json
import requests
from bs4 import BeautifulSoup
from typing import Dict, List
import pandas as pd

BASE_URL = "https://understat.com/match/"
BASE_LEAGUE_URL = "https://understat.com/league/"


def scrape(id: str, type: str, league=None) -> str:
    match type:
        case "match":
            URL = BASE_URL + id
        case "season":
            match league:
                case "EPL":
                    URL = BASE_LEAGUE_URL + "EPL/" + str(id)
                case "La_liga":
                    URL = BASE_LEAGUE_URL + "La_liga/" + str(id)
                case "Bundesliga":
                    URL = BASE_LEAGUE_URL + "Bundesliga/" + str(id)
                case "Serie_A":
                    URL = BASE_LEAGUE_URL + "Serie_A/" + str(id)
                case "Ligue_1":
                    URL = BASE_LEAGUE_URL + "Ligue_1/" + str(id)
                case "RFPL":
                    URL = BASE_LEAGUE_URL + "RFPL/" + str(id)

    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "lxml")
    data = soup.find_all("script")
    return data


def create_shots_dataset(data: str) -> List[Dict]:
    shots_string = data[1].string
    start_index = shots_string.index("('") + 2
    end_index = shots_string.index("')")
    json_string = shots_string[start_index:end_index]
    json_string = json_string.encode("utf8").decode("unicode_escape")
    shots_dict = json.loads(json_string)
    shots_home = shots_dict["h"]
    shots_away = shots_dict["a"]

    return shots_home + shots_away


def create_df(id: int) -> pd.DataFrame:
    match = scrape(id, "match")
    df = pd.DataFrame(create_shots_dataset(match))
    return df


def generate_players_dict(year: str, league: str) -> Dict:

    soup_scripts = scrape(year, "season", league)

    script = soup_scripts[3].string

    start_index = script.index("('") + 2
    end_index = script.index("')")
    json_string = script[start_index:end_index]
    json_string = json_string.encode("utf8").decode("unicode_escape")
    players_dict = json.loads(json_string)
    return players_dict
