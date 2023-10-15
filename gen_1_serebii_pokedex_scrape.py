# Imports
import requests
from bs4 import BeautifulSoup as bs
import json

# List with the name of the necessary stats
stats_list = ['hp', 'attack', 'defense', 'special', 'speed']

# Initiate the pokedex variable
pokedex = dict()

# Loop over all pokemon from gen 1
for num in range(1, 152):

  # The links require leading zeroes
  if len(str(num)) == 1:
    pkmn_num = '00'+str(num)
  
  elif len(str(num)) == 2:
    pkmn_num = '0'+str(num)
  
  else:
    pkmn_num = str(num)

  # Build the URL
  pkmn_url = 'https://serebii.net/pokedex/' + pkmn_num + '.shtml'

  # Retrieve the page
  r = requests.get(pkmn_url)

  # Parse it
  soup = bs(r.content, 'html.parser')

  # Get the elements with the relevant information
  dex_divs = soup.find_all("table", {"class": "dextable"})

  # Instantiate a pokemon dictionary
  pokemon = {
    'name':           None,
    'typing':         [],
    'classification': None,
    'height':         None,
    'weight':         None,
    'capture_rate':   None,
    'hp':             None,
    'attack':         None,
    'defense':        None,
    'special':        None,
    'speed':          None
  }

  # Loop through the children of that element
  for child_idx in [3, 7]:
    if child_idx == 3:
      
      for child_idx_2 in [1, 7]:

        if child_idx_2 == 1:
          pokemon['name'] = dex_divs[1].contents[child_idx].contents[child_idx_2].text
        
        else:
          for pkmn_type in dex_divs[1].contents[child_idx].contents[child_idx_2].find_all('a'):
            pokemon['typing'].append(pkmn_type.attrs['href'][len('/pokedex/'):-len('.shtml')])

    elif child_idx == 7:

      for details_idx in range(len(dex_divs[1].contents[child_idx].find_all('td'))):

        if details_idx == 0:
          pokemon['classification'] = dex_divs[1].contents[child_idx].find_all('td')[details_idx].text
        
        elif details_idx == 1:
          height = str(dex_divs[1].contents[child_idx].find_all('td')[details_idx])
          pokemon['height'] = height[height.find('<br/>')+len('<br/>'):-len('</td>')].strip()

        elif details_idx == 2:
          weight = str(dex_divs[1].contents[child_idx].find_all('td')[details_idx])
          pokemon['weight'] = weight[weight.find('<br/>')+len('<br/>'):-len('</td>')].strip()

        elif details_idx == 3:
          # Prevent the differences between RB and Y to appear
          if '(RB)' in dex_divs[1].contents[child_idx].find_all('td')[details_idx].text:
            capture_rate_cell = dex_divs[1].contents[child_idx].find_all('td')[details_idx].text
            pokemon['capture_rate'] = int(capture_rate_cell[:capture_rate_cell.find('(RB)')].strip())

          # Get the capture rate immediately
          else:
            pokemon['capture_rate'] = int(dex_divs[1].contents[child_idx].find_all('td')[details_idx].text)


  # Get the stats information parent element
  stats_div = soup.find('a', {'name':'stats'}).next_element
  
  # Get the table data of the stats
  stats_table_data = stats_div.find_all('td', { 'class': 'fooinfo', 'align': 'center' })

  # Loop through the indices of the elements of the stats list to retrieve each of them
  for stat_idx in range(len(stats_list)):
    pokemon[stats_list[stat_idx]] = int(stats_table_data[stat_idx].text)

  # Add the pokemon to the pokedex
  pokedex[pkmn_num] = pokemon

  print(pkmn_num)

  # Destroy the parsed element to free memory
  soup.decompose()

# Store the pokedex as a JSON
with open("pokedex.json", "w") as f:
  json.dump(pokedex, f)