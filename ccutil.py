#!/usr/bin/python
import git
import sys
import itertools
import os

from ccutil.utils import verbose, parse_args, open_url_in_browser
from ccutil import githelper
from ccutil import ccollab
from ccutil import db

args = parse_args()

def open_repo():
    return githelper.open_repo(".")

def op_reverts():
    r = open_repo()

    ok = True
    for file in githelper.reverts_list():
        print("{} was reverted!".format(file))
        ok = False

    if ok:
        print("No reverts")
        return 0
    else:
        return 1

def op_conflict():
    r = open_repo()

    conflicts = githelper.conflicts_list(args.b)
    for path in conflicts:
        print("{} was changed in both branches!".format(path))

    if len(conflicts) == 0:
        print("")
        print("No conflicts")
        return 0
    else:
        return 1

def op_update():
    r = open_repo()
    cc_op = len(args.args) and args.args[0] or None

    if cc_op == "auto" or cc_op == "manual" or cc_op == None:
        did_create = False
        if cc_op == "manual":
            files = args.args[1:]
        else:
            files = [os.path.exists(path) and path or "" for (path, _) in githelper.feature_files_changed(r.head)]

        id = db.get(r.head.ref)
        if not id:
            id = str(ccollab.create_new_review(files))
            db.set(r.head.ref, id)
            ccollab.update_review_title(id, r.head.commit.message.strip())
            did_create = True
        else:
            ccollab.append_to_review(id, files)

        if did_create or args.always_open_browser:
            open_url_in_browser(ccollab.review_url(id))
    elif cc_op == "setid":
        db.set(r.head.ref, args.args[1])
    elif cc_op == "reset":
        db.set(r.head.ref, None)
    elif cc_op == "id":
        print(db.get(r.head.ref))
    elif cc_op == "browse":
        id = db.get(r.head.ref)
        if id:
            open_url_in_browser(ccollab.review_url(id))
        else:
            print("cc: failed, no id")
            return 1
    else:
        print("cc: Unknown operation!")
        return 1

    return 0


if __name__ == "__main__":
    ops = {"revert r": op_reverts,
            "conflict c": op_conflict,
            "update up": op_update, }

    for names, cb in ops.items():
        if args.op in names.split(" "):
            sys.exit(cb())

    print("Unknown operation!")
    sys.exit(1)

