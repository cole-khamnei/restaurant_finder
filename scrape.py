import io
import time
import requests

import matplotlib.pyplot as plt

from bs4 import BeautifulSoup as bsoup
from typing import Optional

try:
    get_ipython()
    from tqdm.notebook import tqdm
except NameError:
    from tqdm import tqdm

import constants

########################################################################################################################
### Constants ###
########################################################################################################################

########################################################################################################################
### utilities ###
########################################################################################################################


def safe_request(url: str, headers: dict = constants.REQUEST_HEADERS,
                 anti_dos_delay: float = constants.ANTI_DOS_DELAY):
    """"""
    time.sleep(anti_dos_delay)
    try:
        data = requests.get(url, headers=headers)
        return data
    except requests.exceptions.ConnectionError as e:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return requests.get(url, headers=headers, verify=False)


def get_image_data_from_url(image_url: str):
    """"""
    response = safe_request(image_url)
    image_bytes = io.BytesIO(response.content)
    return image_bytes


def generate_image_from_data(image_bytes, text: str = ""):
    """"""
    fig, ax = plt.subplots(figsize=(14, 2))
    a = plt.imread(image_bytes, format="jpg")
    ax.imshow(a)
    plt.axis('off')
#     ax2.text(-1000, 350, text, fontsize=14)
    buf = io.BytesIO()
    #         fig.tight_layout()
    fig.savefig(buf, format='png')
    buf.seek(0)
    restaurant_slide = buf.read()
    plt.close()
    
    return restaurant_slide


def google_search_html(search_phrase: str, anti_dos_delay: float = constants.ANTI_DOS_DELAY):
    """"""
    search_phrase = search_phrase.replace(" ", "+")
    url = constants.GOOGLE_SEARCH_URL_FORM.format(search_phrase=search_phrase)
    return bsoup(safe_request(url, anti_dos_delay=anti_dos_delay).content, "html.parser")


def get_google_rating(search_phrase: str, pbar: bool = True,
                      anti_dos_delay: float = constants.ANTI_DOS_DELAY) -> float:
    """"""
    if isinstance(search_phrase, str):
        try:
            soup = google_search_html(search_phrase, anti_dos_delay=anti_dos_delay)
            rating = float(soup.find_all("span", {"aria-hidden": "true"})[0].text)
            return rating

        except:
            return None
    else:
        if pbar:
            iterator = tqdm(search_phrase, unit=" Restaurant", desc="Fetching Google Reviews")
        else:
            iterator = search_phrase

        # return_array = []
        # for item in iterator:
        #     return_array.append(get_google_rating(item, anti_dos_delay=anti_dos_delay))

        # return return_array
        return [get_google_rating(item, anti_dos_delay=anti_dos_delay) for item in iterator]


########################################################################################################################
### Michelin Guide Scraping ###
########################################################################################################################


def get_michelin_guide_url(state: str, city: str, stars: Optional[str] = None) -> str:
    """"""
    state = state.lower().replace(" ", "-")
    if "new-york" in state:
        state = "new-york-state"
        
    city = city.lower().replace(" ", "-")
    
    if stars:
        stars = stars.replace("+", "-3")
        if "-" in stars:
            lower, upper = stars.split("-")
            stars = range(int(lower), int(upper) + 1)
        else:
            stars = [int(stars)]

        distinctions = ""
        for star in stars:
            if star == 0:
                distinctions += "/bib-gourmand"
            elif star == 1:
                distinctions += f"/{star}-star-michelin"
            else:
                distinctions += f"/{star}-stars-michelin"
            
    
    return constants.MICHELIN_GUIDE_URL_FORM.format(state=state, city=city) + distinctions


