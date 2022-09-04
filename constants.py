########################################################################################################################
### Constants ###
########################################################################################################################

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko)'
    ' Chrome/39.0.2171.95 Safari/537.36'
}
ANTI_DOS_DELAY = 0.1
GOOGLE_SEARCH_URL_FORM = "https://www.google.com/search?q={search_phrase}"


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
### End ###
########################################################################################################################
