import json
import os

from dotenv import load_dotenv

from rudeler.constants import ROOT_DIR, PROJECT_NAME

load_dotenv(os.environ['RUDELER_ENV_FILE'])


class Config:
    PROJECT_NAME = PROJECT_NAME
    ROOT_DIR = ROOT_DIR

    RUDELER_SEARCH_CONFIGURATION = json.loads(os.environ['RUDELER_SEARCH_CONFIGURATION'])

    ASVZ_USERNAME = os.environ['ASVZ_USERNAME']
    ASVZ_PASSWORD = os.environ['ASVZ_PASSWORD']

    SPOND_USERNAME = os.environ['SPOND_USERNAME']
    SPOND_PASSWORD = os.environ['SPOND_PASSWORD']
    SPOND_BOT_ACCOUNT_ID = os.environ['SPOND_BOT_ACCOUNT_ID']
    SPOND_GROUP_ID = os.environ['SPOND_GROUP_ID']
    SPOND_SUB_GROUP_ID = os.environ['SPOND_SUB_GROUP_ID']
