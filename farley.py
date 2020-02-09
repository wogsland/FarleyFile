import click
import json
import os


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


@click.group()
def cli():
    click.echo('Hello World!')
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


cli.add_command(detail)
cli.add_command(list)
cli.add_command(search)


if __name__ == '__main__':
    cli()
