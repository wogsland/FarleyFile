# Integrations

Integration credentials are stored in `.env`, which can be created by

    cp .env-example .env

and the adding your specific credentials. Details on obtaining those credentials for the various integrations can be found below.

### Github

Get your [Github access token](https://github.com/settings/tokens) from the settings and add it to `.env`. Then simply

    farley github

to import your contacts from Github.

### LinkedIn - WIP

Set up your credentials [here](https://www.linkedin.com/developers/apps). This integration is incomplete. [Contributions](CONTRIBUTING.md) welcome!

### Strava - WIP

Follow the [API getting started guide](https://developers.strava.com/docs/getting-started/) provided by Strava to get your access token. This integration is incomplete. [Contributions](CONTRIBUTING.md) welcome!

### Twitter - WIP

Create a [Twitter App](https://apps.twitter.com/) and go to "Keys and tokens" for that app to obtain the four credentials needed. After adding these to the app then

    farley twitter

but if you have thousands of of connections like me then rate limits will kill you pretty quickly. That's why this is listed as a work in progress. [Contributions](CONTRIBUTING.md) welcome!
