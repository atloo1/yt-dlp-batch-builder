# -*- coding: utf-8 -*-
"""
Write a yt-dlp batch file for HTML of a YouTube Watch later playlist.

Run with:

poetry run python yt_dlp_batch_builder/yt_dlp_batch_builder.py \
    --input-filepath ~/Downloads/"Watch later - YouTube.html" \
    --output-filepath ~/Downloads/yt_dlp_batch.txt
"""

import re
from pathlib import Path
from typing import List, Optional, Union

import click

R_VID_ID_INDEXED = re.compile(r'index=\d+')


def yt_dlp_batch_builder(
        input_filepath: Union[Path, str],
        output_filepath: Union[Path, str],
):
    """Write a yt-dlp batch file for a Watch later page.

    :param input_filepath: Watch later playlist HTML filepath
    :param output_filepath: filepath of resultant yt-dlp batch file
    """
    with open(input_filepath) as f:
        html = f.read()

    vid_ids = _get_vid_ids(html)
    vid_titles = _get_vid_titles(html)
    channels = _get_channels(html)

    with open(output_filepath, 'w') as f:
        for vid_id, vid_title, channel in zip(vid_ids, vid_titles, channels):
            f.write(f'https://www.youtube.com/watch?v={vid_id}\t# {vid_title} - {channel}\n')


@click.command()
@click.option('--input-filepath', type=click.Path(exists=True))
@click.option('--output-filepath', type=click.Path())
def _main(
        input_filepath: str,
        output_filepath: str,
):
    """Private click CLI for yt_dlp_batch_builder()."""
    input_filepath = Path(input_filepath).resolve()
    output_filepath = Path(output_filepath).resolve()

    yt_dlp_batch_builder(input_filepath, output_filepath)
    click.echo(f'SUCCESS: see {output_filepath}')


def _get_vid_ids(html_str: str) -> List[str]:
    """Get video IDs in order from a Watch later page."""
    vid_ids = []
    blocks = html_str.split('","commandMetadata":{"webCommandMetadata":{"url":"/watch?v=')[1:]

    for block in blocks:
        vid_id, _ = block.split('","webPageType":"WEB_PAGE_TYPE_WATCH","rootVe":', 1)
        if R_VID_ID_INDEXED.search(vid_id):
            vid_id, _ = vid_id.split('\\', 1)
            vid_ids.append(vid_id)

    return vid_ids


def _get_vid_titles(html_str: str) -> List[str]:
    """Get video titles in order from a Watch later page."""
    vid_titles = []
    blocks = html_str.split('"}],"accessibility":{"accessibilityData":{"label":"')[:-1]

    for block in blocks:
        try:
            vid_title = block.rsplit('}]},"title":{"runs":[{"text":"', 1)[1]

        except IndexError:  # handle premiers
            continue

        vid_titles.append(vid_title)

    return vid_titles


def _get_channels(html_str: str) -> List[str]:
    """Get channels in order from a Watch later page."""
    blocks = html_str.split('"},"shortBylineText":{"runs":[{"text":"')[1:]
    channels = [block.split('","navigationEndpoint":{"clickTrackingParams":"', 1)[0] for block in blocks]

    return channels


if __name__ == '__main__':
    _main()
