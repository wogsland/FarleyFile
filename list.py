import json
import os

for fileName in os.listdir('files'):
    if '.gitignore' == fileName:
        continue
    with open('files/{}'.format(fileName), 'r') as file:
        person = json.load(file)
        print('{} {} {}'.format(person['id'], person['firstName'], person['lastName']))
