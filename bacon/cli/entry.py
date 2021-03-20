#!/usr/bin/env python3

import logging
import sys

import click

from bacon.bacon import compose_query, fetch, report


LOG = logging.getLogger(__name__)


@click.command(context_settings=dict(help_option_names=["-h", "--help"], max_content_width=120))
@click.option("-v", "--verbose", is_flag=True, default=False, help="Show logs.")
@click.option(
    "-t",
    "--type",
    "type_",
    type=click.Choice(["all-meat", "meat-and-filler"]),
    default="meat-and-filler",
    help='"all-meat" for meat only or "meat-and-filler" for meat mixed with miscellaneous "lorem ipsum" filler.',
)
@click.option("-p", "--paras", default=1, help="Optional number of paragraphs.")
@click.option("-s", "--sentences", default=0, help='Number of sentences (overrides "paras").')
@click.option(
    "-l/-n", "--lorem/--no-lorem", default=True, help='Start the first paragraph with "Bacon ipsum dolor sit amet".'
)
@click.option(
    "-f",
    "--format",
    "format_",
    type=click.Choice(["json", "text", "html"]),
    default="text",
    help="Format of returned payload.",
)
def root(verbose, type_, paras, sentences, lorem, format_):
    """Bacon Ipsum API Client"""
    if verbose:
        LOG.setLevel(logging.DEBUG)

    query = compose_query(type_, paras, format_, lorem, sentences)
    content = fetch(query)
    report(content)


def main():
    root(
        auto_envvar_prefix="BACON",
        show_default=True,
    )


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
