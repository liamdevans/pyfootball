import datetime

import requests
import os

import globals
from globals import endpoints
from models.competition import Competition
from models.team import Team
from models.fixture import Fixture
from models.standings import Standings
from models.player import Player


class Football(object):
    def __init__(self, api_key=None):
        """Takes either an api_key as a keyword argument or tries to access
        an environmental variable ``PYFOOTBALL_API_KEY``, then uses the key to
        send a test request to make sure that it's valid. The api_key
        kwarg takes precedence over the envvar.

        Sends one request to api.football-data.org.

        :keyword api_key: The user's football-data.org API key.
        :type api_key: string
        """
        if api_key:
            key = api_key
        elif os.getenv('PYFOOTBALL_API_KEY', None):
            key = os.getenv('PYFOOTBALL_API_KEY')
        else:
            raise ValueError("Couldn't find an API key in the keyword " +
                             "argument api_key nor the environmental " +
                             "variable PYFOOTBALL_API_KEY.")

        endpoint = endpoints['all_competitions']
        globals.headers = {'X-Auth-Token': key}
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()
        globals.api_key = key

    def get_prev_response(self):
        """Returns information about the most recent response.

        :returns: prev_response: Information about the most recent response.
        """
        return globals.prev_response

    def get_competition(self, comp_id):
        """Returns a Competition object associated with the competition ID.

        Sends one request to api.football-data.org.

        :param comp_id: The competition ID.
        :type comp_id: integer

        :returns: Competition: The Competition object.
        """
        endpoint = endpoints['competition'].format(comp_id)
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()

        return Competition(r.json())

    def get_all_competitions(self):
        """Returns a list of Competition objects representing the current
        season's competitions.

        Sends one request to api.football-data.org.

        :returns: comp_list: List of Competition objects.
        """
        endpoint = endpoints['all_competitions']
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()

        data = r.json()
        comp_list = []
        for comp in data['competitions']:
            comp_list.append(Competition(comp))
        return comp_list

    def get_league_table(self, comp_id):
        """Given a competition ID, returns a LeagueTable object for the
        league table associated with the competition.

        Sends one request to api.football-data.org.

        :param comp_id: The competition ID.
        :type comp_id: integer

        :returns: LeagueTable: A LeagueTable object.
        """
        endpoint = endpoints['league_table'].format(comp_id)
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()
        data = r.json()

        return Standings(data)

    def get_comp_fixtures(self, comp_id):
        """Given an ID, returns a list of Fixture objects associated with the
        given competition, for the current season.

        Sends one request to api.football-data.org.

        :param comp_id: The competition ID.
        :type comp_id: integer

        :returns: fixture_list: A list of Fixture objects.
        """
        endpoint = endpoints['comp_fixtures'].format(comp_id)
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()

        data = r.json()
        fixture_list = []
        for fixture in data['matches']:
            fixture_list.append(Fixture(fixture))
        return fixture_list

    def get_competition_teams(self, comp_id):
        """Given an ID, returns a list of Team objects associated with the
        given competition.

        Sends one request to api.football-data.org.

        :param comp_id: The competition ID.
        :type comp_id: integer

        :returns: team_list: A list of Team objects.
        """
        endpoint = endpoints['comp_teams'].format(comp_id)
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()

        data = r.json()
        team_list = []
        for tm in data['teams']:
            team_list.append(Team(tm))
        return team_list

    def get_fixture(self, fixture_id):
        """Returns a Fixture object associated with the given ID. The response
        includes a head-to-head between teams; this will be implemented
        in the near future.

        Sends one request to api.football-data.org.

        :param fixture_id: The fixture ID.
        :type fixture_id: integer

        :returns: Fixture: A Fixture object.
        """
        endpoint = endpoints['fixture'].format(fixture_id)
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()
        data = r.json()
        return Fixture(data)

    def get_all_fixtures(self):
        """Returns a list of all Fixture objects in the specified time frame.
        Defaults to the next 7 days or "n7". TODO: Include timeFrameStart
        and timeFrameEnd, and filter for specifying time frame.

        Sends one request to api.football-data.org.

        :returns: fixture_list: A list of Fixture objects.
        """
        endpoint = endpoints['all_fixtures']
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()

        data = r.json()
        fixture_list = []
        for fixture in data['matches']:
            fixture_list.append(Fixture(fixture))
        return fixture_list

    def get_team(self, team_id):
        """Given an ID, returns a Team object for the team associated with
        the ID.

        Sends one request to api.football-data.org.

        :param team_id: The team ID.
        :type team_id: integer

        :returns: Team: A Team object.
        """
        endpoint = endpoints['team'].format(team_id)
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()

        return Team(r.json())

    def get_team_players(self, team_id):
        """Given a team ID, returns a list of Player objects associated
        with the team.

        Sends one request to api.football-data.org.

        :param team_id: The team ID.
        :type team_id: integer

        :returns: player_list: A list of Player objects in the specified team.
        """
        endpoint = endpoints['team'].format(team_id)
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()

        data = r.json()
        player_list = []
        for player in data['squad']:
            player_list.append(Player(player))
        return player_list

    def get_team_fixtures(self, team_id):
        """Given a team ID, returns a list of Fixture objects associated
        with the team.

        Sends one request to api.football-data.org.

        :param team_id: The team ID.
        :type team_id: integer

        :returns: fixture_list: A list of Fixture objects for the team.
        """
        endpoint = endpoints['team_fixtures'].format(team_id)
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()

        data = r.json()
        fixture_list = []
        for fixture in data['matches']:
            fixture_list.append(Fixture(fixture))
        return fixture_list

    def get_player(self, player_id):
        """Given a player ID, returns a Player object associated with
        the player.

        Sends one request to api.football-data.org.

        :param player_id: The player ID.
        :type player_id: integer

        :return: Player: A Player object for the player.
        """
        endpoint = endpoints['player'].format(player_id)
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()
        data = r.json()

        return Player(data)

    def get_player_matches(self, player_id, n_matches=15):
        """Given a player_id, returns n_matches number of Fixture objects
        of which the player has played in.

        :param player_id: The player ID
        :param n_matches: The number of matches to receive (default 15)
        :return: matches_list: List of Fixture objects
        """
        endpoint = endpoints['player_matches'].format(player_id) + '?limit={}'.format(n_matches)
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()
        data = r.json()

        matches_list = []
        for match in data['matches']:
            matches_list.append(Fixture(match))
        return matches_list


