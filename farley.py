# -*- coding: utf-8 -*-
import click
import json
import os
import twitter as twitterAPI

from datetime import date
from FarleyFile import Person, Files
from linkedin_v2 import linkedin as linkedinAPI
from github import Github
#from stravaio import StravaIO # was 0.0.9


def getFileNames():
    'This function gets the filenames of the people files'
    files = Files()
    return files.getFileNames()


def printListing(person):
    'This function prints a one line listing of a person'
    listing = '{} <name omitted>'.format(person['id'])
    if 'firstName' in person and 'lastName' in person:
        listing = '{} {} {}'.format(person['id'], person['firstName'], person['lastName'])
    elif 'firstName' in person:
        listing = '{} {} <last name omitted>'.format(person['id'], person['firstName'])
    elif 'lastName' in person:
        listing = '{} <first name omitted> {}'.format(person['id'], person['lastName'])
    click.echo(listing)


def readEnvironment():
    'This function reads in the environment variables from a file if needed'
    click.echo('reading environment variables...')
    if os.path.isfile('.env') is True:
        with open('.env', 'r') as file:
            for line in file:
                if line.startswith('#'):
                    continue
                # Remove leading `export `
                # then, split name / value pair
                key, value = line.split('=', 1)
                os.environ[key] = value[:-1]


@click.command(help='Allows for addition to a specific person')
@click.option('--id', help='ID of the person to add to', prompt=True)
@click.option('--field', help='Field to add', prompt=True)
@click.option('--value', help='Value to add to the field', prompt=True)
def add(id, field, value):
    click.echo('Adding details to person...')
    person = Person(id)
    if 'email' == field:
        click.echo('Adding email {} to {}...'.format(value, person.json['firstName']))
        person.addEmail(value)
    else:
        click.echo('Unfortunately adding to {} is not supported at this time'.format(field))


@click.command(help='Allows for addition to a specific person')
def dupes():
    click.echo('Gathering potential duplicates (first/last name matches)...')
    for fileName1 in getFileNames():
        for fileName2 in getFileNames():
            if fileName1 != fileName2:
                with open('files/{}'.format(fileName1), 'r') as file1:
                    with open('files/{}'.format(fileName2), 'r') as file2:
                        person1 = json.load(file1)
                        person2 = json.load(file2)
                        if person1['firstName'] == person2['firstName'] and person1['lastName'] == person2['lastName']:
                            print('Potential duplicates:')
                            printListing(person1)
                            printListing(person2)

@click.group()
def cli():
    click.echo('FarleyFile processing...')
    readEnvironment()
    pass


@click.command(help='Lists all the attributes of a given user')
@click.option('--id', help='ID of the person to get details for', prompt=True)
def detail(id):
    click.echo('Listing Details')
    fileName = 'files/{}.json'.format(str(id))
    if os.path.isfile(fileName) is False:
        click.echo('Please chose a valid ID')
        exit()
    with open(fileName, 'r') as file:
        person = json.load(file)
        for key in person.keys():
            click.echo('{}: {}'.format(key, str(person[key])))


@click.command(help='Exports all the connections to a single file')
@click.option('--path', default=None, help='Optional path for the export', prompt=False)
@click.option('--indent', default=2, help='Optional json indentation', prompt=False)
def export(path, indent):
    click.echo('Exporting Files...')
    if path is None:
        filePath = 'export.json'
    else:
        filePath = '{}/export.json'.format(path)
    indent = int(indent)
    export = {
        'connections': []
    }
    for fileName in getFileNames():
        with open('files/{}'.format(fileName), 'r') as file:
            personRecord = json.load(file)
            click.echo('exporting file {}'.format(personRecord['id']))
            export['connections'].append(personRecord)
    with open(filePath, 'w') as file:
        json.dump(export, file, indent=indent)


@click.command(help='Imports users you are following from Github')  # noqa: C901
@click.option('--token', default=None, help='The Github access token', prompt=False, envvar='GITHUB_ACCESS_TOKEN')
def github(token):
    click.echo('Getting Github...')
    client = Github(str(token))

    for follower in client.get_user().get_following():
        # Assemble person information
        note = 'Following on Github as of {}'.format(date.today())
        notes = [note]
        github = follower.login
        github_url = follower.html_url
        firstName = None
        lastName = None
        person = {
            'github': github,
            'githubUrl': github_url,
            'notes': notes
        }
        if follower.name is not None:
            names = follower.name.split(' ')
            if len(names) > 0:
                firstName = names[0]
                person['firstName'] = firstName
            if len(names) > 1:
                names.pop(0)
                lastName = ' '.join(names)
                person['lastName'] = lastName

        # match person information or create new
        match = None
        fileNames = getFileNames()
        for fileName in fileNames:
            with open('files/{}'.format(fileName), 'r') as file:
                personRecord = json.load(file)
                matchesGithub = False
                matchesGithubUrl = False
                matchesName = False
                if 'github' in personRecord:
                    matchesGithub = (personRecord['github'] == person['github'])
                if 'githubUrl' in personRecord:
                    matchesGithubUrl = (personRecord['githubUrl'] == person['githubUrl'])
                if 'firstName' in personRecord and 'firstName' in person:
                    matchesFirstName = (personRecord['firstName'] == person['firstName'])
                if 'lastName' in personRecord and 'lastName' in person:
                    matchesLastName = (personRecord['lastName'] == person['lastName'])
                matchesName = matchesFirstName and matchesLastName
                if matchesGithub or matchesGithubUrl or matchesName:
                    match = fileName
                    updated = False
                    updates = ''
                    if 'github' not in personRecord:
                        updates = updates + 'adding github '
                        personRecord['github'] = person['github']
                        updated = True
                    if 'githubUrl' not in personRecord:
                        updates = updates + 'adding githubUrl '
                        personRecord['githubUrl'] = person['githubUrl']
                        updated = True
                    if 'firstName' not in personRecord and 'firstName' in person:
                        updates = updates + 'adding firstName '
                        personRecord['firstName'] = person['firstName']
                        updated = True
                    if 'lastName' not in personRecord and 'lastName' in person:
                        updates = updates + 'adding lastName '
                        personRecord['lastName'] = person['lastName']
                        updated = True
                    if 'notes' not in personRecord:
                        updates = updates + 'adding notes '
                        personRecord['notes'] = person['notes']
                        updated = True
                    elif note not in personRecord['notes']:
                        updates = updates + 'adding note '
                        personRecord['notes'].append(note)
                        updated = True
                    if updated:
                        click.echo('updating match ({}): {} ({})'.format(updates, match, follower.login))
                        with open('files/{}'.format(fileName), 'w') as file:
                            json.dump(personRecord, file, indent=2)

        if match is None:
            id = str(len(fileNames) + 1)
            fileName = 'files/{}.json'.format(id)
            person['id'] = id
            click.echo('no match for {} adding {}'.format(follower.login, fileName))
            with open(fileName, 'w') as file:
                json.dump(person, file, indent=2)


