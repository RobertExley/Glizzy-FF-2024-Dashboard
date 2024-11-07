import requests

LEAGUE_ID = '1124814690363400192'

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

ENDPOINTS = {
    'nfl_state': 'https://api.sleeper.app/v1/state/nfl',
    'matchups': f'https://api.sleeper.app/v1/league/{LEAGUE_ID}/matchups/',
    'rosters': f'https://api.sleeper.app/v1/league/{LEAGUE_ID}/rosters',
    'users': f'https://api.sleeper.app/v1/league/{LEAGUE_ID}/users'
}

class SleeperDataCollector:

    def __init__(self):
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
        roster_data = self._get_roster_data()
        return { roster['roster_id']:roster['owner_id'] for roster in roster_data }
    
    def _map_user_ids_to_usernames(self):
        user_data = self._get_user_data()
        return { user['user_id']:user['display_name'] for user in user_data }
    
    def _map_roster_ids_to_usernames(self):
        return { roster_id:self.user_ids_to_usernames[self.roster_ids_to_user_ids[roster_id]] 
                for roster_id in self.roster_ids_to_user_ids }
    
    def _get_matchup_data(self):
        return self._get_generic_request(ENDPOINTS['matchups'])
    
    def _get_roster_data(self):
        return self._get_generic_request(ENDPOINTS['rosters'])
    
    def _get_user_data(self):
        return self._get_generic_request(ENDPOINTS['users'])
    
    def _get_nfl_state(self):
        return self._get_generic_request(ENDPOINTS['nfl_state'])

    def get_current_week(self):
        return self._get_nfl_state()["week"]
    
    def get_matchups_and_scores_one_week(self, week: int):
        week_matchup_endpoint = ENDPOINTS["matchups"] + str(week)
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
                if score > 0:
                    weekly_scores[username].append(score)

        return weekly_matchups, weekly_scores