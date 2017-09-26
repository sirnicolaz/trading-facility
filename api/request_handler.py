import urllib.request
from urllib.request import Request, urlopen
from urllib.error import URLError
import json
from uuid import uuid1
import hmac


def get(url):
    attempts = 3
    while attempts > 0:
        try:
            response = urllib.request.urlopen(url)
            encoding = response.info().get_content_charset('utf8')
            data = json.loads(response.read().decode(encoding))
            attempts = 0
        except URLError:
            attempts -= 1

    return data


def get_auth(url, api_key, api_secret):
    if not api_secret or not api_key:
        raise ValueError("Missing API Key and/or API Secret")

    auth_url = __authenticate_url(url, api_key)
    sign = hmac.new(str.encode(api_secret), str.encode(auth_url), digestmod="sha512").hexdigest()

    q = Request(auth_url)
    q.add_header('apisign', sign)
    response = urlopen(q)

    encoding = response.info().get_content_charset('utf8')
    data = json.loads(response.read().decode(encoding))

    return data


def __authenticate_url(url, api_key):
    nonce = str(uuid1())
    api_key_param = "apikey=%s&nonce=%s" % (api_key, nonce)
    if '?' not in url:
        return url + "?" + api_key_param
    else:
        return url + "&" + api_key_param