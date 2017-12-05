#!/usr/bin/python
import git
import sys
import itertools
import os

from ccutil.utils import verbose, message, output, parse_args, open_url_in_browser
from ccutil import githelper
from ccutil import ccollab
from ccutil import db
from ccutil import utils

args = parse_args()

def open_repo():
    return githelper.open_repo(".")

def op_reverts():
    r = open_repo()

    ok = True
    for file in githelper.reverts_list():
        message("{} was reverted!", file)
        output(file)
        ok = False

    if ok:
        message("No reverts")
        return 0
    else:
        return 1

def op_conflict():
    r = open_repo()

    ref1 = r.head
    ref2 = None
    if args.c:
        ref1 = r.branches[args.c]

    conflicts = None
    if args.r:
        ref_changes = githelper.feature_files_changed(ref1)
        cc_changes = ccollab.review_files_changed(args.r)
        conflicts = utils.hashdict_conflicts(ref_changes, cc_changes, str(ref1), "CC {}".format(args.r))
    else:
        conflicts = githelper.conflicts_list(ref1, args.b)

    for path in conflicts:
        message("{} was changed in both branches!", path)
        output(path)

    if len(conflicts) == 0:
        message("")
        message("No conflicts")
        return 0
    else:
        return 1

def op_update():
    r = open_repo()
    cc_op = len(args.args) and args.args[0] or None
    ref = r.head.ref
    if args.b:
        ref = args.b

    if cc_op == "auto" or cc_op == "manual" or cc_op == None:
        did_create = False
        if cc_op == "manual":
            files = args.args[1:]
            if args.reverts:
                files = files + githelper.reverts_list()

            id = db.get(r.head.ref)
            if id:
                ccollab.append_files_to_review(files)
            else:
                message("manual upload failed: no id!")
                return 1
        else:
            commits = githelper.feature_commits(r.head)
            id = db.get(r.head.ref)
            if args.a and not id:
                message("updated failed: no id in append only mode")
                return 1

            if not id:
                id = str(ccollab.create_new_review(commits))
                db.set(r.head.ref, id)
                ccollab.update_review(id, r.head.commit.message.strip(), args.group, "git: {}".format(str(r.head.ref)))
                did_create = True
            else:
                ccollab.append_to_review(id, commits)

            if did_create or args.always_open_browser:
                open_url_in_browser(ccollab.review_url(id))

    elif cc_op == "setid":
        db.set(ref, args.args[1])
    elif cc_op == "reset":
        db.set(ref, None)
    elif cc_op == "id":
        message("Current id: {}", db.get(ref))
        output(db.get(ref))
    elif cc_op == "browse":
        id = db.get(ref)
        if id:
            open_url_in_browser(ccollab.review_url(id))
        else:
            message("browse failed, no id")
            return 1
    else:
        message("cc: Unknown operation!")
        return 1

    return 0


if __name__ == "__main__":
    ops = {"revert r": op_reverts,
            "conflict c": op_conflict,
            "update up": op_update, }

    for names, cb in ops.items():
        if args.op in names.split(" "):
            sys.exit(cb())

    message("Unknown operation!")
    sys.exit(1)

