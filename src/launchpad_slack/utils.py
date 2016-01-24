# -*- coding: utf-8 -*-
from launchpadlib.launchpad import Launchpad

import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

statuses = ["Unknown", "Invalid", "Opinion", "Won't Fix", "Fix Released",
            "Fix Committed", "New", "Incomplete", "Confirmed", "Triaged", "In Progress"]
severities = ["Unknown", "Undecided", "Wishlist",
              "Low", "Medium", "High", "Critical"]


def lp_login(lp_instance='production'):
    cachedir = os.path.join(PROJECT_PATH, 'lp_cache')
    client_ident = "Launchpad Slack"
    try:
        launchpad = Launchpad.login_anonymously(
            client_ident, lp_instance, cachedir)
    except:
        return None
    return launchpad


def _sort(task1, task2):
    task1_status = task1.status
    task1_importance = task1.importance
    task2_status = task2.status
    task2_importance = task2.importance

    if task1_status not in statuses:
        print("%r is an unknown status for Launchpad" % task1_status)
        if task2_status not in statuses:
            print("%r is an unknown status for Launchpad" % task1_status)
            return -1
        return 1

    if task1_importance not in severities:
        print("%r is an unknown status for Launchpad." % task1_importance)
        if task2_importance not in severities:
            print("%r is an unknown status for Launchpad." % task1_importance)
            return -1
        return 1

    if task1_status != task2_status:
        if statuses.index(task1_status) < statuses.index(task2_status):
            return -1
        return 1
    if task1_importance != task2_importance:
        if severities.index(task1_importance) < severities.index(task2_importance):
            return -1
        return 1
    return 0
