"""Module for data transformations and internal conventions"""

TEAM_TRANSLATIONS = {
    "Tigers": "Richmond",
    "Blues": "Carlton",
    "Demons": "Melbourne",
    "Giants": "GWS",
    "Suns": "Gold Coast",
    "Bombers": "Essendon",
    "Swans": "Sydney",
    "Magpies": "Collingwood",
    "Kangaroos": "North Melbourne",
    "Crows": "Adelaide",
    "Bulldogs": "Western Bulldogs",
    "Dockers": "Fremantle",
    "Power": "Port Adelaide",
    "Saints": "St Kilda",
    "Eagles": "West Coast",
    "Lions": "Brisbane",
    "Cats": "Geelong",
    "Hawks": "Hawthorn",
    "Adelaide Crows": "Adelaide",
    "Brisbane Lions": "Brisbane",
    "Gold Coast Suns": "Gold Coast",
    "GWS Giants": "GWS",
    "Geelong Cats": "Geelong",
    "West Coast Eagles": "West Coast",
    "Sydney Swans": "Sydney",
}

# I used this dictionary to convert betting venue names to match venue names
# for the sake of joining the two data sets, but no longer use venues to join them.
# It was a pain to put this together, though, so I'm keeping it around in case I need
# it later.
# VENUE_TRANSLATIONS = {
#     "AAMI": "AAMI Stadium",
#     "ANZ": "ANZ Stadium",
#     "Adelaide": "Adelaide Oval",
#     "Aurora": "UTAS Stadium",
#     "Aurora Stadium": "UTAS Stadium",
#     "Blacktown": "Blacktown International",
#     "Blundstone": "Blundstone Arena",
#     "Cazaly's": "Cazaly's Stadium",
#     "Domain": "Domain Stadium",
#     "Etihad": "Etihad Stadium",
#     "GMHBA": "GMHBA Stadium",
#     "Gabba": "Gabba",
#     "Jiangwan": "Jiangwan Stadium",
#     "MCG": "MCG",
#     "Mars": "Mars Stadium",
#     "Metricon": "Metricon Stadium",
#     "Perth": "Optus Stadium",
#     "SCG": "SCG",
#     "Spotless": "Spotless Stadium",
#     "StarTrack": "Manuka Oval",
#     "TIO": "TIO Stadium",
#     "UTAS": "UTAS Stadium",
#     "Westpac": "Westpac Stadium",
#     "TIO Traegar Park": "TIO Stadium",
# }

CITIES = {
    "Adelaide": {"state": "SA", "lat": -34.9285, "long": 138.6007},
    "Sydney": {"state": "NSW", "lat": -33.8688, "long": 151.2093},
    "Melbourne": {"state": "VIC", "lat": -37.8136, "long": 144.9631},
    "Geelong": {"state": "VIC", "lat": -38.1499, "long": 144.3617},
    "Perth": {"state": "WA", "lat": -31.9505, "long": 115.8605},
    "Gold Coast": {"state": "QLD", "lat": -28.0167, "long": 153.4000},
    "Brisbane": {"state": "QLD", "lat": -27.4698, "long": 153.0251},
    "Launceston": {"state": "TAS", "lat": -41.4332, "long": 147.1441},
    "Canberra": {"state": "ACT", "lat": -35.2809, "long": 149.1300},
    "Hobart": {"state": "TAS", "lat": -42.8821, "long": 147.3272},
    "Darwin": {"state": "NT", "lat": -12.4634, "long": 130.8456},
    "Alice Springs": {"state": "NT", "lat": -23.6980, "long": 133.8807},
    "Wellington": {"state": "NZ", "lat": -41.2865, "long": 174.7762},
    "Euroa": {"state": "VIC", "lat": -36.7500, "long": 145.5667},
    "Yallourn": {"state": "VIC", "lat": -38.1803, "long": 146.3183},
    "Cairns": {"state": "QLD", "lat": -6.9186, "long": 145.7781},
    "Ballarat": {"state": "VIC", "lat": -37.5622, "long": 143.8503},
    "Shanghai": {"state": "CHN", "lat": 31.2304, "long": 121.4737},
    "Albury": {"state": "NSW", "lat": -36.0737, "long": 146.9135},
}

TEAM_CITIES = {
    "Adelaide": "Adelaide",
    "Brisbane": "Brisbane",
    "Carlton": "Melbourne",
    "Collingwood": "Melbourne",
    "Essendon": "Melbourne",
    "Fitzroy": "Melbourne",
    "Western Bulldogs": "Melbourne",
    "Fremantle": "Perth",
    "GWS": "Sydney",
    "Geelong": "Geelong",
    "Gold Coast": "Gold Coast",
    "Hawthorn": "Melbourne",
    "Melbourne": "Melbourne",
    "North Melbourne": "Melbourne",
    "Port Adelaide": "Adelaide",
    "Richmond": "Melbourne",
    "St Kilda": "Melbourne",
    "Sydney": "Sydney",
    "University": "Melbourne",
    "West Coast": "Perth",
}

VENUE_CITIES = {
    "Football Park": "Adelaide",
    "S.C.G.": "Sydney",
    "Windy Hill": "Melbourne",
    "Subiaco": "Perth",
    "Moorabbin Oval": "Melbourne",
    "M.C.G.": "Melbourne",
    "Kardinia Park": "Geelong",
    "Victoria Park": "Melbourne",
    "Waverley Park": "Melbourne",
    "Princes Park": "Melbourne",
    "Western Oval": "Melbourne",
    "W.A.C.A.": "Perth",
    "Carrara": "Gold Coast",
    "Gabba": "Brisbane",
    "Docklands": "Melbourne",
    "York Park": "Launceston",
    "Manuka Oval": "Canberra",
    "Sydney Showground": "Sydney",
    "Adelaide Oval": "Adelaide",
    "Bellerive Oval": "Hobart",
    "Marrara Oval": "Darwin",
    "Traeger Park": "Alice Springs",
    "Perth Stadium": "Perth",
    "Stadium Australia": "Sydney",
    "Wellington": "Wellington",
    "Lake Oval": "Melbourne",
    "East Melbourne": "Melbourne",
    "Corio Oval": "Geelong",
    "Junction Oval": "Melbourne",
    "Brunswick St": "Melbourne",
    "Punt Rd": "Melbourne",
    "Glenferrie Oval": "Melbourne",
    "Arden St": "Melbourne",
    "Olympic Park": "Melbourne",
    "Yarraville Oval": "Melbourne",
    "Toorak Park": "Melbourne",
    "Euroa": "Euroa",
    "Coburg Oval": "Melbourne",
    "Brisbane Exhibition": "Brisbane",
    "North Hobart": "Hobart",
    "Bruce Stadium": "Canberra",
    "Yallourn": "Yallourn",
    "Cazaly's Stadium": "Cairns",
    "Eureka Stadium": "Ballarat",
    "Blacktown": "Sydney",
    "Jiangwan Stadium": "Shanghai",
    "Albury": "Albury",
}

TEAM_NAMES = sorted(["Fitzroy", "University"] + list(set(TEAM_TRANSLATIONS.values())))
ROUND_TYPES = ["Finals", "Regular"]
VENUES = list(set(VENUE_CITIES.keys()))
INDEX_COLS = ["team", "year", "round_number"]
SEED = 42
AVG_SEASON_LENGTH = 23
CATEGORY_COLS = ["team", "oppo_team", "round_type", "venue"]
