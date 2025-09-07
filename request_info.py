import requests
import armor_finder_constants as constants
import os
import json

RESPONSE_JSON_KEY = "Response"
VERSION_JSON_KEY = "version"

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
    
    Manifest structure:
	
    { Response : {
			{ version : "version_string" }
    	}
    }
    
    """
    up_to_date = True # used to check if the manifest is up to date
    request_url = f"{constants.BASE} + {constants.MANIFEST_URL}" # endpoint for fetching the Bungie API manifest

    try:
        response = requests.get(request_url, headers=constants.REQUEST_HEADERS, timeout=10)
        response.raise_for_status()
        remote_manifest = response.json()

        # check if the manifest file exists.
        if os.path.exists(constants.MANIFEST_FILENAME):
            
            #if file exists, load it from local storage
            with open(constants.MANIFEST_FILENAME, "r") as f:
                local_manifest = json.load(f) # load manifest json
                print("Manifest loaded from local storage")
                
            # if the local manifest version is not equal to the remote version 
            if local_manifest.get(RESPONSE_JSON_KEY, {}).get(VERSION_JSON_KEY) != remote_manifest.get(RESPONSE_JSON_KEY, {}).get(VERSION_JSON_KEY):
                # print version differences
                print(f"Local manifest version diff from remote. Updating manifest")
                print(f"Local version: {local_manifest.get(RESPONSE_JSON_KEY, {}).get(VERSION_JSON_KEY)}")
                print(f"Remote version: {remote_manifest.get(RESPONSE_JSON_KEY, {}).get(VERSION_JSON_KEY)}")

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