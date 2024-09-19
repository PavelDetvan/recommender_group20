import requests
import pandas as pd

# Load your dataset (assuming it's a CSV with a column 'Wine Name')
wine_dataset = pd.read_csvwines_df = pd.read_csv("All-XWines_Full_100K_wines_21M_ratings\XWines_Full_100K_wines.csv")
wine_names = wine_dataset['WineName'].tolist()

# Define a function to search for wines by name and fetch details
def search_wine_by_name(wine_name):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
    }
    wine_name = wine_name.replace(" ", "-")
    search_url = f"https://www.vivino.com/api/explore/explore?currency_code=USD&q={wine_name}&page=1"

    print(f"Request URL: {search_url}")
    
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for wine: {wine_name}")
        print(f"Status Code: {response.status_code}")

        return None

# Create an empty list to store wine details
wine_details_list = []

# Iterate over the wine names and fetch their details
for wine_name in wine_names:
    result = search_wine_by_name(wine_name)
    
    if result and 'explore_vintage' in result:
        # Assuming you want the first match in the result
        for wine in result['explore_vintage']['matches']:
            wine_id = wine['vintage']['wine']['id']
            winery_name = wine['vintage']['wine']['winery']['name']
            wine_title = wine['vintage']['wine']['name']
            vintage_year = wine['vintage']['year']
            rating = wine['vintage']['statistics']['ratings_average']
            num_reviews = wine['vintage']['statistics']['ratings_count']
            
            # Store the relevant details
            wine_details_list.append({
                "Wine ID": wine_id,
                "Winery": winery_name,
                "Wine": wine_title,
                "Year": vintage_year,
                "Rating": rating,
                "Number of Reviews": num_reviews
            })

# Create a DataFrame from the collected wine details
wine_details_df = pd.DataFrame(wine_details_list)

# Save the DataFrame to a CSV file
wine_details_df.to_csv('fetched_wine_details.csv', index=False)
