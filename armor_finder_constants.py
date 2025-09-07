from dotenv import load_dotenv
import os

#**********************************************
# GLOBAL CONSTANTS
#**********************************************

#******************************
# API VARS
#******************************

# Key variables
API_KEY = os.getenv("BUNGIE_API_KEY") # Needed for API requests
REQUEST_HEADERS = {"X-API-Key": API_KEY} # Also required in API requests

# User-specific
MEMBERSHIP_ID = os.getenv("MEMBERSHIP_ID") # Membership ID for current profile
MEMBERSHIP_TYPE = os.getenv("MEMBERSHIP_TYPE") # Membership type for current profile

#**********************
# Bungie API endpoints
#**********************

# Base endpoint for any request
BASE = "https://www.bungie.net"	

# Endpoint for Bungie manifest
MANIFEST_URL = "/Platform/Destiny2/Manifest/" 

# Constructs a request endpoint for the user's profile 
PROFILE_URL = f"/Platform/Destiny2/{MEMBERSHIP_TYPE}/Profile/{MEMBERSHIP_ID}/" 

#******************************
# JSON Paths
#******************************

# Stores the last manifest pulled
MANIFEST_FILENAME = "Manifest.json"

 #Stores a "Lite" version of item info. *** STILL VERY LARGE ***
INVENTORY_ITEM_LITE_DEFINITION_FILENAME = "DestinyInventoryItemLiteDefinition.json"