#!/usr/bin/env python3

import requests
import redis
import time
from typing import Callable


def count_calls(method: Callable) -> Callable:
    def wrapper(self, url: str) -> str:
        key = f"count:{url}"
        self._redis.incr(key)
        return method(self, url)

    return wrapper


class WebCache:
    def __init__(self):
        self._redis = redis.Redis()

    @count_calls
    def get_page(self, url: str) -> str:
        cached_content = self._redis.get(url)
        if cached_content:
            return cached_content.decode("utf-8")
        else:
            response = requests.get(url)
            content = response.text
            self._redis.setex(url, 10, content)
            return content
