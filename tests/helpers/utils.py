from urllib.parse import urlparse

from dotenv import load_dotenv

import jsonpath_rw_ext as json_parser


def json_matcher(data):
    return lambda json_path_expr: json_parser.match(json_path_expr, data)


def json_matcher_first_item(data):
    return lambda json_path_expr: json_parser.match(json_path_expr, data)[0]


def load_integration_test_env(env_file: str = '.env.integrationtest'):
    load_dotenv(env_file)


def is_valid_uri(uri):
    try:
        result = urlparse(uri)
        return all([result.scheme, result.netloc])
    except:
        return False
