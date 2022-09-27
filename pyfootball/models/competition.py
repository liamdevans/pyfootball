import traceback
import requests
from datetime import datetime

from pyfootball import globals
from .team import Team
from .fixture import Fixture
from .standings import Standings


class Competition():
    def __init__(self, data):
        """Takes a dict converted from the JSON response by the API and wraps
        the competition data within an object.

        :param data: The competition data from the API's response.
        :type data: dict
        """
        # self._teams_ep = data['_links']['teams']['href']
        # self._fixtures_ep = data['_links']['fixtures']['href']
        # self._league_table_ep = data['_links']['leagueTable']['href']
        self.id = data['id']
        self.area = data['area']
        self.name = data['name']
        self.code = data['code']
        self.type = data['type']
        self.emblem = data['emblem']
        self.start_date = datetime.strptime(data['currentSeason']['startDate'], '%Y-%m-%d')
        self.end_date = datetime.strptime(data['currentSeason']['endDate'], '%Y-%m-%d')
        self.current_matchday = data['currentSeason']['currentMatchday']
        self.winner = data['currentSeason']['winner']
        self.numberOfAvailableSeasons = data.get('numberOfAvailableSeasons', len(data['seasons']))
        self.last_updated = datetime.strptime(data['lastUpdated'],
                                              '%Y-%m-%dT%H:%M:%SZ')

    def get_fixtures(self):
        """Return a list of Fixture objects representing the fixtures in this
        competition for the current season.

        Sends one request to api.football-data.org.

        :returns: fixture_list: A list of Fixture objects.
        """
        r = requests.get(self._fixtures_ep, headers=globals.headers)
        globals.update_prev_response(r, self._fixtures_ep)
        r.raise_for_status()

        data = r.json()
        fixture_list = []
        for fixture in data['fixtures']:
            fixture_list.append(Fixture(fixture))
        return fixture_list

    def get_teams(self):
        """Return a list of Team objects representing the teams in this
        competition for the current season.

        Sends one request to api.football-data.org.

        :returns: team_list: A list of Team objects.
        """
        r = requests.get(self._teams_ep, headers=globals.headers)
        globals.update_prev_response(r, self._teams_ep)
        r.raise_for_status()

        data = r.json()
        team_list = []
        for tm in data['teams']:
            team_list.append(Team(tm))
        return team_list

    def get_league_table(self):
        """Return the league table for this competition.

        Sends one request to api.football-data.org.

        :returns: LeagueTable: A LeagueTable object.
        """
        r = requests.get(self._league_table_ep, headers=globals.headers)
        globals.update_prev_response(r, self._league_table_ep)
        r.raise_for_status()

        return Standings(r.json())
