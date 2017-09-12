import argparse
import os

args = None

def parse_args(): 
    global args

    parser = argparse.ArgumentParser()
    parser.add_argument("op")
    parser.add_argument("-b", default=None)
    parser.add_argument("--browser", default=None)
    parser.add_argument("--always-open-browser", action="store_true", default=False)
    parser.add_argument("-v", action="store_true", default=False)
    args = parser.parse_args()
    return args

def verbose(msg, *_args, **kwargs):
    if args.v:
        print(msg.format(*_args, **kwargs))

def open_url_in_browser(url):
    if args.browser:
        print("Opening {}".format(url))
        os.system("open -a {} {}".format(args.browser, url))
