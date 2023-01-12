from typing import Any


class Server:
    ip: str
    query_port: int

    def __init__(self, ip: str, query_port: int):
        self.ip = ip
        self.query_port = query_port

    def __iter__(self):
        yield 'ip', self.ip
        yield 'query_port', self.query_port

    def __repr__(self):
        return f'{self.ip}:{self.query_port}'

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and \
            other.ip == self.ip and \
            other.query_port == self.query_port
