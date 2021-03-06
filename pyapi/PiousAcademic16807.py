from collections import deque
import time
import requests

#Put your API key you got from the developer page in the space of 'YOUR KEY HERE'
MYKEY = '5622468da0a94df4a7bf18cc9912861b'
MYGT = 'sebastiencorps'
ALLGTS = 'GAMERTAG1,GAMERTAG2,GAMETAG3,GAMERTAG4' #make sure to keep it as one string and seperate GTs by a comma each

#This class raises exceptions caused by a non-200 response code from a request made
class i343Exception(Exception):
    def __init__(self, error, response):
        self.error = error
        self.headers = response.headers

    def __str__(self):
        return self.error

error_302 = 'Golden Path. The Location header should point at the corresponding emblem image.'
error_400 = 'An unsupported value was provided for a query string parameter.'
error_401 = 'Access denied.'
error_404 = 'Specified Title was not "h5"/Specified player gamertag was not found.'
error_500 = 'Internal Server Error'

def raise_status(response):
    if response.status_code == 302:
        raise i343Exception(error_302, response)
    elif response.status_code == 400:
        raise i343Exception(error_400, response)
    elif response.status_code == 401:
        raise i343Exception(error_401, response)
    elif response.status_code == 404:
        raise i343Exception(error_404, response)
    elif response.status_code == 500:
        raise i343Exception(error_500, response)
    else:
        response.raise_for_status()

#This class makes sure you are operating within your rate limit constraints. Technically it is not
#necessary, but without it you could hit the cap on 343's end accidentally and run the risk of your
#api key being suspended.
class RateLimit:
    def __init__(self, allowed_requests, seconds):
        self.allowed_requests = allowed_requests
        self.seconds = seconds
        self.made_requests = deque()

    def __reload(self):
        t = time.time()
        while len(self.made_requests) > 0 and self.made_requests[0] < t:
            self.made_requests.popleft()

    def add_request(self):
        self.made_requests.append(time.time() + self.seconds)

    def request_available(self):
        self.__reload()
        return len(self.made_requests) < self.allowed_requests

