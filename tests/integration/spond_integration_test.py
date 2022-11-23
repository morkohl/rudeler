from datetime import timedelta, datetime
import random

from spond.spond import Spond

from rudeler.spond_client import SpondClient, SPOND_DATETIME_FORMAT

import pytest
import pytest_asyncio

from tests.helpers.spond import create_event_data, delete_all_events
from tests.helpers.utils import json_matcher, json_matcher_first_item
from tests.integration.config import Config


@pytest.fixture(scope='function')
def spond_client():
    spond_client = SpondClient(
        spond=Spond(
            username=Config.SPOND_USERNAME,
            password=Config.SPOND_PASSWORD
        ),
        spond_client_account_id=Config.SPOND_BOT_ACCOUNT_ID,
        spond_group_id=Config.SPOND_GROUP_ID,
        spond_sub_group_id=Config.SPOND_SUB_GROUP_ID
    )

    return spond_client


@pytest_asyncio.fixture(scope='function')
async def after_delete_events(spond_client):
    yield

    await delete_all_events(spond_client)


@pytest.fixture(scope='module')
def spond_integration_test_group_members():
    return [
        Config.SPOND_BOT_ACCOUNT_ID
    ]


@pytest.mark.asyncio
async def test_spond_publish_event(spond_client, spond_integration_test_group_members, after_delete_events):
    event_title = str(random.getrandbits(64))
    event_date = datetime.now() + timedelta(days=1)

    event = create_event_data(event_title, event_date)

    spond_event_data = await spond_client.publish_event(event)

    json_match = json_matcher(spond_event_data)
    json_match_first_item = json_matcher_first_item(spond_event_data)

    assert json_match_first_item('heading') == event_title
    assert event['extra_info'] in json_match_first_item('description')
    assert event['event_url'] in json_match_first_item('description')
    assert json_match_first_item('startTimestamp') == event['date'].strftime(SPOND_DATETIME_FORMAT)
    # assert json_match_first_item('endTimestamp', spond_event_data) == event['date_end'].strftime(SPOND_DATETIME_FORMAT)
    assert json_match_first_item('meetupPrior') == 60
    assert json_match_first_item('$.recipients.group.id') == spond_client.group_id
    assert spond_integration_test_group_members[0] in json_match('$.recipients.group.members[*].id')
    assert len(json_match('$.recipients.group.members[*].id',)) >= 2
    assert json_match_first_item('visibility') == 'ALL'
    assert json_match_first_item('behalfOfIds') == [spond_client.client_account_id]


@pytest.mark.asyncio
async def test_spond_is_event_publishable_false_event_exists(spond_client, spond_integration_test_group_members, after_delete_events):
    event_title = str(random.getrandbits(64))
    event_date = datetime.now() + timedelta(days=1)

    event = create_event_data(event_title, event_date)

    await spond_client.publish_event(event)

    assert await spond_client.is_event_publishable(event) is False


@pytest.mark.asyncio
async def test_spond_is_event_publishable_true_new_event(spond_client, spond_integration_test_group_members, after_delete_events):
    event_title = str(random.getrandbits(64))
    event_date = datetime.now() + timedelta(days=1)

    event = create_event_data(event_title, event_date)

    assert await spond_client.is_event_publishable(event) is True
