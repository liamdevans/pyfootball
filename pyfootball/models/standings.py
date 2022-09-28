import traceback


class Standings(object):
    def __init__(self, data):
        """Takes a dict converted from the JSON response by the API and wraps
        the league table data within an object.

        :param data: The league table data from the API's response.
        :type data: dict
        """
        self.area = data['area']
        self.competition = data['competition']
        self.season = data['season']

        if self.competition['type'] == 'LEAGUE':
            self.total_standings = self.create_standings_list(data['standings'][0])
            self.home_standings = self.create_standings_list(data['standings'][1])
            self.away_standings = self.create_standings_list(data['standings'][2])
        elif self.competition['type'] == 'LEAGUE_CUP':
            self.total_standings = data['standings']    # TODO fix for LEAGUE_CUP type

    def create_standings_list(self, data):
        _standings_list = []
        for pos in data['table']:
            _standings_list.append(self.Standing(pos))
        return _standings_list

    class Standing(object):
        def __init__(self, data):
            """A private LeagueTable class that stores information about
            a given position in the table.
            """
            self.position = data['position']
            self.team = data['team']
            self.team_id = self.team['id']
            self.team_name = self.team['name']
            self.team_shortName = self.team['shortName']
            self.team_tla = self.team['tla']
            self.team_crest = self.team['crest']
            self.games_played = data['playedGames']
            self.form = data['form']
            self.wins = data['won']
            self.draws = data['draw']
            self.losses = data['lost']
            self.points = data['points']
            self.goals = data['goalsFor']
            self.goals_against = data['goalsAgainst']
            self.goal_difference = data['goalDifference']