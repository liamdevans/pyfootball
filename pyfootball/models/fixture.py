import traceback
from datetime import datetime


class Fixture(object):
    def __init__(self, data):
        """Takes a dict converted from the JSON response by the API and wraps
        the fixture data within an object.

        :param data: The fixture data from the API's response.
        :type data: dict
        """
        self.area = data['area']
        self.competition = data['competition']
        self.season = data['season']
        self.id = data['id']
        self.date = datetime.strptime(data['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
        self.status = data['status']
        self.matchday = data['matchday']
        self.stage = data['stage']
        self.group = data['group']
        self.lastUpdated = data['lastUpdated']
        self.home_team = data['homeTeam']
        self.home_team_id = self.home_team['id']
        self.home_team_name = self.home_team['name']
        self.away_team = data['awayTeam']
        self.away_team_id = self.away_team['id']
        self.away_team_name = self.away_team['name']
        self.score = data['score']
        self.odds = data['odds']
        self.referees = data['referees']

        if self.status == 'FINISHED':
            if self.score['winner'] == 'HOME_TEAM':
                self.winner = self.home_team_name
            elif self.score['winner'] == 'AWAY_TEAM':
                self.winner = self.away_team_name
            else:
                self.winner = 'DRAW'
        else:
            self.winner = None

    def __repr__(self):
        return f"[{self.date}] {self.home_team_name} vs {self.away_team_name}"

