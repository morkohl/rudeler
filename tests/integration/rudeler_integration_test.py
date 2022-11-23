import pytest
import pytest_asyncio

from main import Rudeler
from rudeler.asvz import ASVZScraper
from rudeler.spond_client import SpondClient

from tests.integration.config import Config

from spond.spond import Spond

import pytest

from tests.helpers.spond import delete_all_events


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


@pytest.mark.asyncio
async def test_rudeler_success(after_delete_events):
    asvz_scraper = ASVZScraper(
        Config.ASVZ_USERNAME,
        Config.ASVZ_PASSWORD,
    )

    spond_client = SpondClient(
        spond=Spond(
            Config.SPOND_USERNAME,
            Config.SPOND_PASSWORD
        ),
        spond_client_account_id=Config.SPOND_BOT_ACCOUNT_ID,
        spond_group_id=Config.SPOND_GROUP_ID,
        spond_sub_group_id=Config.SPOND_SUB_GROUP_ID
    )

    rudeler = Rudeler(asvz_scraper, spond_client)

    search_configuration = {
        'everything': {
            'title_includes': '',
            'additional_info_includes': None
        },
    }

    await rudeler.run(search_configuration, max_events=5)

