from pyapi.PiousAcademic16807 import PiousAcademic as PA

api = PA()
MYKEY = '5622468da0a94df4a7bf18cc9912861b'
MYGT = 'sebastiencorps'
print(api.get_matches_for_player(MYGT))
