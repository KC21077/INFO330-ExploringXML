import sqlite3
import sys
import xml.etree.ElementTree as ET

connection = sqlite3.connect('pokemon.sqlite')
cursor = connection.cursor()
# Incoming Pokemon MUST be in this format
#
# <pokemon pokedex="" classification="" generation="">
#     <name>...</name>
#     <hp>...</name>
#     <type>...</type>
#     <type>...</type>
#     <attack>...</attack>
#     <defense>...</defense>
#     <speed>...</speed>
#     <sp_attack>...</sp_attack>
#     <sp_defense>...</sp_defense>
#     <height><m>...</m></height>
#     <weight><kg>...</kg></weight>
#     <abilities>
#         <ability />
#     </abilities>
# </pokemon>



# Read pokemon XML file name from command-line
# (Currently this code does nothing; your job is to fix that!)
if len(sys.argv) < 2:
    print("Usage: python Import.py [pokedex.xml]")

for i, arg in enumerate(sys.argv):
    # Skip if this is the Python filename (argv[0])
    if i == 0:
        continue

tree = ET.parse('pokedex.xml')
root = tree.getroot()

#Extract data from pokemon xml and put it into the database
for pokemon in root:
    pokedex = pokemon.get('pokedexNumber')
    classification = pokemon.get('classification')
    generation = pokemon.get('generation')
    name = pokemon.find('name').text
    hp = pokemon.find('hp').text
    types = [t.text for t in pokemon.findall('type')]
    attack = pokemon.find('attack').text
    defense = pokemon.find('defense').text
    speed = pokemon.find('speed').text
    sp_attack = pokemon.find('sp_attack').text
    sp_defense = pokemon.find('sp_defense').text
    height = pokemon.find('height/m').text
    weight = pokemon.find('weight/kg').text
    abilities = [a.text for a in pokemon.findall('abilities/ability')]

    cursor.execute('SELECT name FROM Pokemon WHERE name = ?', (name,))
    row = cursor.fetchone()
    if row is not None:
        print(f'{name} is already in the database')
        continue

cursor.execute('''INSERT INTO imported_pokemon_data (pokedex_number, classfication, generation, name, hp, type1, type2, attack, defense, speed, sp_attack, sp_defense, height_m, weight_kg)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (pokedex, classification, generation, name, hp, types[0], types[1] if len(types) > 1 else None, attack, defense, speed, sp_attack, sp_defense, height, weight))
pokemon_id = cursor.lastrowid

for ability in abilities:
    cursor.execute('INSERT INTO imported_pokemon_data (pokedex_number, abilities) VALUES (?, ?)', (pokemon_id, ability))

print(f'{name} inserted into the database')

connection.commit()
connection.close()
