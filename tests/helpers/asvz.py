from datetime import datetime

import pytest


@pytest.fixture(scope='session')
def expected_events_all():
    return [
        {
            'date': datetime(2022, 11, 19, 8, 0),
            'event_url': 'https://www.airsoft-verzeichnis.de/index.php?status=event&eventnummer=018857',
            'extra_info': '(AO Darkzone)',
            'image_url': 'https://www.airsoft-verzeichnis.de/events_files/0003756547_c_normal.jpg',
            'title': 'Classic Airsoft Gameday'
        },
        {
            'date': datetime(2022, 11, 19, 8, 0),
            'event_url': 'https://www.airsoft-verzeichnis.de/index.php?status=event&eventnummer=019713',
            'extra_info': None,
            'image_url': 'https://www.airsoft-verzeichnis.de/events_files/0003898344_c_normal.jpg',
            'title': 'GHG Fungame'
        },
        {
            'date': datetime(2022, 11, 20, 8, 0),
            'event_url': 'https://www.airsoft-verzeichnis.de/index.php?status=event&eventnummer=018858',
            'extra_info': '(AO Darkzone)',
            'image_url': 'https://www.airsoft-verzeichnis.de/events_files/0003756549_c_normal.jpg',
            'title': 'Classic Airsoft Gameday'
        },
        {
            'date': datetime(2022, 11, 20, 8, 0),
            'event_url': 'https://www.airsoft-verzeichnis.de/index.php?status=event&eventnummer=019722',
            'extra_info': '(ASFK GAMEDAY )',
            'image_url': 'https://www.airsoft-verzeichnis.de/events_files/0003900326_c_normal.jpg',
            'title': 'ASFK GAMEDAY '
        },
        {
            'date': datetime(2022, 11, 27, 8, 0),
            'event_url': 'https://www.airsoft-verzeichnis.de/index.php?status=event&eventnummer=019723',
            'extra_info': '(ASFK GAMEDAY )',
            'image_url': 'https://www.airsoft-verzeichnis.de/events_files/0003900307_c_normal.jpg',
            'title': 'ASFK GAMEDAY '
        },
        {
            'date': datetime(2022, 11, 27, 8, 0),
            'event_url': 'https://www.airsoft-verzeichnis.de/index.php?status=event&eventnummer=019728',
            'extra_info': '(Hidefield)',
            'image_url': 'https://www.airsoft-verzeichnis.de/events_files/0003903025_c_normal.jpg',
            'title': 'Sonntagsspiel auf Hidefield'
        },
        {
            'date': datetime(2022, 12, 3, 8, 0),
            'event_url': 'https://www.airsoft-verzeichnis.de/index.php?status=event&eventnummer=019398',
            'extra_info': '(Hungriger Wolf)',
            'image_url': 'https://www.airsoft-verzeichnis.de/events_files/0003844531_c_normal.jpg',
            'title': 'Hungrigen Wolf Spieltag Nr. 17'
        },
        {
            'date': datetime(2022, 12, 4, 8, 0),
            'event_url': 'https://www.airsoft-verzeichnis.de/index.php?status=event&eventnummer=019644',
            'extra_info': None,
            'image_url': 'https://www.airsoft-verzeichnis.de/events_files/0003881818_c_normal.jpg',
            'title': 'GHG Fungame'
        },
        {
            'date': datetime(2022, 12, 4, 8, 0),
            'event_url': 'https://www.airsoft-verzeichnis.de/index.php?status=event&eventnummer=018853',
            'extra_info': '(AO Darkzone)',
            'image_url': 'https://www.airsoft-verzeichnis.de/events_files/0003756539_c_normal.jpg',
            'title': 'Classic Airsoft Gameday'
        },
        {
            'date': datetime(2022, 12, 10, 8, 0),
            'event_url': 'https://www.airsoft-verzeichnis.de/index.php?status=event&eventnummer=019729',
            'extra_info': '(Hidefield)',
            'image_url': 'https://www.airsoft-verzeichnis.de/events_files/0003903030_c_normal.jpg',
            'title': 'Spieltag auf Hidefield'
        },
        {
            'date': datetime(2022, 12, 11, 8, 0),
            'event_url': 'https://www.airsoft-verzeichnis.de/index.php?status=event&eventnummer=018852',
            'extra_info': '(AO Darkzone)',
            'image_url': 'https://www.airsoft-verzeichnis.de/events_files/0003756537_c_normal.jpg',
            'title': 'Classic Airsoft Gameday'
        },
        {
            'date': datetime(2022, 12, 17, 8, 0),
            'event_url': 'https://www.airsoft-verzeichnis.de/index.php?status=event&eventnummer=019399',
            'extra_info': '(Hungriger Wolf)',
            'image_url': 'https://www.airsoft-verzeichnis.de/events_files/0003844534_c_normal.jpg',
            'title': 'Hungrigen Wolf Spieltag Nr. 18'
        }
    ]


@pytest.fixture(scope='session')
def expected_events_ghg():
    return [
        {
            'date': datetime(2022, 11, 19, 8, 0),
            'event_url': 'https://www.airsoft-verzeichnis.de/index.php?status=event&eventnummer=019713',
            'extra_info': None,
            'image_url': 'https://www.airsoft-verzeichnis.de/events_files/0003898344_c_normal.jpg',
            'title': 'GHG Fungame'
        },
        {
            'date': datetime(2022, 12, 4, 8, 0),
            'event_url': 'https://www.airsoft-verzeichnis.de/index.php?status=event&eventnummer=019644',
            'extra_info': None,
            'image_url': 'https://www.airsoft-verzeichnis.de/events_files/0003881818_c_normal.jpg',
            'title': 'GHG Fungame'
        },
    ]