@click.command(help='WIP - Import all your connections from LinkedIn')
def linkedin():
    click.echo('Getting LinkedIn...')
    authentication = linkedinAPI.LinkedInDeveloperAuthentication(
        os.environ['LINKEDIN_CONSUMER_KEY'],
        os.environ['LINKEDIN_CONSUMER_SECRET'],
        os.environ['LINKEDIN_USER_TOKEN'],
        os.environ['LINKEDIN_USER_SECRET'],
        'https://github.com/wogsland/FarleyFile',
        linkedinAPI.PERMISSIONS.enums.values())
    application = linkedinAPI.LinkedInApplication(authentication)
    print(application.get_profile())


@click.command(help='Lists all your connections')
def list():
    click.echo('Listing People...')
    for fileName in getFileNames():
        with open('files/{}'.format(fileName), 'r') as file:
            person = json.load(file)
            printListing(person)


@click.group(help='Commands for interacting with a person record')
def person():
    click.echo('Person processing...')
    pass


@click.command(help='Lists all the connections matching a given search term')
@click.option('--name', help='Name to search for', prompt=True)
def search(name):
    click.echo('Searching People')
    for fileName in getFileNames():
        with open('files/{}'.format(fileName), 'r') as file:
            person = json.load(file)
            firstNameMatch = 'firstName' in person and name.lower() in person['firstName'].lower()
            middleNameMatch = 'middleName' in person and name.lower() in person['middleName'].lower()
            lastNameMatch = 'lastName' in person and name.lower() in person['lastName'].lower()
            if firstNameMatch or middleNameMatch or lastNameMatch:
                printListing(person)


#@click.command(help='WIP - imports Strava connections')
#@click.option('--token', help='The Strava access token', prompt=True)
#def strava(token):
#    click.echo('Getting Strava...')
#    client = StravaIO(access_token=token)
#    athlete = client.get_logged_in_athlete().to_dict()
#    for key in athlete.keys():
#        click.echo('{}: {}'.format(key, str(athlete[key])))


@click.command(help='WIP - imports Twitter connections')
def twitter():
    click.echo('Getting Twitter...')
    print('key: {}'.format(os.environ['TWITTER_API_ACCESS_TOKEN']))
    client = twitterAPI.Api(consumer_key=os.environ['TWITTER_API_KEY'],
                            consumer_secret=os.environ['TWITTER_API_SECRET_KEY'],
                            access_token_key=os.environ['TWITTER_API_ACCESS_TOKEN'],
                            access_token_secret=os.environ['TWITTER_API_ACCESS_TOKEN_SECRET'])
    # click.echo(client)
    # cred = client.VerifyCredentials()
    # click.echo(cred)
    # user = client.GetUser('wogsland')
    # token = client.GetAppOnlyAuthToken(consumer_key=os.environ['TWITTER_API_KEY'],
    #                     consumer_secret=os.environ['TWITTER_API_SECRET_KEY'])
    # click.echo(token)

    if os.path.isfile('temp.txt') is False:
        print('no temp file exists')
        rl = client.rate_limit
        print(rl.get_limit('friends/ids'))
        friends = client.GetFriendIDs(screen_name='wogsland')
        with open('temp.txt', 'w') as file:
            file.write(','.join([str(friend) for friend in friends]))
    with open('temp.txt', 'r') as file:
        users = file.read().split(',')
    twitterId = users[1]
    user = client.GetUser(twitterId)
    twitterName = user.name
    twitterHandle = user.screen_name
    print('{} name: {} handle: {}'.format(twitterId, twitterName, twitterHandle))


cli.add_command(detail)
cli.add_command(export)
cli.add_command(github)
# cli.add_command(linkedin)
cli.add_command(list)
cli.add_command(person)
cli.add_command(search)
# cli.add_command(strava)
# cli.add_command(twitter)

person.add_command(add)
person.add_command(dupes)

if __name__ == '__main__':
    cli()
