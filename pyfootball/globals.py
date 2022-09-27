api_key = ""
headers = {}
prev_response = {}

_base = 'https://api.football-data.org/v4/'

endpoints = {
    'fixture': _base + 'matches/{}',
    'all_fixtures': _base + 'matches/',
    'competition': _base + 'competitions/{}',
    'all_competitions': _base + 'competitions/',
    'comp_teams': _base + 'competitions/{}/teams',
    'comp_fixtures': _base + 'competitions/{}/matches',
    'team': _base + 'teams/{}',
    'team_fixtures': _base + 'teams/{}/matches/',
    'league_table': _base + 'competitions/{}/standings'
}


def update_prev_response(r, endpoint):
    """ Sets the prev_response attribute to contain a dict that includes
        the response status code and headers of the most recent HTTP
        request.

        Arguments:
        r -- The response object (of the latest HTTP request).
        endpoint -- The endpoint used (in the latest HTTP request).
    """
    global prev_response
    prev_response = r.headers
    prev_response['Status-Code'] = r.status_code
    prev_response['Endpoint'] = endpoint
