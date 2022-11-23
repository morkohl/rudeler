import asyncio

from rudeler.asvz import ASVZScraper
from rudeler.config import Config
from rudeler.spond_client import SpondClient

from spond.spond import Spond


class Rudeler:

    def __init__(self, asvz_scraper: ASVZScraper, spond_client: SpondClient) -> None:
        self.asvz_scraper = asvz_scraper
        self.spond_client = spond_client

    async def run(self, search_configuration, max_events: int = None) -> None:
        events = self.asvz_scraper.scrape_events(search_configuration)

        if max_events:
            events = events[:max_events]

        print(f'attempting to publish {len(events)} from ASVZ to')

        for event in events:
            event_identifier = event["event_url"]

            print(f'attempting to publish event {event_identifier} to spond')

            if await self.spond_client.is_event_publishable(event):
                print(f'publishing event {event_identifier} to spond')

                await self.spond_client.publish_event(event)

                print(f'successfully published event {event_identifier} to spond')
            else:
                print(f'can not publish event {event_identifier} to spond because it is already published')


async def run_rudeler_async(request):
    asvz_scraper = ASVZScraper(
        username=Config.ASVZ_USERNAME,
        password=Config.ASVZ_PASSWORD
    )

    spond_client = SpondClient(
        spond=Spond(
            username=Config.SPOND_USERNAME,
            password=Config.SPOND_PASSWORD
        ),
        spond_client_account_id=Config.SPOND_BOT_ACCOUNT_ID,
        spond_group_id=Config.SPOND_GROUP_ID,
        spond_sub_group_id=Config.SPOND_SUB_GROUP_ID
    )

    rudeler = Rudeler(
        asvz_scraper=asvz_scraper,
        spond_client=spond_client
    )

    await rudeler.run(Config.RUDELER_SEARCH_CONFIGURATION)


def run_rudeler(request):
    asyncio.run(run_rudeler_async(request))

    return 'success'
