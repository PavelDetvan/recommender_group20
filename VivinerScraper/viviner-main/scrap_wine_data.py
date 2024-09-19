import json
import sys
import pandas as pd

import utils.constants as c
from utils.requester import Requester


if __name__ == '__main__':
    # Gathers the input arguments and its variables
    output_file = 'scraped_wine.csv'
    start_page = 1

    

    # Instantiates a wrapper over the `requests` package
    r = Requester(c.BASE_URL)

    # Defines the payload, i.e., filters to be used on the search at least one is needed for the api
    payload = {
        "country_codes[]": "br",
        # "min_rating": 0,
    }

    # Performs an initial request to get the number of records (wines)
    res = r.get('explore/explore?', params=payload)
    n_matches = res.json()['explore_vintage']['records_matched']

    print(f'Number of matches: {n_matches}')

    # Create an empty list to store all wine data
    wine_data = []

    # Iterates through the amount of possible pages
    for i in range(start_page, max(1, int(n_matches / c.RECORDS_PER_PAGE)) + 1):
        # Adds the page to the payload
        payload['page'] = i

        print(f'Page: {payload["page"]}')

        # Performs the request and scraps the URLs
        res = r.get('explore/explore', params=payload)
        matches = res.json()['explore_vintage']['matches']

        # Iterates over every match
        for match in matches:

            '''
            # Wine based data
            wine_id = wine['vintage']['wine']['id']
            winery_name = wine['vintage']['wine']['winery']['name']
            wine_title = wine['vintage']['wine']['name']
            vintage_year = wine['vintage']['year']

            # Reviews based data
            rating = wine['vintage']['statistics']['ratings_average']
            num_reviews = wine['vintage']['statistics']['ratings_count']
            
            #Type              0
            #Elaborate         0
            #Grapes            0
            #Harmonize         0
            #ABV               0
            #Body              0
            #Acidity           0
            #Code              0
            #Country           0
            #RegionID          0
            #RegionName        0
            #WineryID          0
            #Vintages          0

            # Store the relevant details
            wine_data.append({
                "WineID": wine_id,
                "WineryName": winery_name,
                "WineName": wine_title,
                "Year": vintage_year,
                "Rating": rating,
                "Number of Reviews": num_reviews
            })
            '''

            # Gathers the wine-based data
            wine = match['vintage']['wine']

            print(f'wine data: {wine}')

            # Gathers the full-taste profile from current match
            res = r.get(f'wines/{wine["id"]}/tastes')
            tastes = res.json()
            wine['taste'] = tastes['tastes']

            print(f'taste data: {tastes}')

            sys.exit(0)
        
    # Convert the list of wine data to a DataFrame
    df = pd.DataFrame(wine_data)

    # Save the DataFrame to a CSV file
    df.to_csv(output_file, index=False)

    print(f'Data saved to {output_file}')