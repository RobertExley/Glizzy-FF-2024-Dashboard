import requests

REQUEST_HEADERS = {
    'Date': 'Wed, 06 Nov 2024 07:02:49 GMT',
    'Content-Type': 'application/json; charset=utf-8',
    'Transfer-Encoding': 'chunked',
    'Connection': 'keep-alive',
    'access-control-allow-credentials': 'true',
    'access-control-allow-origin': '*',
    'access-control-expose-headers': 'etag,date',
    'cache-control': 'public, s-maxage=300',
    'x-request-id': 'ee7c57a0d897f20600b1b4e9e1654a4c',
    'Strict-Transport-Security': 'max-age=15724800; includeSubDomains',
    'CF-Cache-Status': 'MISS',
    'Last-Modified': 'Wed, 06 Nov 2024 07:02:49 GMT',
    'Vary': 'Accept-Encoding',
    'Server': 'cloudflare',
    'CF-RAY': '8de338618f2c4313-EWR',
    'Content-Encoding': 'gzip',
}



class SleeperDataCollector:

    def __init__(self, league_id):

        self.league_id = league_id
        self.endpoints = {
            'nfl_state': 'https://api.sleeper.app/v1/state/nfl',
            'matchups': f'https://api.sleeper.app/v1/league/{self.league_id}/matchups/',
            'rosters': f'https://api.sleeper.app/v1/league/{self.league_id}/rosters',
            'users': f'https://api.sleeper.app/v1/league/{self.league_id}/users'
        }

        self.roster_data = self._get_roster_data()
        self.user_data = self._get_user_data()
        self.nfl_state = self._get_nfl_state()

        self.roster_ids_to_user_ids = self._map_roster_ids_to_user_ids()
        self.user_ids_to_usernames = self._map_user_ids_to_usernames()
        self.roster_ids_to_usernames = self._map_roster_ids_to_usernames()

    def _get_generic_request(self, url: str, headers: dict = REQUEST_HEADERS):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to retrieve data: {response.status_code}"
        
    def _map_roster_ids_to_user_ids(self):
        return { roster['roster_id']:roster['owner_id'] for roster in self.roster_data }
    
    def _map_user_ids_to_usernames(self):
        return { user['user_id']:user['display_name'] for user in self.user_data }
    
    def _map_roster_ids_to_usernames(self):
        return { roster_id:self.user_ids_to_usernames[self.roster_ids_to_user_ids[roster_id]] 
                for roster_id in self.roster_ids_to_user_ids }
    
    def _get_matchup_data(self):
        return self._get_generic_request(self.endpoints['matchups'])
    
    def _get_roster_data(self):
        return self._get_generic_request(self.endpoints['rosters'])
    
    def _get_user_data(self):
        return self._get_generic_request(self.endpoints['users'])
    
    def _get_nfl_state(self):
        return self._get_generic_request(self.endpoints['nfl_state'])

    def get_current_week(self):
        return self.nfl_state["week"]
    
    def get_usernames(self):
        return self.user_ids_to_usernames.values()
    
    def get_matchups_and_scores_one_week(self, week: int):
        week_matchup_endpoint = self.endpoints["matchups"] + str(week)
        matchups_data = self._get_generic_request(week_matchup_endpoint)
        
        matchups_map = { matchup['matchup_id']:[] for matchup in matchups_data } # initialize
        week_scores = {}
        
        for matchup in matchups_data:
            roster_id = matchup['roster_id']
            matchup_id = matchup['matchup_id']
            username = self.roster_ids_to_usernames[roster_id]
            matchups_map[matchup_id].append(username)
            week_scores[username] = matchup['points']

        formatted_week_matchups = [ (v[0], v[1]) for _, v in matchups_map.items() ]

        return formatted_week_matchups, week_scores

    def get_all_weekly_matchups_and_scores(self, first_week_of_playoffs: int = 15):

        weekly_matchups = {}
        weekly_scores = { v:[] for _, v in self.roster_ids_to_usernames.items() }
        
        for i in range(1, first_week_of_playoffs):
            formatted_week_matchups, week_scores = self.get_matchups_and_scores_one_week(i)
            weekly_matchups[i] = formatted_week_matchups
            for username, score in week_scores.items():
                if i < self.get_current_week():
                    weekly_scores[username].append(score)

        return weekly_matchups, weekly_scores
    
    def get_wins(self):
        return { self.roster_ids_to_usernames[roster["roster_id"]]:roster["settings"]["wins"] for roster in self.roster_data }
    
    def get_weekly_fractional_records(self, weekly_scores):

        num_weeks = self.get_current_week() - 1
        weekly_fractional_records = {player: [0] * num_weeks for player in weekly_scores}
        
        for week in range(num_weeks):
            week_scores = [(player, weekly_scores[player][week]) for player in weekly_scores]
            print(week_scores)

            for player1, score1 in week_scores:
                wins = 0
                for player2, score2 in week_scores:
                    if player1 != player2 and score1 > score2:
                        wins += 1
                weekly_fractional_records[player1][week] = wins
        
        return weekly_fractional_records