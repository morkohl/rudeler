from rudeler.spond_client import SPOND_DATETIME_FORMAT


async def delete_all_events(spond_client):
    spond = spond_client.spond
    events = await spond.get_events()
    event_ids = [event['id'] for event in events]

    for event_id in event_ids:
        url = spond.apiurl + f'sponds/{event_id}?quiet=true'

        await spond.clientsession.delete(url)


def create_event_data(event_title, event_date):
    return {
        'date': event_date,
        'event_url': 'https://www.airsoft-verzeichnis.de/index.php?status=event&eventnummer=018857',
        'extra_info': '(some random extra info)',
        'image_url': 'https://www.airsoft-verzeichnis.de/bilder/0002922/0002922011_c_normal.jpg',
        'title': event_title
    }


def create_event_request_data(event, client_account_id, profile_id, group_id, member_ids, sub_group_id):
    expected_data = {
        'heading': event['title'],
        'description': f'{event["extra_info"]}\nevent link: {event["event_url"]}',
        'meetupPrior': '60',
        'spondType': 'event',
        'startTimestamp': event['date'].strftime(SPOND_DATETIME_FORMAT),
        'openEnded': True,
        'commentsDisabled': False,
        'maxAccepted': 0,
        'rsvpDate': None,
        'location': None,
        'owners': [
            {
                'id': profile_id
            }
        ],
        'visibility': 'ALL',
        'participantsHidden': False,
        'autoReminderType': 'DISABLED',
        'autoAccept': False,
        'attachments': [],
        'type': 'EVENT',
        'tasks': {
            'openTasks': [],
            'assignedTasks': []
        },
        'recipients': {
            'groupMembers': member_ids,
            'group': {
                'id': group_id,
                'subGroups': [sub_group_id]
            }
        }
    }
    return expected_data
