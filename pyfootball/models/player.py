import traceback
from datetime import datetime


class Player():
    def __init__(self, data):
        """Takes a dict converted from the JSON response by the API and wraps
        the player data within an object.

        :param data: The player data from the API's response.
        :type data: dict
        """
        self.id = data['id']
        self.name = data['name']
        self.position = data['position']
        self.date_of_birth = datetime.strptime(data['dateOfBirth'],
                                               '%Y-%m-%d').date()
        self.nationality = data['nationality']
        self.shirt_number = data.get('shirtNumber')
        self.lastUpdated = data.get('lastUpdated')
        self.currentTeam = data.get('currentTeam')
