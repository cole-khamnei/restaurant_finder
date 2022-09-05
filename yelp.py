import requests
import time

import pandas as pd

try:
    get_ipython()
    from tqdm.notebook import tqdm
except NameError:
    from tqdm import tqdm

import constants

########################################################################################################################
### Constants ###
########################################################################################################################


def get_restaurants(term: str, location: str = constants.YELP_DEFAULT_LOCATION, **params: dict):
    """
    suggested search terms:
    
    radius: in meters
    limit: max items to return (max value is 50)
    offset: list offset number
    sort_by: best_match, rating, review_count or distance
    price: 1 = $, 2 = $$, 3 = $$$, 4 = $$$$, example: 1,2,4
    
    """
    url_form = constants.YELP_API_HOST + constants.YELP_SEARCH_PATH + "?"
    url_form = f"{url_form}?term={term}&location={location}"
    for key, value in params.items():
        url_form += f"&{key}={value}"

    req = requests.request('GET', url_form, headers=constants.YELP_REQUEST_HEADER)
    time.sleep(1.1)
    return req


def get_all_restaurants(term: str, location: str = constants.YELP_DEFAULT_LOCATION, top=None, offset: int = 0,
                        per_price: bool = True, **params: dict):
    """"""
    limit = 50
    
    assert "limit" not in params and "offset" not in params
    top = min(999, top)

    if per_price:
        assert "price" in params
        prices = params.pop("price").split(",")

        pbar = tqdm(total=top * len(prices), unit=" restaurants", desc="Gathering Restaurant Data")
        data = get_all_restaurants(term, location, top=top, offset=offset, per_price=False,
                                   price=prices[0], pbar=pbar, **params)
        for price in prices[1:]:
            price_data = get_all_restaurants(term, location, top=top, offset=offset, per_price=False,
                                             price=price, pbar=pbar, **params)
            data["businesses"] += price_data["businesses"]

        pbar.close()
        return data

    params["limit"] = limit
    params["offset"] = offset
    restaurant_data = get_restaurants(term, location=location, **params).json()
    total_restaurants = restaurant_data["total"]
    
    if total_restaurants == 0:
        raise ValueError("No restaurants found.")
    
    if total_restaurants < limit:
        return restaurant_data

    n_fetched = len(restaurant_data["businesses"])

    max_index = (top - n_fetched) // limit if top else (total_restaurants - n_fetched) // limit
    
    if "pbar" in params:
        pbar = params.pop("pbar")
        pbar.update(limit)
    else:
        pbar = tqdm(total=max_index * limit, unit=" restaurants", desc="Gathering Restaurant Data")
    
    for pull_index in range(max_index):
        params["offset"] += limit
        additional_restaurant_data = get_restaurants(term, location=location, **params).json()
        if len(additional_restaurant_data) == 0:
            break

        restaurant_data["businesses"] += additional_restaurant_data["businesses"]
        pbar.update(limit)
    
    return restaurant_data


def yelp_data_to_restaurant_df(data: dict) -> pd.DataFrame:
    """"""
    columns = ['name', 'review_count', 'rating', 'id', 'alias', "price"]

    restaurant_list = []
    for restaurant in data["businesses"]:
        row = [restaurant[key] for key in columns]
        row.append(", ".join(item["title"] for item in restaurant["categories"]))
        row.append(", ".join(restaurant["location"]["display_address"]))
        row.append(restaurant["location"]["city"])
        restaurant_list.append(row)

    return pd.DataFrame(restaurant_list, columns=columns + ["categories", "address", "city"])

########################################################################################################################
### End ###
########################################################################################################################
