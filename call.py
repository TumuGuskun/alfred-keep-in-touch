#!/usr/bin/python3.10
from dataclasses import dataclass, field
from datetime import datetime
import sys
from workflow.workflow import ICON_ERROR, ICON_TRASH
from workflow.workflow3 import Workflow3


@dataclass
class Friend:
    name: str
    last_called: datetime = field(default_factory=lambda: datetime.now())


def main(wf: Workflow3):
    args = wf.args

    if args:
        query = args[0]
        if query.startswith('Add Friend > Name > '):
            _, name = query.split('Add Friend > Name > ')
            friends = wf.stored_data(name='friends') or {}
            friends[name.lower()] = (Friend(name.lower()))
            wf.store_data(name='friends', data=friends)
        elif query.startswith('Call > '):
            _, name = query.split('Call > ')
            friends = wf.stored_data(name='friends') or {}
            friends[name.lower()].last_called = datetime.now()
            wf.store_data(name='friends', data=friends)
        elif query.startswith('Delete > '):
            _, name = query.split('Delete > ')
            friends = wf.stored_data(name='friends') or {}
            del friends[name.lower()]
            wf.store_data(name='friends', data=friends)
        else:
            wf.add_item(title=f'Mark {query} as called',
                        arg=f'Call > {query}', valid=True)
            wf.add_item(title='Delete', arg=f'Delete > {query}',
                        icon=ICON_TRASH, valid=True)
            wf.add_item(title='Cancel', arg='cancel',
                        icon=ICON_ERROR, valid=True)
    else:
        friends = wf.stored_data(name='friends') or {}
        for name, friend in sorted(friends.items(), key=lambda f: f[1].last_called):
            capitalized = ' '.join([name.capitalize()
                                   for name in friend.name.split()])
            wf.add_item(title=capitalized,
                        subtitle=friend.last_called.strftime('%Y-%m-%d'), arg=capitalized, valid=True)

        wf.add_item(title='Add Friend', arg='add', valid=True)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
