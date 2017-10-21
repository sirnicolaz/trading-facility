import urllib.request
import json
from lxml.html.soupparser import fromstring
from environment import COIN_SOCIAL_DIR
import pathlib


def __get_url_content(url):
    response = urllib.request.urlopen(url)
    encoding = response.info().get_content_charset('utf8')

    return response.read().decode(encoding)


def run(output_dir):
    coin_list_url = "https://files.coinmarketcap.com/generated/search/quick_search.json"
    coin_list = json.loads(__get_url_content(coin_list_url))

    for coin in coin_list:
        coin_url = "https://coinmarketcap.com/currencies/%s/" % coin['slug']
        coin_html = __get_url_content(coin_url)

        tree = fromstring(coin_html)
        result = tree.xpath("string(//*[@class='twitter-timeline']/@href)")

        with open(output_dir + "/" + coin['symbol'], "w") as file:
            file.write(result)


if __name__ == '__main__':
    pathlib.Path(COIN_SOCIAL_DIR).mkdir(parents=True, exist_ok=True)
    run(COIN_SOCIAL_DIR)