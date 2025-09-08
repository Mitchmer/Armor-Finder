import requests
import armor_finder_constants as constants
import os
import json
from flask import Flask, request, redirect # Flask web framework utilities
import webbrowser # To automatically open the login page

app = Flask(__name__)

def begin_app():
    print(f"➡ Starting local server on {constants.REDIRECT_DOMAIN} ...")
    print("➡ Opening browser to Bungie login page ...")

    # test if token has expired
    response = test_response()
    if response is False:
        print("Token expired. Requesting new token")
        # Open the root route in the browser (which redirects to Bungie login)
        webbrowser.open(f"{constants.REDIRECT_DOMAIN}")

        # Run Flask with HTTPS (adhoc self-signed certificate)
        app.run(ssl_context="adhoc", port=constants.REDIRECT_PORT)
    else:
        # TODO: BEGIN THE REQUESTENING AND THE PARSENING
        print("BEGIN THE REQUESTENING AND THE PARSENING") 


def request_memberships(token):
    headers = {
        "Authorization" : f"Bearer {token.get("access_token")}",
        "X-API-Key" : constants.API_KEY     
    }
    membership_response = requests.get(
        f"{constants.BASE}{constants.MEMBERSHIP_URL}",
        headers=headers,
        timeout=10
    )

    # check response for expired token
    if (membership_response.ok): # status_code is less than 400
        # then the rest of the stuff happens

        membership = membership_response.json()

        print("***** MEMBERSHIP RESPONSE ******")
        print(membership_response)
        print(membership)
        with open(constants.MEMBERSHIP_FILENAME, "w") as f:
            json.dump(membership, f)
            print("Saved membership to local")

    return membership_response.ok


def test_response():
    test_successful = False
    if (os.path.exists(constants.TOKEN_FILENAME)):
        with open(constants.TOKEN_FILENAME, "r") as f:
            token = json.load(f)
            print("Loaded local token")
        test_successful = request_memberships(token) 
    return test_successful


@app.route("/")
def index():
    """
    Root route: immediately redirects the user to Bungie's OAuth authorization page.
    Visiting https://localhost:5000 in a browser kicks off the login flow.
    """
    return redirect(constants.AUTH_URL)


@app.route("/callback")
def callback():
    """
    Callback route: Bungie redirects here after user login and consent.
    The URL will contain ?code=...&state=...
    """
    # Extract query parameters from Bungie's redirect
    code = request.args.get("code")
    state = request.args.get("state")

    # Verify the returned state matches what we generated earlier
    if state != constants.STATE:
        return "State mismatch! Possible CSRF attack.", 400

    # Verify we actually got an authorization code
    if not code:
        return "No authorization code received.", 400

    print(f"\n✅ Received authorization code: {code}")

    # Exchange the authorization code for access/refresh tokens
    token_response = requests.post(
        constants.TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": constants.CLIENT_ID
            # TODO "client_secret": CLIENT_SECRET,       # Remove if using Public client
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    token = token_response.json()
    with open(constants.TOKEN_FILENAME, "w") as f:
        json.dump(token, f)
        print("Saved token to local")
    
    #print("\n=== Token Response ===")
    #print(tokens)

    # Extract the access token from the response
    access_token = token.get("access_token")

    #if access_token:

        # >>> This is where you can call your own functions instead of (or in addition to) the sample API call <<<
        # For example:
        # my_app_logic(tokens, api_response.json())

    # Send a response to the browser so the user knows we're done
    return "<h1>Authorization complete. You can close this tab.</h1>"


def request_manifest():
    """
    Requests the Bungie API manifest. This also checks whether or not
    the local manifest is up-to-date with the remote, current API
    manifest. The result of this check can be used by the rest of the
    application (for use in something such as determining whether or
    not to pull a massive JSON file).
    
    :param args: can be a list of arguments, all that matters is that
        when concatenated they form a complete API request for the
        manifest.
    :return: returns a JSON object for query.
    """
    up_to_date = True # used to check if the manifest is up to date
    request_url = f"{constants.BASE}{constants.MANIFEST_URL}" # endpoint for fetching the Bungie API manifest

    try:
        headers = { "X-API-Key" : constants.API_KEY }
        response = requests.get(request_url, headers=headers, timeout=10)
        response.raise_for_status()
        remote_manifest = response.json()

        # check if the manifest file exists.
        if os.path.exists(constants.MANIFEST_FILENAME):
            
            #if file exists, load it from local storage
            with open(constants.MANIFEST_FILENAME, "r") as f:
                local_manifest = json.load(f) # load manifest json
                print("Manifest loaded from local storage")
                
            # if the local manifest version is not equal to the remote version 
            if local_manifest.get(constants.RESPONSE_JSON_KEY, {}).get(constants.VERSION_JSON_KEY) != remote_manifest.get(constants.RESPONSE_JSON_KEY, {}).get(constants.VERSION_JSON_KEY):
                # print version differences
                print(f"Local manifest version diff from remote. Updating manifest")
                print(f"Local version: {local_manifest.get(constants.RESPONSE_JSON_KEY, {}).get(constants.VERSION_JSON_KEY)}")
                print(f"Remote version: {remote_manifest.get(constants.RESPONSE_JSON_KEY, {}).get(constants.VERSION_JSON_KEY)}")

                # open file for writing
                with open(constants.MANIFEST_FILENAME, "w") as f:
                    # noinspection PyTypeChecker
                    json.dump(remote_manifest, f) # write json to local manifest
                local_manifest = remote_manifest # set remote manifest as local manifest
                up_to_date = False # set flag to signal manifest was not up-to-date
            
        # if the manifest doesn't exist, create it and save the manifest that was fetched 
        else:
            print("Local manifest not found. Saving API manifest")
            with open(constants.MANIFEST_FILENAME, "w") as f:
                json.dump(remote_manifest, f) # write json to file
            local_manifest = remote_manifest # set the local manifest as the remote one

    except requests.exceptions.Timeout:
        raise RuntimeError("⏳ Bungie API timed out while fetching manifest metadata.")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"❌ Bungie API returned HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"⚠️ Network error while fetching manifest metadata: {e}")
    except (json.JSONDecodeError, KeyError) as e:
        raise RuntimeError(f"⚠️ Could not parse manifest metadata: {e}")

    # return the manifest (whether new or old) and whether or not the version was up-to-date
    return local_manifest, up_to_date


