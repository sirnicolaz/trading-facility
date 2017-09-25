MOCK_COOKIES_PATH="/tmp/cookies.txt"


def get_mock_cookie():
    file = open(MOCK_COOKIES_PATH, "r")
    cookie = file.read().replace('\n', '')
    file.close()

    return cookie


def store_mock_cookie(mock_cookie):
    with open(MOCK_COOKIES_PATH, "w") as text_file:
        text_file.write(mock_cookie)