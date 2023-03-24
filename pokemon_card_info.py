import requests
import json
import argparse

# Set up command line arguments
parser = argparse.ArgumentParser(description='Retrieve Pokemon card data from the API')
parser.add_argument('-t', '--type', choices=['Fire', 'Grass'], default='Fire', help='The type of the card (default: Fire)')
parser.add_argument('-hp', '--min-hp', type=int, default=90, help='The minimum HP of the card (default: 90)')
parser.add_argument('-r', '--rarity', default='Rare', help='The rarity of the card (default: Rare)')
parser.add_argument('-l', '--limit',default='Specify amount of records needed', help='no of records')

# Parse command line arguments
args = parser.parse_args()

# Set up query parameters
query_params = {
    'types': args.type,
    'hp': f'gte{args.min_hp}',
    'rarity': args.rarity,
    'orderBy': 'id',
}

# Make the API request
response = requests.get('https://api.pokemontcg.io/v2/cards', params=query_params)

# Check for errors
if response.status_code != 200:
    print(f"Error: {response.status_code} {response.reason}")
    exit(1)

# Parse the JSON data
cards = response.json()['data']

# Format the output
output = []

for card in cards:
    if 'types' in card.keys(): 
        if 'Fire' or 'Grass' in card['types'] and int(card['hp']) >=90:
            if isinstance(card['id'],int):
                output.append({
                'id': card['id'],
                'name': card['name'],
                'type': card['types'][0],
                'hp': card['hp'],
                'rarity': card['rarity'],
            })

    if len(output) == 10:
        break

# Print the output as JSON
print(json.dumps(output, indent=2))
