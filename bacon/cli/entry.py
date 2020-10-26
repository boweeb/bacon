#!/usr/bin/env python3

import logging
import sys

import click
import requests


LOG = logging.getLogger(__name__)


@click.command(context_settings=dict(help_option_names=["-h", "--help"], max_content_width=120))
@click.option("--verbose", "-v", is_flag=True, default=False)
@click.option("--type", "-t", "type_", default="meat-and-filler", help="")
@click.option("--paras", "-p", default=1, help="Optional number of paragraphs.")
@click.option("--sentences", "-s", default=0, help='Number of sentences (overrides "paras").')
@click.option("--lorem/--no-lorem", "-l/-n", default=True, help="")
@click.option("--format", "-f", "format_", default="json", help="")
def root(verbose, type_, paras, sentences, lorem, format_):
    if verbose:
        LOG.setLevel(logging.DEBUG)

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

    r = requests.get("https://baconipsum.com/api/", params=query)

    LOG.debug(f'"URL": {r.url}')
    LOG.debug(f'"Content-Type": {r.headers["Content-Type"]}')
    LOG.debug(f'"Status Code": {r.status_code}')

    if not r.status_code == 200:
        LOG.error("Hmmm... there was a problem contacting the API endpoint.")

    body = r.json()

    for line in body:
        print(line)


def main():
    root(show_default=True)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
