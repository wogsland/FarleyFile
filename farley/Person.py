import json
import os


class Person():
    def __init__(self, id):
        'Initialization'
        self.id = id
        self.json = None
        self.fileName = None
        fileName = 'files/{}.json'.format(id)
        if os.path.isfile(fileName) is True:
            self.fileName = fileName
            with open(self.fileName, 'r') as file:
                self.json = json.load(file)

    def addEmail(self, email):
        'Adds an email to the connection'
        if 'email' in self.json:
            if email != self.json['email']:
                self.json['emails'] = [
                    self.json['email'],
                    email
                ]
                self.json.pop('email')
                with open(self.fileName, 'w') as file:
                    json.dump(self.json, file, indent=2)
        elif 'emails' in self.json:
            found = False
            for testEmail in self.json['emails']:
                if email == testEmail:
                    found = True
            if found is False:
                self.json['emails'].append(email)
                with open(self.fileName, 'w') as file:
                    json.dump(self.json, file, indent=2)
        else:
            self.json['email'] = email
            with open(self.fileName, 'w') as file:
                json.dump(self.json, file, indent=2)
