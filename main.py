from dotenv import load_dotenv
import os
import requests
import json

"""
===============================================================
Destiny 2 Armor Finder
===============================================================
Programmer: Mitch Merrell
Date Created: 09/07/2025
===============================================================
This program is a tool which enables users to automatically
pull their inventory information and find missing and better
armor pieces from various "sets" and "archetypes," resulting
in a Destiny Item Manager (DIM) query for easy locating.
===============================================================
Algorithm 
==========
	1. query Bungie API
		- log in if needed?
	2. check manifest for new information
		- if new, update the manifest and the "item definition"
			json files with the newest files
	3. pull user's information
	4. TODO: enable user to customize the sets they want
		- for now, just pull from Techsec
	5. TODO: enable user to customize the archetypes they want
		- for now, just use "Gunner" and "Paragon" archetypes
	6. For each armor slot (helmet, gauntlets, etc):
		a. Go through each "archetype":
			i. Find the highest "base stat total":
				- add it to the user's armor pool
===============================================================
"""




def main():
	print("Hello!")

if __name__ == "__main__":
	main()