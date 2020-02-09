import click
import json
import os
import twitter as twitterAPI

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
                os.environ[key] = value


@click.group()
def cli():
    click.echo('FarleyFile processing...')
    pass


@click.command()
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


@click.command()
def list():
    click.echo('Listing People...')
    for fileName in getFileNames():
        with open('files/{}'.format(fileName), 'r') as file:
            person = json.load(file)
            printListing(person)


@click.command()
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

@click.command()
@click.option('--token', help='The Strava access token', prompt=True)
def strava(token):
    click.echo('Getting Strava...')
    client = StravaIO(access_token=token)
    athlete = client.get_logged_in_athlete().to_dict()
    for key in athlete.keys():
        click.echo('{}: {}'.format(key, str(athlete[key])))


@click.command()
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
cli.add_command(list)
cli.add_command(search)
cli.add_command(strava)
cli.add_command(twitter)


if __name__ == '__main__':
    readEnvironment()
    cli()
