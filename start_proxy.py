from bittrex_proxy import proxy
import environment

def run(cookies_file="cookies.txt"):
    proxy.start(cookies_file)

if __name__ == "__main__":
    run()