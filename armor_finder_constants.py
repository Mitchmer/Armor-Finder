from dotenv import load_dotenv, find_dotenv
import os
import secrets

load_dotenv(find_dotenv()) # load the .env file

#**********************************************
# GLOBAL CONSTANTS
#**********************************************

#******************************
# API VARS
#******************************

# Base endpoint for any request
BASE = "https://www.bungie.net"	

# Key variables
API_KEY = os.getenv("BUNGIE_API_KEY") # Needed for API requests
#REQUEST_HEADERS = {"X-API-Key": API_KEY} # Also required in API requests

# User-specific
MEMBERSHIP_ID = os.getenv("MEMBERSHIP_ID") # Membership ID for current profile
MEMBERSHIP_TYPE = os.getenv("MEMBERSHIP_TYPE") # Membership type for current profile

# OAuth Requests
STATE = secrets.token_urlsafe(16)
CLIENT_ID = os.getenv("OAUTH_CLIENT_ID")
CLIENT_SECRET = ""
AUTH_URL = f"{BASE}/en/oauth/authorize?client_id={CLIENT_ID}&response_type=code&state={STATE}"
REDIRECT_PORT = 5000
REDIRECT_DOMAIN = f"https://localhost:{REDIRECT_PORT}"
REDIRECT_URL = f"{REDIRECT_DOMAIN}/callback"
TOKEN_URL = f"{BASE}/platform/app/oauth/token"

# Endpoint for Bungie manifest
MANIFEST_URL = "/Platform/Destiny2/Manifest/" 

# Constructs a request endpoint for the user's profile 
MEMBERSHIP_URL = "/Platform/User/GetMembershipsForCurrentUser/"


#**********************
# JSON key/values
#**********************
"""
Manifest Structure

{ Response : {
        { version : "version_string" }
    }
}
"""
RESPONSE_JSON_KEY = "Response"
VERSION_JSON_KEY = "version"

#******************************
# JSON Paths
#******************************

# Stores the last manifest pulled
MANIFEST_FILENAME = "Manifest.json"

# Stores a "Lite" version of item info. *** STILL VERY LARGE ***
INVENTORY_ITEM_LITE_DEFINITION_FILENAME = "DestinyInventoryItemLiteDefinition.json"

TOKEN_FILENAME = "token.json"
MEMBERSHIP_FILENAME = "membership.json"