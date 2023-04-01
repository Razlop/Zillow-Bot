import requests
import os
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set up Google Sheets API credentials

# Path to Service Key
SERVICE_ACCOUNT_FILE = 'propertyvision-381813-860b0e15663b.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# ID is located here in the URL = https://docs.google.com/spreadsheets/d/spreadsheetId
SPREADSHEET_ID = '1I5UxZFOrAeTwaLb45SARNli2uLgrlmQ8EvLYAfh6QYs'

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE).with_scopes(SCOPES)
service = build('sheets', 'v4', credentials=creds)
# Set up RapidAPI Zillow API credentials
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
location = '48307'


# Define the function to get house listings from Zillow
def get_zillow_listings(location):
    url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
    querystring = {"location": location, "home_type": "Houses"}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()

def get_sold_zillow_listings(location):
    url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
    querystring = {"location": location, "status_type":"RecentlySold", "home_type": "Houses"}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()

def write_to_google_sheet(sheet_name, house_data):
    range_name = f'{sheet_name}!A1'
    header = [['zpid', 'Address', 'Price', 'Bedrooms', 'Bathrooms', 'Living Area', 'Lot Area', 'Property Type', 'PP Sqft', 'Images']]
    body = {'values': header + house_data}
    result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=range_name, valueInputOption='RAW', body=body).execute()

# Get house listings for the specified location
listings = get_zillow_listings(location)
sold_listings = get_sold_zillow_listings(location)

def get_zillow_images(zpid):
    url = "https://zillow-com1.p.rapidapi.com/images"
    querystring = {"zpid": zpid}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response)
    return response.json()

# Process the listings and extract required data
def process_listings(listings_data):
    house_data = []
    for listing in listings_data['props']:
        zpid = listing['zpid']
        address = listing['address']
        price = listing['price']
        bedrooms = listing['bedrooms']
        bathrooms = listing['bathrooms']
        living_area = listing['livingArea']
        lot_area = listing['lotAreaValue']
        property_type = listing['propertyType']
        price_per_sqft = price / living_area

        # images_data = get_zillow_images(zpid)
        # images = ','.join(images_data['images']) if 'images' in images_data else 'No images'

        house_data.append([zpid, address, price, bedrooms, bathrooms, living_area, lot_area, property_type, price_per_sqft, images])

        # Add 1 second time delay due to api limits (api limits 2 requests per second)
        time.sleep(1)

    return house_data

house_data = process_listings(listings)
sold_house_data = process_listings(sold_listings)

# Write the listings to the Google  Sheet
write_to_google_sheet("48307", house_data)
write_to_google_sheet("48307SOLD", sold_house_data)