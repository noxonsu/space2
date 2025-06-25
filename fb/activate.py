import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CERT = os.getenv("CERT") # Not used for Cloud API, but kept for reference
NUMBER = os.getenv("NUMBER")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
WHATSAPP_BUSINESS_ACCOUNT_ID = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID")
PIN = "555666" # User provided PIN

if not ACCESS_TOKEN or not WHATSAPP_BUSINESS_ACCOUNT_ID or not NUMBER or not PIN:
    print("Error: ACCESS_TOKEN, WHATSAPP_BUSINESS_ACCOUNT_ID, NUMBER, or PIN not found/provided.")
    exit(1)

# Extract country code and phone number
# Assuming NUMBER is in format "+CC XXXXXXXXXX"
# The Cloud API register endpoint uses the phone_number_id, not cc and phone_number directly.
# We will use the NUMBER to verify against the retrieved phone numbers.
cc = NUMBER.split(' ')[0][1:] if ' ' in NUMBER else NUMBER[1:3] # Example: +91 2250323060 -> 91, +1234567890 -> 12
phone_number_without_cc = "".join(NUMBER.split(' ')[1:]) if ' ' in NUMBER else NUMBER[3:] # Example: +91 2250323060 -> 2250323060, +1234567890 -> 234567890

BASE_URL = "https://graph.facebook.com/v23.0" # Using v23.0 as per documentation example

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Step 1: Get Phone Number ID
print(f"Attempting to retrieve phone number ID for WABA ID: {WHATSAPP_BUSINESS_ACCOUNT_ID}")
get_phone_numbers_endpoint = f"{BASE_URL}/{WHATSAPP_BUSINESS_ACCOUNT_ID}/phone_numbers"

phone_number_id = None
try:
    response = requests.get(get_phone_numbers_endpoint, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(f"Get Phone Numbers Response: {data}")

    for phone_obj in data.get("data", []):
        # The display_phone_number might be formatted differently, so we need to normalize for comparison
        display_phone_number_normalized = phone_obj.get("display_phone_number", "").replace(" ", "").replace("-", "").replace("+", "")
        
        # Compare with the number from .env, removing '+' and spaces
        env_number_normalized = NUMBER.replace(" ", "").replace("+", "")

        if display_phone_number_normalized == env_number_normalized:
            phone_number_id = phone_obj.get("id")
            print(f"Found matching phone number ID: {phone_number_id} for number: {NUMBER}")
            break
    
    if not phone_number_id:
        print(f"Error: Could not find phone number ID for {NUMBER} under WABA ID {WHATSAPP_BUSINESS_ACCOUNT_ID}.")
        exit(1)

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred while getting phone numbers: {http_err}")
    print(f"Response body: {response.text}")
    exit(1)
except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred while getting phone numbers: {conn_err}")
    exit(1)
except requests.exceptions.Timeout as timeout_err:
    print(f"Timeout error occurred while getting phone numbers: {timeout_err}")
    exit(1)
except requests.exceptions.RequestException as req_err:
    print(f"An unexpected error occurred while getting phone numbers: {req_err}")
    exit(1)

# Step 2: Register Phone Number
print(f"Attempting to register phone number with ID: {phone_number_id}")
register_endpoint = f"{BASE_URL}/{phone_number_id}/register"

payload = {
    "messaging_product": "whatsapp",
    "pin": PIN
}

try:
    response = requests.post(register_endpoint, headers=headers, json=payload)
    response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")

    if response.json().get("success"):
        print(f"Phone number {NUMBER} successfully registered with Cloud API.")
    else:
        print(f"Phone number registration failed. Response: {response.json()}")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred during registration: {http_err}")
    print(f"Response body: {response.text}")
except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred during registration: {conn_err}")
except requests.exceptions.Timeout as timeout_err:
    print(f"Timeout error occurred during registration: {timeout_err}")
except requests.exceptions.RequestException as req_err:
    print(f"An unexpected error occurred during registration: {req_err}")
