# -*- coding: utf-8 -*-

import os

SLACK_USERNAME = "Launchpad"
SLACK_CHANNEL = "#random"
SLACK_ICON_URL = "https://launchpadlibrarian.net/50084288/launchpad-logo"
SLACK_PROJECT_NAME = "Launchpad Slack"

for key in os.environ:
    if key[:3] == 'SLACK_':
        name = key[3:]
        globals()[name] = os.environ[key]
