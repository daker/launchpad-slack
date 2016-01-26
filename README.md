# launchpad-slack

Launchpad offers online source code hosting for Git & Bazaar projects, with powerful collaboration tools, code review, and bugs tracking.

This integration will post commits, merge requests to a channel in Slack.

## Setting up a Incoming WebHook in Slack
Go to the [Incoming WebHooks](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) app, and make sure you generate Webhook URL to the channel where you want the messages to go, it looks something like the following url :

```https://hooks.slack.com/services/XXXXXXX/YYYYYYYY/ZZZZZZZZZZZZZZZZZ```

## Deploying to Heroku

```sh
$ git clone git@github.com:daker/launchpad-slack.git
$ cd launchpad-slack
$ heroku create
$ git push heroku master
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

Once the app is deployed, under your app settings you need to add ```SLACK_INCOMING_WEBHOOKS``` to the Config Variables section which will hold the Slack Incoming WebHook you generated before, finally make sure you restart the app.

## Setting up a webhook in Launchpad
Copy the heroku app url, then go to your branch page in Launchpad.net, click on "Manage webhooks" then "Add webhook" and finally make sure the url looks something like the following :

```https://<HEROKU_APP_NAME>.herokuapp.com/webhook```

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request