from requests import Session
from urllib.parse import urljoin


class BaseSession(Session):
    def __init__(self, base_url=None):
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        if url.startswith('http'):
            joined_url = url
        else:
            joined_url = urljoin(self.base_url, url)
        return super().request(method, joined_url, *args, **kwargs)
