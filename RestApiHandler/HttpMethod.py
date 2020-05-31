from enum import Enum


class HttpMethod(Enum):
    GET = 1
    POST = 2
    HEAD = 3
    PUT = 4
    DELETE = 5
    PATCH = 6
    OPTIONS = 7
