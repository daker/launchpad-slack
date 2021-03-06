# -*- coding: utf-8 -*-

import os

SLACK_USERNAME = "Launchpad"
SLACK_CHANNEL = "#random"
SLACK_ICON_URL = "https://launchpadlibrarian.net/50084288/launchpad-logo"

for key in os.environ:
    if key[:6] == 'SLACK_':
        globals()[key] = os.environ[key]
