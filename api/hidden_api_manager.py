from urllib.request import Request, urlopen
import os

__COOKIES_FILE = os.environ.get("COOKIES_FILE")


def __update_cookies(response):
    new_cookies = response.headers['Set-Cookie']
    if new_cookies is not None:
        with open(__COOKIES_FILE, "w") as text_file:
            text_file.write(new_cookies)


def __get_cookies():
    return open(__COOKIES_FILE, "r").read().replace('\n', '')


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
        cookies = __get_cookies()
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

        response = urlopen(q)

        __update_cookies(response)

        if response_pipe:
            response_pipe.send(response.read())
