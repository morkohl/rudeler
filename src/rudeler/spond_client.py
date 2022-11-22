import asyncio
from datetime import datetime
from typing import Dict, Any

from spond.spond import Spond

from rudeler.event import EventType

SPOND_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class SpondClient:

    def __init__(self,
                 spond: Spond,
                 spond_client_account_id: str,
                 spond_group_id: str,
                 spond_sub_group_id: str,
                 ) -> None:
        self.spond = spond
        self.spond_web_client = spond.clientsession
        self.client_account_id = spond_client_account_id
        # todo: this should be a parameter in functions
        self.group_id = spond_group_id
        # todo: this should be a parameter in functions
        self.sub_group_id = spond_sub_group_id

    """
        Verifies if an event is logically publishable in Spond.
        
        In order for this function to return True the event must satisfy the following conditions:
         - The date of the event is in the future 
         - The title of the event does not equal the title of any existing events
         - The date of the event does not equal the date of any existing events with the same name
         
         Args:
            event (EventType): The event to verify.
         
         Returns:
            (bool): True if the event is logically publishable. False otherwise.
            
    """
    async def is_event_publishable(self, event: EventType) -> bool:
        if not self.spond.cookie:
            await self.spond.login()

        # todo: this could be a parameter... side effect ?
        upcoming_events = await self.spond.get_events()

        # compare heading and startTimestamp
        # will only work as long as nobody changes the name or the date
        # maybe later this could be compared with extra_info and event_url or image_url
        # maybe add an ASVZ ID to be parsed?

        def is_event_in_future(e: EventType):
            today = datetime.now().date()
            event_date = e['date'].date()

            return event_date >= today

        def is_event_published(ue: list[Dict[str, Any]], e: EventType):
            for upcoming_event in ue:
                upcoming_event_date = datetime.strptime(upcoming_event['startTimestamp'], SPOND_DATETIME_FORMAT).date()
                event_date = e['date'].date()
                if e['title'] == upcoming_event['heading'] and event_date == upcoming_event_date:
                    return True

            return False

        return is_event_in_future(event) and not is_event_published(upcoming_events, event)

    """
        Gets the members for the sub group configured in self.sub_group_id.
        
        Returns: 
            list[str]: The list of members in the specified sub group.
    """
    # todo doesnt have to be a public method and doesnt need tests
    # todo instead make more publish tests and move this piece to publish_events
    async def get_sub_group_members(self) -> list[str]:
        if not self.spond.cookie:
            await self.spond.login()

        # todo: this should be a parameter... side effects are bad
        groups = await self.spond.get_groups()
        group = next((group for group in groups if group['id'] == self.group_id), None)

        if not group:
            raise Exception(f'Account not member of configured group "{self.group_id}"')

        all_sub_group_members = group['members']
        return [member['id'] for member in all_sub_group_members if self.sub_group_id in member['subGroups']]

    """
        Publishes an event to spond.
        
        Args:
            event (EventType): The event to publish.
            
        Returns:
            dict: The json as dictionary from the spond API for the published event.
        
        Raises:
            Exception: If the request did not return status code == 200.
        
    """
    async def publish_event(self, event):
        if not self.spond.cookie:
            await self.spond.login()

        # todo: this should be a parameter... side effects are bad
        member_ids = await self.get_sub_group_members()
        profile_id = await self._get_account_profile_id()

        if len(member_ids) == 0:
            print('Publishing an event with no one invited')

        url = self.spond.apiurl + 'sponds'

        event_data = self._create_event_data(event, profile_id, member_ids)

        headers = {
            'Content-Type': 'application/json',
        }

        response = await self.spond.clientsession.post(url, json=event_data, headers=headers)

        response_status_code = response.status
        if response_status_code != 200:
            raise Exception(f'Publishing event failed '
                            f'with status code "{response_status_code}" and reason "{await response.read()}"')

        return await response.json()

    async def _get_account_profile_id(self):
        groups = await self.spond.get_groups()
        group = next((group for group in groups if group['id'] == self.group_id), None)

        if not group:
            raise Exception(f'Account not member of configured group "{self.group_id}"')

        account_group_member = next((member for member in group['members'] if member['id'] == self.client_account_id))
        profile_id = account_group_member['profile']['id']
        return profile_id

    def _create_event_data(self, event, profile_id, member_ids):
        event_data = {
            'heading': event['title'],
            'description': f'{event["extra_info"]}\n'
                           f'event link: {event["event_url"]}',
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
            # todo change to everyone
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
                    'id': self.group_id,
                    'subGroups': [
                        self.sub_group_id
                    ]
                }
            }
        }
        return event_data

# Code for uploading images
# print('uploading image')
#
#
# res = await self.spond.clientsession.get(event['image_url'])
#
# url = 'https://spond.com/api/2.1/images/upload'
#
# headers = {
#     'Content-Type': 'multipart/form-data; boundary=---------------------------255867094021998731301751551194'
# }
#
# img = await res.read()
#
# with aiohttp.MultipartWriter as mpwriter:
#     mpwriter.append(await res.read(), headers={'Content-Type': 'image/jpeg'})
#
#
# res = await self.spond.clientsession.post(url, data=mpwriter, headers=headers)