if __name__ == '__main__':
    f = Football()

    # print([i.competition['type'] for i in f.get_team_fixtures(328)])
#     globals.headers = {'X-Auth-Token': os.getenv('PYFOOTBALL_API_KEY'),
#                        'X-Unfold-Goals': 'true'}

    # print([c.name for c in f.get_all_competitions()]) # passed
    # print(f.get_competition('ELC').name)  # passed
    # print(f.get_competition_teams('ELC'))     # passed
    # print(set([fix.season['startDate'] for fix in f.get_comp_fixtures('ELC')]))   # passed

    # print(f.get_all_fixtures())   # passed
    # print(f.get_fixture(12).winner) # passed

    # print([t.team_tla for t in f.get_league_table(2016).total_standings])   # passed
    # print(f.get_prev_response())   # passed
    # team = f.get_team(328)
    # print(team)     # passed

    fix = f.get_team_fixtures(328)[2]
    team_id = fix.home_team_id
    print(f.get_team(team_id).venue)

    # print([h.home_team_name for h in f.get_team_fixtures(90)])  # passed
    # print(f.search_teams('manchester')) # failed
    # print([p.nationality for p in f.get_team_players(90)])  # passed

    # print(f.get_player(16275).shirt_number)  # passed
    # print([m.winner for m in f.get_player_matches(16275, 20)]) # passed

    # fix = f.get_comp_fixtures('ELC')[0]
    # print([key for key in fix.__dict__.keys() if type(fix.__dict__[key]) == datetime.datetime])

    # comp = f.get_competition('ELC')
    # print([key for key in comp.__dict__.keys() if type(comp.__dict__[key]) == datetime.datetime])

