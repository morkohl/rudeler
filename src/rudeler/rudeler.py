from rudeler.asvz import ASVZScraper
from rudeler.spond_client import SpondClient


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


