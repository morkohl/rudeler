from datetime import datetime, timedelta
from unittest.mock import AsyncMock

import aiohttp
import pytest
from pytest_mock import mocker
from spond.spond import Spond

from rudeler.spond_client import SpondClient, SPOND_DATETIME_FORMAT
from tests.helpers.spond import create_event_request_data, create_event_data


@pytest.fixture(scope='function')
def spond_basic_mock(mocker):
    mocker.patch.object(Spond, 'login', autospec=True)


@pytest.fixture(scope='function')
def spond_client():
    return SpondClient(
        spond=Spond(username='some username', password='some password'),
        spond_client_account_id='some client account id',
        spond_group_id='some group id',
        spond_sub_group_id='spond_sub_group_id'
    )


def create_spond_event_data(event_title, event_date):
    return {
        'heading': event_title,
        'startTimestamp': event_date.strftime(SPOND_DATETIME_FORMAT)
    }


@pytest.mark.asyncio
async def test_spond_is_event_publishable_true_first_event(mocker, spond_client, spond_basic_mock):
    event_title = 'some title'
    event_date = datetime.now() + timedelta(days=1)
    event = create_event_data(event_title, event_date)

    mocker.patch.object(Spond, 'get_events', new=AsyncMock(return_value=[]))

    assert await spond_client.is_event_publishable(event) is True


@pytest.mark.asyncio
async def test_spond_is_event_publishable_true_new_event(mocker, spond_client, spond_basic_mock):
    now = datetime.now()
    event_date_new = now + timedelta(days=1)
    event_date_spond = now + timedelta(days=2)
    event = create_event_data('some title', event_date_new)
    spond_event = create_spond_event_data('some different title', event_date_spond)

    mocker.patch.object(Spond, 'get_events', new=AsyncMock(return_value=[spond_event]))

    assert await spond_client.is_event_publishable(event) is True


@pytest.mark.asyncio
async def test_spond_is_event_publishable_true_new_event_diff_title_same_date(mocker, spond_client, spond_basic_mock):
    event_date = datetime.now() + timedelta(days=1)
    event = create_event_data('some title', event_date)
    spond_event = create_spond_event_data('some different title', event_date)

    mocker.patch.object(Spond, 'get_events', new=AsyncMock(return_value=[spond_event]))

    assert await spond_client.is_event_publishable(event) is True


@pytest.mark.asyncio
async def test_spond_is_event_publishable_true_new_event_same_title_diff_date(mocker, spond_client, spond_basic_mock):
    event_title = 'some title'
    now = datetime.now()
    event_date_new = now + timedelta(days=1)
    event_date_spond = now + timedelta(days=2)
    event = create_event_data(event_title, event_date_new)
    spond_event = create_spond_event_data(event_title, event_date_spond)

    mocker.patch.object(Spond, 'get_events', new=AsyncMock(return_value=[spond_event]))

    assert await spond_client.is_event_publishable(event) is True


@pytest.mark.asyncio
async def test_spond_is_event_publishable_false_equal_title_and_date(mocker, spond_client, spond_basic_mock):
    event_title = 'some title'
    event_date = datetime.now() + timedelta(days=1)
    event = create_event_data(event_title, event_date)
    spond_event = create_spond_event_data(event_title, event_date)

    mocker.patch.object(Spond, 'get_events', new=AsyncMock(return_value=[spond_event]))

    assert await spond_client.is_event_publishable(event) is False


@pytest.mark.asyncio
async def test_spond_is_event_publishable_false_date_in_past(mocker, spond_client, spond_basic_mock):
    event_title = 'some title'
    event_date = datetime.now() - timedelta(days=1)
    event = create_event_data(event_title, event_date)

    mocker.patch.object(Spond, 'get_events', new=AsyncMock(return_value=[]))

    assert await spond_client.is_event_publishable(event) is False


@pytest.mark.asyncio
async def test_spond_get_sub_group_member_ids_find_members(mocker, spond_client, spond_basic_mock):
    group_id = 'some group id'
    sub_group_id = 'some sub group id'
    member_id = 'member 1'
    groups = [
        {
            'id': group_id,
            'members': [
                {
                    'id': member_id,
                    'subGroups': [sub_group_id]
                },
                {
                    'id': 'member 2',
                    'subGroups': ['some other sub group id']
                }
            ]
        },
        {
            'id': 'some other group id'
        }
    ]

    mocker.patch.object(Spond, 'get_groups', new=AsyncMock(return_value=groups))

    spond_client.group_id = group_id
    spond_client.sub_group_id = sub_group_id

    assert await spond_client.get_sub_group_members() == [member_id]


