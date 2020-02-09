import json
import sys

if len(sys.argv) != 2:
    print('detail should only have 1 argument')
    exit()

with open('files/{}.json'.format(str(sys.argv[1])), 'r') as file:
    person = json.load(file)
    for key in person.keys():
        print('{}: {}'.format(key, str(person[key])))
