import requests
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
RAPIDAPI_KEY = ""
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

# Get house listings for the specified location
listings = get_zillow_listings(location)
print(listings)

# Process the listings and extract required data
house_data = []
for listing in listings['props']:
    zpid = listing['zpid']
    address = listing['address']
    price = listing['price']
    bedrooms = listing['bedrooms']
    bathrooms = listing['bathrooms']
    living_area = listing['livingArea']
    property_type = listing['propertyType']
    price_per_sqft = price / living_area

    house_data.append([zpid, address, price, bedrooms, bathrooms, living_area, property_type, price_per_sqft])

# Write the listings to the Google Sheet
range_name = '48307!A1'
header = [['zpid', 'Address', 'Price', 'Bedrooms', 'Bathrooms', 'Living Area', 'Property Type', 'PP Sqft']]
body = {'values': header + house_data}
result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=range_name, valueInputOption='RAW', body=body).execute()