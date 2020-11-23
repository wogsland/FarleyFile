FarleyFile
==========

<a href="https://github.com/wogsland/FarleyFile/actions"><img alt="GitHub Actions status" src="https://github.com/wogsland/FarleyFile/workflows/Python%20package/badge.svg"></a>

The name here comes from a practice Eisenhower had of keeping an information file on everybody he knew so that he could review it before interacting with them. There's a lot of information out there on the web about the people we know, and the aim of this project is to help people reclaim control of the data regarding the people that they know and store it in a single place.

## Setup

FarleyFile is a command line tools for keeping track of your contacts.

    virtualenv venv
    . venv/bin/activate
    pip3 install -r requirements.txt
    pip3 install --editable .

You can begin either by starting to create files on your own or importing your contacts from one of the social media platforms that supports such data exports. Check out the [integrations](INTEGRATIONS.md). To see all the available commands just type

    farley --help

## Importing

The idea to integrate with all major social media platforms, but currently only Github and Twitter are supported. More information on the [integrations page](INTEGRATIONS.md).

## Deduping & Merging - WIP

If you import from a number of social media platforms then merging duplicate contacts will be required and there should functionality to do this automagically but for now we have

    farley person dupes

to list out everybody with a matching first and last name.

## Searching

Basic search functionality is provided with

    farley search

### Maintainer

1. [Bradley Wogsland](https://github.com/wogsland)

## Issues

If you run into an issue, you can file it [here](https://github.com/wogsland/FarleyFile/issues/new).

## Contributing

Contributions are welcome! Check out our [contributing page](CONTRIBUTING.md).

## License

This is a tool for anyone to use and so I've licensed it under the [MIT license](LICENSE.md).

<img src="https://upload.wikimedia.org/wikipedia/commons/f/f8/Dwight_D._Eisenhower_as_General_of_the_Army_crop.jpg" alt="I like Ike" width="300"/>
