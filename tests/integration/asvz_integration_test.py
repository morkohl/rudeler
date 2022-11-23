from datetime import datetime

from rudeler.asvz import ASVZScraper

import pytest

from tests.helpers.utils import json_matcher_first_item, is_valid_uri
from tests.integration.config import Config


def test_asvz_login_success():
    asvz_scraper = ASVZScraper(Config.ASVZ_USERNAME, Config.ASVZ_PASSWORD)

    asvz_scraper.login()


def test_asvz_login_fail():
    asvz_scraper = ASVZScraper(Config.ASVZ_USERNAME, 'invalid')

    with pytest.raises(Exception) as ex:
        asvz_scraper.login()

    assert ex.type == Exception
    assert ex.value.args[0] == 'ASVZ login failed'


def test_asvz_scrape_events():
    asvz_scraper = ASVZScraper(Config.ASVZ_USERNAME, Config.ASVZ_PASSWORD)

    search_config = {
        # Intentionally everything to verify that DOM is still the same and scraping works
        'everything': {
            'title_includes': '',
            'additional_info_includes': ''
        }
    }

    events = asvz_scraper.scrape_events(search_config)

    assert len(events) > 0

    json_match_first_item = json_matcher_first_item(events[0])

    event_date = json_match_first_item('date')
    assert type(event_date) == datetime
    assert event_date > datetime.now()

    event_title = json_match_first_item('title')
    assert type(event_title) == str
    assert len(event_title) > 0

    event_extra_info = json_match_first_item('extra_info')
    assert type(event_extra_info) == str
    assert len(event_extra_info) > 0

    assert is_valid_uri(json_match_first_item('event_url')) is True
    assert is_valid_uri(json_match_first_item('image_url')) is True
