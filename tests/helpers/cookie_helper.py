MOCK_COOKIES_PATH="resources/cookies.txt"


def get_mock_cookie():
    return open(MOCK_COOKIES_PATH, "r").read().replace('\n', '')


def store_mock_cookie(mock_cookie):
    with open(MOCK_COOKIES_PATH, "w") as text_file:
        text_file.write(mock_cookie)