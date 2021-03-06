# Contributing

Contributions welcome!

### Roadmap

The current tasks on the roadmap include

1. Interface to create/view/edit files
1. File validation
1. File import
1. Deduping/merging
1. Google contacts import
1. Twitter import - WIP
1. LinkedIn import - WIP
1. Facebook import
1. Instagram import (is this even possible?)
1. Strava import (is this even possible?) - WIP
1. Tumblr import
1. Store files on S3 instead
1. Import a previous export
1. Executable packaging
1. Ability to `brew install` packaged executable

### Testing

The tests can be run simply with

   pytest

### Linting

Linting can be done with flake8:

    flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude=venv

### Maintainer

1. [Bradley Wogsland](https://github.com/wogsland)
