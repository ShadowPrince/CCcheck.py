## Installation

* `sudo easy_install GitPython`
* `chmod +x CCcheck.py`
* Link `CCcheck.py` to `$PATH`

## Usage

`CCcheck.py OP`

## Operation list

* `revert` (or `r`) - check current working tree agains current repo `HEAD` for reverted files. Should be used before amending.
    Basically it comparest list of changed files of `HEAD` against it's base commit in `develop` and the same list, only with current working tree and `develop`. If there's a file that was changed, commited, and now reverted to it's `develop` state in the working tree app will print an alert and exit with 1.
* `conflict` (or `c`) - check pending changed files in develop (commits that was made after current's branch base commit) agains changed files in current branch. Should be used before rebasing.
    It compares list of changed files in `develop` commits which are aread of current branch base commit and list of files that was changed in branch, if there's files that were changed in both places app will print an alert and exit with 1.

## Arguments

* `-v` - verbose. Use this when in doubt
* `-f` - argument for `conflict` op which will use different branch instead of `develop`.
