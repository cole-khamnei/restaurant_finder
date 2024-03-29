import private_constants

########################################################################################################################
### Constants ###
########################################################################################################################

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko)'
    ' Chrome/39.0.2171.95 Safari/537.36'
}
ANTI_DOS_DELAY = 0.1

MICHELIN_GUIDE_URL_FORM = "https://guide.michelin.com/us/en/{state}/{city}/restaurants"

MICHELIN_GUIDE_HTML_CLASSES = {
    "total_restaurants": "flex-fill search-results__stats js-restaurant__stats pl-text pl-big",
    "restaurant": "col-md-6 col-lg-6 col-xl-3"
}

MICHELIN_HTML_DISTINCTIONS_MAP = {
    "m": "1 Star",
    "n": "2 Stars",
    "o": "3 Stars",
    "=": "Bib Gourmand"
}

########################################################################################################################
### yelp constants ###
########################################################################################################################

YELP_API_HOST = 'https://api.yelp.com'
YELP_SEARCH_PATH = '/v3/businesses/search'
YELP_BUSINESS_PATH = '/v3/businesses/'

YELP_DEFAULT_LOCATION = 'NYC'
SEARCH_LIMIT = 3

YELP_REQUEST_HEADER = {
    'Authorization': f'Bearer {private_constants.YELP_API_KEY}',
}

########################################################################################################################
### Google constants ###
########################################################################################################################

GOOGLE_SEARCH_URL_FORM = "https://www.google.com/search?q={search_phrase}"
GOOGLE_PLACE_FIELDS = ["name", "business_status", "place_id", "price_level",
                       "rating", "user_ratings_total"]

GOOGLE_PLACE_EMPTY = {field: None for field in GOOGLE_PLACE_FIELDS}

########################################################################################################################
### End ###
########################################################################################################################