#The 3 different types of request and all their respective function calls are defined
#under this class. Any function arguments initialized as 'None' are disable unless an
#argument is given, meaning they are optional arguments to pass or not. Refer to the
#official documentation for further details.
class PiousAcademic(object):
    def __init__(self, title="h5", limits=(RateLimit(10,10), RateLimit(600,600))):
        self.title = title
        self.limits = limits

    def can_make_request(self):
        for lim in self.limits:
            if not lim.request_available():
                return False
            return True

    def meta_request(self, url, params={}, headers={'Ocp-Apim-Subscription-Key': MYKEY}):
        entries = {}
        for key, value in params.items():
            if key not in entries:
                entries[key] = value

        r = requests.get(
            'https://www.haloapi.com/metadata/{title}/metadata/{url}'.format(
                title=self.title,
                url=url),
            params = entries,
            headers = headers)
        for lim in self.limits:
            lim.add_request()
        raise_status(r)
        return r.json()

    def  get_campaign_missions(self):
        url = 'campaign-missions'
        return self.meta_request(url)

    def  get_commendations(self):
        url = 'commendations'
        return self.meta_request(url)

    def get_csr_designations(self):
        url = 'csr-designations'
        return self.meta_request(url)

    def get_enemies(self):
        url = 'enemies'
        return self.meta_request(url)

    def get_flexible_stats(self):
        url = 'flexible-stats'
        return self.meta_request(url)

    def get_game_base_variants(self):
        url = 'game-base-variants'
        return self.meta_request(url)

    def get_game_variants_by_id(self,  varID):
        url = 'game-variants/{id1}'.format(
            id1 = varID)
        return self.meta_request(url)

    def get_impulses(self):
        url = 'impulses'
        return self.meta_request(url)

    def get_maps_variants_by_id(self,  mapID):
        url = 'map-variants/{id1}'.format(
            id1 = mapID)
        return self.meta_request(url)

    def get_maps(self):
        url = 'maps'
        return self.meta_request(url)

    def get_medals(self):
        url = 'medals'
        return self.meta_request(url)

    def get_playlists(self):
        url = 'playlists'
        return self.meta_request(url)

    def get_requisition_packs_by_id(self, reqpackID):
        url = 'requisition-packs/{id1}'.format(
            id1 = reqpackID)
        return self.meta_request(url)

    def get_requisition_by_id(self, reqID):
            url = 'requisitions/{id1}'.format(
                id1 = reqID)
            return self.meta_request(url)

    def get_skulls(self):
        url = 'skulls'
        return self.meta_request(url)

    def get_spartan_ranks(self):
        url = 'spartan-ranks'
        return self.meta_request(url)

    def get_team_colors(self):
        url = 'team-colors'
        return self.meta_request(url)

    def get_vehicles(self):
        url = 'vehicles'
        return self.meta_request(url)

    def get_weapons(self):
        url = 'weapons'
        return self.meta_request(url)

    def profile_request(self, url, params={}, headers={'Ocp-Apim-Subscription-Key': MYKEY}):
        entries = {}
        for key, value in params.items():
            if key not in entries:
                entries[key] = value

        r = requests.get(
            'https://www.haloapi.com/profile/{title}/profiles/{url}'.format(
                title=self.title,
                url=url),
            params = entries,
            headers = headers,
        )
        for lim in self.limits:
            lim.add_request()
        raise_status(r)
        print(r)
        return r.json()

    def get_emblem_by_id(self, playerID, size=None):
        url = '{player}/emblem'.format(
            player = playerID)
        return self.profile_request(url,
                                    {'size':size})

    def get_profile_by_id(self, playerID, size=None, crop=None):
        url = '{player}/spartan'.format(
            player = playerID)
        return self.profile_request(url,
                                    {'size':size,
                                     'crop':crop})

    def stats_request(self, url, params={}, headers={'Ocp-Apim-Subscription-Key': MYKEY}):
        entries = {}
        for key, value in params.items():
            if key not in entries:
                entries[key] = value

            r = requests.get(
                'https://www.haloapi.com/stats/{title}/{url}'.format(
                    title=self.title,
                    url=url),
                params = entries,
                headers = headers
            )
            for lim in self.limits:
                lim.add_request()
            raise_status(r)
            return r.json()

    def get_matches_for_player(self, playerID, modes=None, start=None, count=None):
        url = 'players/{player}/matches'.format(player = playerID)
        return self.stats_request(url,
                                 {'modes':modes,
                                  'start':start,
                                  'count':count})

    def get_arena_match_by_id(self, matchID):
        url = 'arena/matches/{matchId}'.format(
            matchId = matchID)
        return self.stats_request(url)

    def get_campaign_match_by_id(self, matchID):
        url = 'campaign/matches/{matchId}'.format(
            matchId = matchID)
        return self.stats_request(url)

    def get_custom_match_by_id(self, matchID):
        url = 'custom/matches/{matchId}'.format(
            matchId = matchID)
        return self.stats_request(url)

    def get_warzone_match_by_id(self, matchID):
        url = 'warzone/matches/{matchId}'.format(
            matchId = matchID)
        return self.stats_request(url)

    def get_arena_servicerecord_for_players(self, playerIDs):
        url = 'servicerecords/arena'
        return self.stats_request(url,
                                  {'players':playerIDs})

    def get_campaign_servicerecord_for_players(self, playerIDs):
        url = 'servicerecords/campaign'
        return self.stats_request(url,
                                  {'players':playerIDs})

    def get_custom_servicerecord_for_players(self, playerIDs):
        url = 'servicerecords/custom'
        return self.stats_request(url,
                                  {'players':playerIDs})

    def get_warzone_servicerecord_for_players(self, playerIDs):
        url = 'servicerecords/warzone'
        return self.stats_request(url,
                                  {'players':playerIDs})
