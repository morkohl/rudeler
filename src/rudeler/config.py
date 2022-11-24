import json
import os


class Config:
    RUDELER_SEARCH_CONFIGURATION = json.loads(os.environ['RUDELER_SEARCH_CONFIGURATION'])

    ASVZ_USERNAME = os.environ['ASVZ_USERNAME']
    ASVZ_PASSWORD = os.environ['ASVZ_PASSWORD']

    SPOND_USERNAME = os.environ['SPOND_USERNAME']
    SPOND_PASSWORD = os.environ['SPOND_PASSWORD']
    SPOND_BOT_ACCOUNT_ID = os.environ['SPOND_BOT_ACCOUNT_ID']
    SPOND_GROUP_ID = os.environ['SPOND_GROUP_ID']
    SPOND_SUB_GROUP_ID = os.environ['SPOND_SUB_GROUP_ID']