@pytest.mark.asyncio
async def test_spond_get_sub_group_member_ids_find_no_members(mocker, spond_client, spond_basic_mock):
    group_id = 'some group id'
    sub_group_id = 'some sub group id'
    member_id = 'member 1'
    groups = [
        {
            'id': group_id,
            'members': [
                {
                    'id': 'some member id',
                    'subGroups': ['some other sub group id']
                }
            ]
        },
        {
            'id': 'some other group',
            'members': [
                {
                    'id': member_id,
                    'subGroups': [sub_group_id]
                },
            ]
        }
    ]

    mocker.patch.object(Spond, 'get_groups', new=AsyncMock(return_value=groups))

    spond_client.group_id = group_id
    spond_client.sub_group_id = sub_group_id

    assert await spond_client.get_sub_group_members() == []


@pytest.mark.asyncio
async def test_spond_get_sub_group_member_ids_fail_account_not_in_group(mocker, spond_client, spond_basic_mock):
    mocker.patch.object(Spond, 'get_groups', new=AsyncMock(return_value=[]))

    with pytest.raises(Exception) as ex:
        await spond_client.get_sub_group_members()

    assert ex.type == Exception
    assert ex.value.args[0] == f'Account not member of configured group "{spond_client.group_id}"'


@pytest.mark.asyncio
async def test_spond_publish_event(mocker, spond_client, spond_basic_mock):
    client_account_id = 'some account id'
    profile_id = 'some profile id'
    group_id = 'some group id'
    sub_group_id = 'some sub group id'
    member_id = 'member 1'
    event_title = 'some title'
    event_date = datetime.now() + timedelta(days=1)
    event = create_event_data(event_title, event_date)

    mocker.patch.object(SpondClient, 'get_sub_group_members', new=AsyncMock(return_value=['member 1']))
    mocker.patch.object(SpondClient, '_get_account_profile_id', new=AsyncMock(return_value=profile_id))

    expected_status_code = 200
    expected_status_message = 'OK'
    mocked_response = AsyncMock()
    mocked_response.status = expected_status_code
    mocked_response.read.return_value = expected_status_message

    mocker.patch.object(
        aiohttp.ClientSession,
        'post',
        new=AsyncMock(return_value=mocked_response)
    )

    spond_client.client_account_id = client_account_id
    spond_client.group_id = group_id
    spond_client.sub_group_id = sub_group_id

    await spond_client.publish_event(event)

    expected_url = 'https://spond.com/api/2.1/sponds'

    expected_headers = {
        'Content-Type': 'application/json'
    }

    expected_data = create_event_request_data(
        event,
        client_account_id,
        profile_id,
        group_id,
        [member_id],
        sub_group_id
    )

    spond_client.spond.clientsession.post.assert_called_once_with(
        expected_url,
        json=expected_data,
        headers=expected_headers
    )

    mocked_response.json.assert_called_once()


@pytest.mark.asyncio
async def test_spond_publish_event_fail(mocker, spond_client, spond_basic_mock):
    event_title = 'some title'
    event_date = datetime.now() + timedelta(days=1)
    event = create_event_data(event_title, event_date)

    mocker.patch.object(SpondClient, 'get_sub_group_members', new=AsyncMock(return_value=['member 1']))
    mocker.patch.object(SpondClient, '_get_account_profile_id', new=AsyncMock(return_value='some profile id'))

    expected_status_code = 500
    expected_status_message = 'Server Error'
    mocked_response = AsyncMock()
    mocked_response.status = expected_status_code
    mocked_response.read.return_value = expected_status_message

    mocker.patch.object(
        aiohttp.ClientSession,
        'post',
        new=AsyncMock(return_value=mocked_response)
    )

    with pytest.raises(Exception) as ex:
        await spond_client.publish_event(event)

    assert ex.type == Exception
    assert ex.value.args[0] == f'Publishing event failed' \
                               f' with status code "{expected_status_code}" and reason "{expected_status_message}"'
