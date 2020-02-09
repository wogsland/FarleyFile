import click
import json
import os

@click.group()
def cli():
    click.echo('Hello World!')
    pass

@click.command()
def list():
    click.echo('Listing People...')
    for fileName in os.listdir('files'):
        if '.gitignore' == fileName:
            continue
        with open('files/{}'.format(fileName), 'r') as file:
            person = json.load(file)
            click.echo('{} {} {}'.format(person['id'], person['firstName'], person['lastName']))

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

cli.add_command(list)
cli.add_command(detail)

if __name__ == '__main__':
    cli()
