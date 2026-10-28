"""Helper de paginacao boto3."""
from typing import Iterator


def paginate(client, operation: str, result_key: str, **kwargs) -> Iterator[dict]:
    paginator = client.get_paginator(operation)
    for page in paginator.paginate(**kwargs):
        yield from page.get(result_key, [])
