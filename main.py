import requests
import xml.etree.ElementTree as ET
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set up Google Sheets API credentials
SERVICE_ACCOUNT_FILE = 'path/to/your/service_account_key.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = 'your_spreadsheet_id'

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, SCOPES)
service = build('sheets', 'v4', credentials=creds)

# Define the function to fetch house listings from Zillow
def fetch_zillow_listings(zipcode, api_key):
    url = f"http://www.zillow.com/webservice/GetSearchResults.htm?zws-id={api_key}&address=&citystatezip={zipcode}"
    response = requests.get(url)
    root = ET.fromstring(response.content)

    house_data = []
    for result in root.findall('.//result'):
        try:
            address = result.find('./address/street').text
            zipcode = result.find('./address/zipcode').text
            city = result.find('./address/city').text
            state = result.find('./address/state').text
            zestimate = result.find('./zestimate/amount').text
            house_data.append([address, city, state, zipcode, zestimate])
        except AttributeError:
            continue
    return house_data

# Fetch house listings for the specified ZIP code
ZIPCODE = '48307'
API_KEY = 'YOUR_ZILLOW_API_KEY'
listings = fetch_zillow_listings(ZIPCODE, API_KEY)

# Write the listings to the Google Sheet
range_name = 'Sheet1!A1'
body = {'values': [['Address', 'City', 'State', 'ZIP Code', 'Zestimate']] + listings}
result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=range_name, valueInputOption='RAW', body=body).execute()
