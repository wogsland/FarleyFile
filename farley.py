import click
import json
import os
import twitter as twitterAPI

from datetime import date
from github import Github
from stravaio import StravaIO


def getFileNames():
    'This function gets the filenames of the people files'
    fileNames = os.listdir('files')
    fileNames.remove('.gitignore')
    return fileNames


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
    'This function reads in the environment variables form a file if needed'
    if os.path.isfile('.env') is True:
        with open('.env', 'r') as file:
            for line in file:
                if line.startswith('#'):
                    continue
                # Remove leading `export `
                # then, split name / value pair
                key, value = line.split('=', 1)
                os.environ[key] = value[:-1]


@click.group()
def cli():
    click.echo('FarleyFile processing...')
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


@click.command(help='Imports users you are following from Github')
@click.option('--token', default=None, help='The Github access token', prompt=False, envvar='GITHUB_ACCESS_TOKEN')
def github(token):
    click.echo('Getting Github...')
    client = Github(str(token))

    i = 0
    for follower in client.get_user().get_following():
        #print('{} ({})'.format(follower.login, follower.name))

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
        if None != follower.name:
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
                if 'firstName' in personRecord and 'firstName' in person and 'lastName' in personRecord and 'lastName' in person:
                    matchesName = (personRecord['firstName'] == person['firstName'] and personRecord['lastName'] == person['lastName'])
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


        if None == match:
            id = str(len(fileNames) + 1)
            fileName = 'files/{}.json'.format(id)
            person['id'] = id
            click.echo('no match for {} adding {}'.format(follower.login, fileName))
            with open(fileName, 'w') as file:
                json.dump(person, file, indent=2)


@click.command(help='Lists all your connections')
def list():
    click.echo('Listing People...')
    for fileName in getFileNames():
        with open('files/{}'.format(fileName), 'r') as file:
            person = json.load(file)
            printListing(person)


@click.command(help="Lists all the connections matching a given search term")
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

@click.command(help="WIP")
@click.option('--token', help='The Strava access token', prompt=True)
def strava(token):
    click.echo('Getting Strava...')
    client = StravaIO(access_token=token)
    athlete = client.get_logged_in_athlete().to_dict()
    for key in athlete.keys():
        click.echo('{}: {}'.format(key, str(athlete[key])))


@click.command(help="WIP")
def twitter():
    click.echo('Getting Twitter...')
    print('key: {}'.format(os.environ['TWITTER_API_ACCESS_TOKEN']))
    client = twitterAPI.Api(consumer_key=os.environ['TWITTER_API_KEY'],
                         consumer_secret=os.environ['TWITTER_API_SECRET_KEY'],
                         access_token_key=os.environ['TWITTER_API_ACCESS_TOKEN'],
                         access_token_secret=os.environ['TWITTER_API_ACCESS_TOKEN_SECRET'])
    click.echo(client)
    cred = client.VerifyCredentials()
    click.echo(cred)
    #user = client.GetUser('wogsland')
    #token = client.GetAppOnlyAuthToken(consumer_key=os.environ['TWITTER_API_KEY'],
    #                     consumer_secret=os.environ['TWITTER_API_SECRET_KEY'])
    #click.echo(token)
    #friends = client.GetFriends()
    #for friend in friends:
    #    click.echo(friend.name)


cli.add_command(detail)
cli.add_command(github)
cli.add_command(list)
cli.add_command(search)
cli.add_command(strava)
cli.add_command(twitter)


if __name__ == '__main__':
    readEnvironment()
    cli()
