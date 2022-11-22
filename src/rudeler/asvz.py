import re
from datetime import datetime
from http import cookiejar
from typing import Dict

import mechanize
from bs4 import BeautifulSoup

from rudeler.event import EventType

ASVZ_URL = 'https://www.airsoft-verzeichnis.de/'
ASVZ_EVENTS_PAGE = 'https://www.airsoft-verzeichnis.de/index.php?status=event_general&sp=3'

SearchConfigType = Dict[str, Dict[str, str]]


# noinspection PyMethodMayBeStatic
class ASVZScraper:
    """
        Scrapes the ASVZ Website for events.

        Args:
            username (str): The username to log in with.
            password (str): The password to log in with.

            html (str): The HTML in string format to scrape. If not supplied will scrape the ASVZ events page.
    """

    def __init__(self, username: str, password: str, html: str = None) -> None:
        self.username = username
        self.password = password
        self.html = html
        cookie_jar = cookiejar.CookieJar()
        self.browser = mechanize.Browser()
        self.browser.set_cookiejar(cookie_jar)

    def login(self) -> None:
        """
            Logs in to ASVZ using username and password.

            Raises:
                Exception: If the login failed.
        """
        self.browser.open(ASVZ_URL)

        self.browser.select_form(nr=1)

        self.browser.form['field_email'] = self.username
        self.browser.form['field_passwort'] = self.password

        self.browser.submit()

        if not self._was_login_successful():
            raise Exception("ASVZ login failed")

    def scrape_events(self, search_configuration: SearchConfigType) -> list[EventType]:
        """
            Scrapes airsoft event data off the asvz website.

            Will scrape from the ASVZ events page unless HTML is explicitly supplied.

            The search configuration will filter out events that do not fulfill the following conditions:
             - ``searched_event`` title NOT a substring of ``event_title``
             - ``searched_event_extra_info`` NOT a substring of ``event_extra_info``
             - ``searched_event_extra_info`` is present but ``event_extra_info`` are not

            Comparisons are always in lowercase.

            Args:
                search_configuration (SearchConfigType): The search configuration for scraping.

            Returns:
                list[EventType]: A list of dictionaries containing event data.

                {
                    'date': datetime(2022, 11, 19, 8, 0),
                    'event_url': 'https://www.airsoft-verzeichnis.de/index.php?status=event&eventnummer=018857',
                    'extra_info': '(AO Darkzone)',
                    'image_url': 'https://www.airsoft-verzeichnis.de/events_files/0003756547_c_normal.jpg',
                    'title': 'Classic Airsoft Gameday'
                }
        """
        if not self.html:
            self.browser.open(ASVZ_EVENTS_PAGE)

            html_parser = BeautifulSoup(self.browser.response().read(), 'html.parser')
        else:
            html_parser = BeautifulSoup(self.html, 'html.parser')

        all_events = self._collect_events(html_parser)

        return [event for event in all_events if self._is_event_searched_for(event, search_configuration)]

    def _was_login_successful(self) -> bool:
        # It's alot easier to verify that the resulting URL
        # is the starting page than to verify some cookie exists etc.
        return 'status=start' in self.browser.geturl()

    def _collect_events(self, html_parser: BeautifulSoup) -> list[EventType]:
        collected_events = []

        event_months = html_parser.findAll('div', id=re.compile('^ghost\\d{6}'))

        for event_month in event_months:
            event_date_day = ''
            event_date_month = int(event_month.attrs['id'][5:7])
            event_date_year = int(event_month.attrs['id'][7:])

            events_in_month = event_month.findAll(
                'div',
                {'class': 'rahmen_startseite_events_einzelevent'},
                recursive=False
            )

            for event in events_in_month:
                event_info = event.find('div', {'class': 'rahmen_startseite_events_einzelevent_name'})
                event_info_contents = event_info.contents[0]
                event_title = str(event_info_contents.contents[0].text)

                event_extra_info = None

                if type(event_info_contents.contents) == list and len(event_info_contents) > 1:
                    event_extra_info = event_info_contents.contents[1].text

                event_date_text = event.find('div', {'class': 'rahmen_startseite_events_einzelevent_datum'}).text

                if event_date_text:
                    event_date_day = int(event_date_text[:2])

                event_url = event_info.next.attrs['href']

                if ASVZ_URL not in event_url:
                    event_url = ASVZ_URL + event_url

                event_date = datetime(year=event_date_year, month=event_date_month, day=event_date_day, hour=8)

                event_img_url_node = event.find('div', {'class': 'rahmen_startseite_events_einzelevent_bild'})
                event_img_url_img_tag = event_img_url_node.next
                event_img_url_small = event_img_url_img_tag.attrs['src']
                event_img_url = ASVZ_URL + event_img_url_small.replace('mini', 'normal')

                collected_events.append({
                    'date': event_date,
                    'title': event_title,
                    'extra_info': event_extra_info,
                    'image_url': event_img_url,
                    'event_url': event_url,
                })

        return collected_events

    def _is_event_searched_for(self, event: EventType, search_configuration: SearchConfigType):
        for search_config in search_configuration.values():
            event_title = event['title'].lower()
            event_extra_info = event['extra_info'].lower() if event['extra_info'] else None

            searched_event_title = search_config['title_includes'].lower()

            searched_event_extra_info = None

            if 'additional_info_includes' in search_config and search_config['additional_info_includes'] is not None:
                searched_event_extra_info = search_config['additional_info_includes'].lower()

            if searched_event_title in event_title:
                if not searched_event_extra_info and not event_extra_info:
                    return True
                if not searched_event_extra_info and event_extra_info:
                    return True
                if searched_event_extra_info and event_extra_info:
                    if searched_event_extra_info in event_extra_info:
                        return True

        return False
