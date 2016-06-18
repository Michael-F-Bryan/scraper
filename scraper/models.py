from urllib.parse import urlparse
from bs4 import BeautifulSoup


class Page:
    """
    A wrapper around a `requests` response that exposes a couple of convenience
    methods and attributes.
    """
    def __init__(self, request):
        self.url = request.url
        self.status_code = request.status_code
        self.soup = BeautifulSoup(request.text, 'html.parser')
        parsed_uri = urlparse(self.url)
        self.base_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    def find(self, *args, **kwargs):
        return self.soup.find(*args, **kwargs)
    
    def find_all(self, *args, **kwargs):
        return self.soup.find_all(*args, **kwargs)    

    def __repr__(self):
        return '<{}: url={}>'.format(
                self.__class__.__name__,
                self.url)

    
class Job:
    """
    A task to be processed by the scraper. This usually encapsulates the
    task handler name, and a url. Any other arguments are passed on to the
    requests library directly.
    """
    def __init__(self, name, url, method='GET', *args, **kwargs):
        self.name = name
        self.url = url
        self.method = method
        self.args = args
        self.kwargs = kwargs
        
    def __repr__(self):
        return '<{}: name={} url="{}">'.format(
                self.__class__.__name__,
                self.name,
                self.url) # if len(self.url) < 20 else self.url[:40]+'...')
