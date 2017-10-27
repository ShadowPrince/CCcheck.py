import argparse
import os

args = None

def parse_args():
    global args

    parser = argparse.ArgumentParser(description="ccollab helper tool")
    parser.add_argument("op", help="""\
revert, r - check for reverts against current working tree.
conflict, c - check for conftlicts against develop (or another branch if -b is featured).

update, up - ccollab helper:
     auto - upload files changed in the branch. 
     manual [file, ] - upload files from arguments. 
     id - get CC id for current branch. 
     setid ID - set id for current branch. 
     reset - remove id for current branch\
""")
    parser.add_argument("args", nargs="*", default=None)
    parser.add_argument("-b", default=None, help="branch to check conflicts against (instead of develop)")
    parser.add_argument("-r", default=None, help="CC id to check conflicts against (instead of develop)")

    parser.add_argument("-c", default=None, help="branch to check conflicts with (defaults to current one)")
    parser.add_argument("--browser", default=None, help="Browser application to use with CC")
    parser.add_argument("--group", default=None, help="GUID of CC group to use")
    parser.add_argument("--reverts", default=False, action="store_true", help="Add reverted files to CC (used in manual variant of update)")
    parser.add_argument("--always-open-browser", action="store_true", default=False, help="Open browser even on updating existing CC")
    parser.add_argument("-a", action="store_true", default=False, help="append only mode - quietly fail when there's no review associated with the branch")
    parser.add_argument("-q", action="store_true", default=False, help="quiet")
    parser.add_argument("-v", action="store_true", default=False, help="verbose")
    args = parser.parse_args()
    return args

def verbose(msg, *_args, **kwargs):
    if args.v and not args.q:
        print(msg.format(*_args, **kwargs))

def message(msg, *_args, **_kwargs):
    if not args.q:
        print(msg.format(*_args, **_kwargs))

def output(msg, *_args, **_kwargs):
    if args.q:
        print(msg.format(*_args, **_kwargs))

def open_url_in_browser(url):
    if args.browser:
        message("Opening {}", url)
        os.system("open -a {} {}".format(args.browser, url))

def hashdict_conflicts(a, b, ref1="a", ref2="b"):
    format = "{:<%s} changed {:<100} {}" % len(max(ref1, ref2))
    for path, hash in a.items():
        verbose(format, ref1, path, hash[:6])
    for path, hash in b.items():
        verbose(format, ref2, path, hash[:6])

    conflicts = []
    for path1, hash1 in a.items():
        for path2, hash2 in b.items():
            if path1 == path2 and hash1 != hash2 and path1 not in conflicts:
                conflicts.append(path1)
            elif path1 == path2:
                message("Path {} was changed in both branches with resulting in equal hashes!", path1)

    return conflicts