def get_michelin_guide_restaurant_html_list(state: str, city: str, stars: Optional[str] = None):
    """"""
    url = get_michelin_guide_url(state=state, city=city, stars=stars)
    
    req = safe_request(url)
    soup = bsoup(req.content, 'html.parser')
    total_restaurants = int(soup.find("div", {"class": constants.MICHELIN_GUIDE_HTML_CLASSES["total_restaurants"]}
                           ).text.split("of")[-1].split("Restaurants")[0].strip())
    
    if total_restaurants <= 0:
        raise ValueError("No restaurants found.")
    
    restaurant_list = soup.find_all("div", {"class": "col-md-6 col-lg-6 col-xl-3"})
    for page_index in range(2, total_restaurants // 20 + 2):
        req = safe_request(url + f"/page/{page_index}")
        if req.status_code != 200:
            break
        
        soup = bsoup(req.content, 'html.parser')
        restaurant_list += soup.find_all("div", {"class": constants.MICHELIN_GUIDE_HTML_CLASSES["restaurant"]})
    
    assert len(restaurant_list) == total_restaurants, \
           f"Incorrect number of restaurants found. Expected {len(total_restaurants)} but got {len(restaurant_list)}"
    
    return restaurant_list


class MichelinRestaurant:
    """"""
    def __init__(self, restaurant_html, distinctions_map: dict = constants.MICHELIN_HTML_DISTINCTIONS_MAP):
        self.distinction = distinctions_map[restaurant_html.find("i", {"class": "fa-michelin"}).text]
        
        self.restaurant_urls = restaurant_html.find_all("a")
        self.name = self.restaurant_urls[2]["aria-label"].lstrip("Open ")
        self.michelin_page_url = "https://guide.michelin.com/" + self.restaurant_urls[2]["href"]
        
        self.food_types = restaurant_html.find("div", {"class": "card__menu-footer--price pl-text"}).text
        self.food_types = sorted(set(self.food_types.strip().split(", ")))
        
        req = safe_request(self.michelin_page_url)
        full_page_html = bsoup(req.content, 'html.parser')
        restaurant_info = vars(full_page_html.find("ul", {"class": "restaurant-details__heading--list"}))["contents"]
        
        self.address = restaurant_info[1].text
        info_tokens = restaurant_info[3].text.replace(",", "").split()
        print(info_tokens)
        if info_tokens[3] == "USD":
            
            self.cost_str = f"${info_tokens[0]} - ${info_tokens[2]}"
            self.cost = int(info_tokens[2])
            self.food_types = info_tokens[5:]
        else:
            self.cost_str = f"${info_tokens[0]}"
            self.cost = int(info_tokens[0])
            self.food_types = info_tokens[3:]
            

        contact_info = full_page_html.find_all("a", {"class": "link js-dtm-link"})
        try:
            self.phone_number = contact_info[0].get("href", None).lstrip("tel:+1 ")
            self.website = contact_info[1].get("href", None)
        except:
            self.website = None
            self.phone_number = None
                
        self.google_rating = get_google_rating(f"{self.name}+nyc")
        self.image_url = restaurant_html.find_all("a")[0]["data-bg"]
        self.image_data = get_image_data_from_url(self.image_url)
        self.profile_image = generate_image_from_data(self.image_data, text=self.__repr__())
        
#     def __str__(self):
#         s = f"{self.name}\n"
#         s += f"{self.distinction}\n"
#         if self.google_rating:
#             s += f"{self.google_rating} Stars (Google Reviews)\n"
#         s += f"{self.cost_str}\n"
#         s += f"{', '.join(self.food_types)}\n"
#         s += f"{self.phone_number}\n"
#         s += f"{self.website}\n\n"
#         return s
    
    def __repr__(self):
        return f"{self.name} | {self.distinction} | {self.google_rating} Stars (Google Reviews)| {self.cost}"
    
    def __str__(self):
        return f"{self.name} | {self.distinction} | {self.google_rating} Stars (Google Reviews)| {self.cost}"
    
    def __lt__(self, other):
        return self.cost < other.cost
    
    def __le(self, other):
        return self.cost <= other.cost
    
#     def _repr_png_(self):
#         print(self.__repr__())
#         return self.profile_image


def get_convert_restaurant_html_list_to_restaurants(restaurant_html_list: list):
    """"""
    desc = "Collecting Restaurant Information"
    iterator = tqdm(restaurant_html_list, desc=desc, unit=" Restaurant")
    return [MichelinRestaurant(restaurant_html) for restaurant_html in iterator]


########################################################################################################################
### End ###
########################################################################################################################
