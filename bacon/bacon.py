import json
import logging
from json import JSONDecodeError
from typing import Dict, Text, Union

from click import echo
import requests


LOG = logging.getLogger(__name__)


def compose_query(type_: Text, paras: int, format_: Text, lorem: bool, sentences: int) -> Dict[Text, Union[Text, int]]:
    query = {
        "type": type_,
        "paras": paras,
        "format": format_,
    }

    if lorem:
        query["start-with-lorem"] = 1

    if sentences:
        query["sentences"] = sentences
        query.pop("paras")

    LOG.debug(query)

    return query


def fetch(query):
    response = requests.get("https://baconipsum.com/api/", params=query)

    LOG.debug(f'"URL": {response.url}')
    LOG.debug(f'"Content-Type": {response.headers["Content-Type"]}')
    LOG.debug(f'"Status Code": {response.status_code}')

    if not response.status_code == 200:
        LOG.error("Hmmm... there was a problem contacting the API endpoint.")

    try:
        body = response.json()
    except JSONDecodeError:
        LOG.debug("Returned content is not JSON.")
        body = response.text

    return body


def report(content):
    if isinstance(content, str):
        echo(content)
    elif isinstance(content, list):
        echo(json.dumps(content))
    else:
        pass
