COOKIES_FILE="cookies.txt"


def get_private_api_cookie():
    file = open(COOKIES_FILE, "r")
    cookie = file.read().replace('\n', '')
    file.close()

    return cookie


def update_private_api_cookie(set_cookie_header):
    if set_cookie_header is not None:
        with open(COOKIES_FILE, "r+") as cookie_file:
            cookie = cookie_file.read()
            cookie_file.seek(0)

            asp_cookie_key = ".AspNet.ApplicationCookie"

            new_asp_cookie = list(filter(lambda cookie: asp_cookie_key in cookie, set_cookie_header.split(";")))
            if len(new_asp_cookie) > 0:
                new_cookie = list(filter(lambda cookie: asp_cookie_key not in cookie, cookie.split(";")))
                new_cookie += new_asp_cookie
                cookie_file.write(";".join(new_cookie))
                cookie_file.truncate()
            else:
                raise ValueError("Invalid cookie returned from server")
