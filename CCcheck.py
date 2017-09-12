#!/usr/bin/python
import git
import sys
import itertools
import os

from cchelper.utils import verbose, parse_args, open_url_in_browser
from cchelper import githelper
from cchelper import ccollab
from cchelper import db

args = parse_args()

if __name__ == "__main__":
    r = githelper.open_repo(".")
    develop_head = r.branches["develop"].commit

    if args.op == "revert" or args.op == "r":
        ok = True
        for file in githelper.reverts_list():
            print("{} was reverted!".format(file))
            ok = False

        if ok:
            print("No reverts")
            sys.exit(0)
        else:
            sys.exit(1)

    elif args.op == "conflict" or args.op == "c":
        conflicts = githelper.conflicts_list(args.b)

        for path in conflicts:
            print("{} was changed in both branches!".format(path))

        if len(conflicts) == 0:
            print("")
            print("No conflicts")
            sys.exit(0)
        else:
            sys.exit(1)

    elif args.op == "updatecc" or args.op == "cc":
        did_create = False
        files = githelper.feature_files_changed(r.head)
        id = db.get(r.head.ref)

        if not id:
            id = ccollab.create_new_review(files)
            db.set(r.head.ref, id)
            did_create = True
        else:
            ccollab.append_to_review(id, files)

        if did_create or args.always_open_browser:
            open_url_in_browser(ccollab.review_url(id))
    elif args.op == "cc_clean":
        db.set(r.head.ref, None)
    elif args.op == "cc_id":
        print(db.get(r.head.ref))
    else:
        print("Unknown operation!")
        sys.exit(1)

