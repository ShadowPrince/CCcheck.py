#!/usr/bin/python
import git
import sys
import itertools
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("op")
parser.add_argument("-f", default=None)
parser.add_argument("-v", action="store_true", default=False)
args = parser.parse_args()

def verbose(msg, *_args, **kwargs):
    if args.v:
        print(msg.format(*_args, **kwargs))

def feature_base(at_ref):
    for commit in r.iter_commits(r.branches["develop"], max_count=30):
        if commit in r.iter_commits(at_ref, max_count=30):
            verbose("{} based at {} in develop", at_ref, commit)
            return commit

def feature_files_changed(ref):
    result = []
    base = feature_base(ref)

    if not base:
        print("Can't find base commit for {}!", ref)
        return None

    for c in r.iter_commits(ref):
        if c == base:
            break
        else:
            verbose("Adding changes from {}", c)
            result += c.stats.files.keys()

    return result

def features_conflicts(ref1, ref2):
    verbose("Finding conflicts between {}", ref1)
    ref1_changes = feature_files_changed(ref1)
    verbose("")
    verbose("And {}", ref2)

    if ref2 == r.branches["develop"]:
        ref1_base = feature_base(ref1)
        ref2_changes = []
        for c in r.iter_commits(r.branches["develop"]):
            if c == ref1_base:
                break
            else:
                verbose("Adding changes from {}", c)
                ref2_changes += c.stats.files.keys()
    else:
        ref2_changes = feature_files_changed(ref2)

    verbose("")
    for path in ref1_changes:
        verbose("{} changed {}", ref1, path)
    for path in ref2_changes:
        verbose("{} changed {}", ref2, path)

    return set(ref1_changes).intersection(set(ref2_changes))

if __name__ == "__main__":
    r = git.Repo(".")
    develop_head = r.branches["develop"].commit

    if args.op == "revert" or args.op == "r":
        based_on = feature_base(r.head)

        head_files = list(map(lambda x: x.b_path, based_on.diff(r.head.commit)))
        working_files = list(map(lambda x: x.b_path, based_on.diff(None)))
        verbose("{} total edits from HEAD, {} from working tree", len(head_files), len(working_files))

        ok = True
        for file in head_files:
            if file not in working_files:
                ok = False
                print("{} was reverted!".format(file))

        if ok:
            print("No reverts")
            sys.exit(0)
        else:
            sys.exit(1)

    elif args.op == "conflict" or args.op == "c":
        if args.f:
            ref2 = r.branches[args.f]
        else:
            ref2 = r.branches["develop"]
            current_base = feature_base(r.head)
            ahead_count = 0
            for c in r.iter_commits(r.branches["develop"]):
                if c == current_base:
                    break
                else:
                    ahead_count += 1
            print("Develop is {} commits ahead of current branch".format(ahead_count))

        conflicts = features_conflicts(r.head, ref2)

        for path in conflicts:
            print("{} was changed in both branches!".format(path))

        if len(conflicts) == 0:
            print("")
            print("No conflicts")
            sys.exit(0)
        else:
            sys.exit(1)

    else:
        print("Unknown operation!")
        sys.exit(1)

