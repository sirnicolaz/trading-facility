import time
from urllib.request import Request, urlopen

from bittrex_proxy.utilities import cookie_store


def __add_default_headers(request):
    request.add_header('Accept-Encoding', 'deflate, sdch, br')
    request.add_header('Accept-Language', 'de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4')
    request.add_header('Upgrade-Insecure-Requests', 1)
    request.add_header('User-Agent',
                 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36')
    request.add_header('Referer', 'https://bittrex.com/History')
    request.add_header('Connection', 'keep-alive')


def request_handling_loop(queue):
    while True:
        # read next request from queue
        data = queue.get()
        url = data['url']
        accept = data['accept']
        query = data['query'] if 'query' in data else None
        response_pipe = data['response_pipe'] if 'response_pipe' in data else None

        q = Request(url)
        cookies = cookie_store.get_private_api_cookie()
        q.add_header('Cookie', cookies)
        q.add_header('Accept', accept)

        q.add_header('Accept-Encoding', 'deflate, sdch, br')
        q.add_header('Accept-Language', 'de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4')
        q.add_header('Upgrade-Insecure-Requests', 1)
        q.add_header('User-Agent',
                     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36')
        q.add_header('Referer', 'https://bittrex.com/History')
        q.add_header('Connection', 'keep-alive')

        if query:
            q.data = query.encode('utf-8')

        attempts = 0
        response = None

        while attempts < 3:
            try:
                response = urlopen(q)
                attempts = 3
            except Exception as e:
                attempts += 1
                print("Error opening url: %s" % str(e))
                time.sleep(2)

        if response is not None:
            cookie_store.update_private_api_cookie(response.headers["Set-Cookie"])
            data = response.read()
        else:
            data = None

        if response_pipe:
            response_pipe.send(data)
