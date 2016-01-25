# -*- coding: utf-8 -*-

from flask import Flask, request, Response, redirect
from utils import lp_login, _sort
import settings

import os
import simplejson
import requests

app = Flask(__name__)

ALLOWED_EVENTS = [
    'bzr:push:0.1',
    'git:push:0.1',
    'merge-proposal:0.1',
]

COLORS_RED = '#e74c3c'
COLORS_green = '#2ecc71'
COLORS_blue = '#3498db'
COLORS_yellow = '#f1c40f'


@app.route('/webhook', methods=['post'])
def webhook():
    lp_event = request.headers.get('X-Launchpad-Event-Type')
    if lp_event is not None and lp_event in ALLOWED_EVENTS:
        webhook = settings.SLACK_INCOMING_WEBHOOKS
        username = settings.SLACK_USERNAME
        icon_url = settings.SLACK_ICON_URL
        channel = settings.SLACK_CHANNEL
        project_name = settings.SLACK_PROJECT_NAME

        fields = []

        fields.append({
            'title': 'Project',
            'value': project_name,
            'short': True,
        })

        if lp_event == 'bzr:push:0.1':
            title = "New bzr commit has been pushed"
            title_link = "http://bazaar.launchpad.net/%s/revision/%s" % (
                request.json['bzr_branch_path'], request.json['new']['revision_id'])

        if lp_event == 'git:push:0.1':
            title = "New git commit has been pushed"
            title_link = "https://git.launchpad.net/%s/commit/?id=%s" % (
                request.json['git_repository'], request.json['commit_sha1'])

        if lp_event == 'merge-proposal:0.1':
            merge_proposal = request.json['merge_proposal']
            action = request.json['action']

            registrant = request.json['new']['registrant']
            description = request.json['new']['description']
            commit_message = request.json['new']['commit_message']

            old_queue_status = request.json['old']['queue_status']
            new_queue_status = request.json['new']['queue_status']

            if action == "created":
                title = "Merge request has been proposed" % registrant
                author_name = "%" % registrant[2:]
                author_link = "https://launchpad.net%s" % registrant

            if action == "modified":
                if new_queue_status == "Needs review":
                    title = "Merge request has been updated"
                if new_queue_status == "Approved":
                    title = "Merge request has been approved"
                if new_queue_status == "Merged":
                    title = "Merge request has been merged"

            title_link = "%s" % merge_proposal

        payload = {
            'parse': 'none',
            'attachments': [{
                'fallback': '[%s] %s' % (project_name, title),
                'title': title,
                'title_link': title_link,
                'author_name': author_name or None,
                'author_link': author_link or None,
                'color': "#36a64f",
                'fields': fields,
            }]
        }

        if username:
            payload['username'] = username.encode('utf-8')

        if channel:
            payload['channel'] = channel

        if icon_url:
            payload['icon_url'] = icon_url

        values = {'payload': simplejson.dumps(payload)}
        requests.post(webhook, data=values)

        return Response("OK", content_type='text/plain; charset=utf-8')
    else:
        return Response("Event not Allowed", content_type='text/plain; charset=utf-8')


@app.route('/lp', methods=['get'])
def lp():
    id = int(request.values.get('bug'))
    lp = lp_login()
    if not lp:
        return Response('Error.',
                        content_type='text/plain; charset=utf-8')

    try:
        bugdata = lp.bugs[id]
        if bugdata.private:
            return Response('This bug is private',
                            content_type='text/plain; charset=utf-8')
        dup = bugdata.duplicate_of
        summary_prefix = ''  # Used to made dups easier
        while dup:
            summary_prefix = 'duplicate for #%d ' % id
            bugdata = dup
            dup = bugdata.duplicate_of

        affected = bugdata.users_affected_count_with_dupes
        heat = bugdata.heat

        tasks = bugdata.bug_tasks

        if tasks.total_size != 1:
            tasks = list(tasks)
            try:
                tasks.sort(_sort)
                taskdata = tasks[-1]
            except ValueError:
                tasks = [
                    _ for _ in tasks if _.bug_target_name.endswith(u'(Ubuntu)')]
                if tasks:
                    if len(tasks) != 1:
                        try:
                            tasks.sort(_sort)
                            taskdata = tasks[-1]
                        except ValueError:
                            taskdata = bugdata.bug_tasks[
                                bugdata.bug_tasks.total_size - 1]
                    else:
                        taskdata = tasks[-1]
                else:
                    taskdata = tasks[-1]
        else:
            taskdata = tasks[0]

        assignee = taskdata.assignee
        t = taskdata.bug_target_display_name  # task name

        if assignee:  # "Diaplay Name (Launchpad ID)"
            assignee = u"%s (%s)" % (assignee.display_name, assignee.name)
        else:
            assignee = ''

    except Exception, e:
        return Response('Error : %s' % e, content_type='text/plain; charset=utf-8')

    extinfo = "(affected: %d, heat: %d)" % (affected, heat)

    (bid, product, title, severity, status, assignee, url, extinfo) = (bugdata.id, t, summary_prefix +
                                                                       bugdata.title, taskdata.importance, taskdata.status, assignee, "https://pad.lv/%s/" % bugdata.id, extinfo)

    severity = severity[0].upper() + severity[1:].lower()
    status = status[0].upper() + status[1:].lower()

    return Response("Bug %s in %s \"%s\" %s [%s,%s] %s" %
                    (bid, product, title, extinfo, severity, status, url),
                    content_type='text/plain; charset=utf-8')


@app.route('/')
def index():
    return redirect('https://github.com/daker/launchpad-slack')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
