import os
from unittest.mock import MagicMock

import pytest
from pytest_mock import mocker
from tests.helpers.asvz import expected_events_all, expected_events_ghg
from get_project_root import root_path

from rudeler.asvz import ASVZScraper, ASVZ_URL


@pytest.fixture(scope='function')
def static_events_html():
    with open(os.path.join(root_path(), 'resources', 'test', 'events.html')) as html_file:
        return html_file.read()


@pytest.fixture(scope='function')
def asvz_scraper():
    return ASVZScraper('some valid username', 'some valid password')


@pytest.fixture(scope='function')
def asvz_scraper_static_html(static_events_html):
    return ASVZScraper('some valid username', 'some valid password', html=static_events_html)


def test_asvz_scrape_events_all_events(asvz_scraper_static_html, expected_events_all):
    search_config = {
        'GHG Event': {
            'title_includes': 'GHG',
            'additional_info_includes': None
        },
        'IZG Event': {
            'title_includes': 'Hungrigen Wolf',
            'additional_info_includes': None
        },
        'Airsoft Operations': {
            'title_includes': 'Classic Airsoft Gameday',
            'additional_info_includes': 'AO Darkzone'
        },
        'Hidefield': {
            'title_includes': 'Hidefield',
            'additional_info_includes': None
        },
        'ASFK': {
            'title_includes': 'ASFK',
            'additional_info_includes': None
        }
    }
    events = asvz_scraper_static_html.scrape_events(search_config)

    assert events == expected_events_all


def test_asvz_scrape_events_only_ghg(asvz_scraper_static_html, expected_events_ghg):
    search_config = {
        'GHG Event': {
            'title_includes': 'GHG',
            'additional_info_includes': None
        },
    }
    events = asvz_scraper_static_html.scrape_events(search_config)

    assert events == expected_events_ghg


def test_asvz_scrape_events_title_does_not_match(asvz_scraper_static_html, expected_events_ghg):
    search_config = {
        'GHG Event': {
            'title_includes': 'NONEXISTENT',
            'additional_info_includes': None
        },
    }
    events = asvz_scraper_static_html.scrape_events(search_config)

    assert events == []


def test_asvz_scrape_events_search_extra_info_present_event_extra_info_not_present(asvz_scraper_static_html):
    search_config = {
        'GHG Event': {
            'title_includes': 'GHG',
            'additional_info_includes': 'NONEXISTENT'
        },
    }
    events = asvz_scraper_static_html.scrape_events(search_config)

    assert events == []


def test_asvz_scrape_events_search_extra_info_not_in_event_extra_info_not_present(asvz_scraper_static_html):
    search_config = {
        'Airsoft Operations': {
            'title_includes': 'Classic Airsoft Gameday',
            'additional_info_includes': 'AO Light zone'
        },
    }
    events = asvz_scraper_static_html.scrape_events(search_config)

    assert events == []


def test_asvz_scraper_login_ok(mocker):
    asvz_scraper = ASVZScraper('some valid username', 'some valid password')

    mock = MagicMock()
    mock.geturl.return_value = ASVZ_URL + 'index.php?status=start'
    mocker.patch.object(asvz_scraper, 'browser', new=mock)

    asvz_scraper.login()


def test_asvz_scraper_login_fails(mocker):
    asvz_scraper = ASVZScraper('some invalid username', 'some invalid password')

    mock = MagicMock()
    mock.geturl.return_value = ASVZ_URL + 'index.php'
    mocker.patch.object(asvz_scraper, 'browser', new=mock)

    with pytest.raises(Exception) as ex:
        asvz_scraper.login()

    assert ex.type == Exception
    assert ex.value.args[0] == 'ASVZ login failed'
