import traceback
import requests

from pyfootball import globals
from pyfootball.globals import endpoints
from .player import Player
from .fixture import Fixture


class Team(object):
    def __init__(self, data):
        """Takes a dict converted from the JSON response by the API and wraps
        the team data within an object.

        :param data: The team data from the API's response.
        :type data: dict
        """
        self.id = data['id']
        self.name = data['name']
        self.short_name = data['shortName']
        self.code = data['tla']
        self.crest_url = data['crest']
        self.address = data['address']
        self.website = data['website']
        self.founded = data['founded']
        self.clubColors = data['clubColors']
        self.venue = data['venue']
        self.runningCompetitions = data['runningCompetitions']
        self.coach = data['coach']
        self.squad = data['squad']
        self.staff = data['staff']
        self.lastUpdated = data['lastUpdated']

        self._fixtures_ep = endpoints['team_fixtures'].format(self.id)
        self._players_ep = endpoints['team'].format(self.id)

    def get_fixtures(self):
        """Return a list of Fixture objects representing this season's
        fixtures for the current team.

        Sends one request to api.football-data.org.

        :returns: fixture_list: A list of Fixture objects.
        """
        r = requests.get(self._fixtures_ep, headers=globals.headers)
        globals.update_prev_response(r, self._fixtures_ep)
        r.raise_for_status()

        data = r.json()
        fixture_list = []
        for fixture in data['matches']:
            fixture_list.append(Fixture(fixture))
        return fixture_list

    def get_players(self):
        """Return a list of Player objects representing players on the current
        team.

        Sends one request to api.football-data.org.

        :returns: player_list: A list of Player objects.
        """
        r = requests.get(self._players_ep, headers=globals.headers)
        globals.update_prev_response(r, self._players_ep)
        r.raise_for_status()

        data = r.json()
        player_list = []
        for player in data['squad']:
            player_list.append(Player(player))
        return player_list
