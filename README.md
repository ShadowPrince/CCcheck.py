
![ccutil](https://raw.githubusercontent.com/ShadowPrince/ccutil/master/addons/screenshots/over.png)

## Installation

* `sudo easy_install GitPython`
* `chmod +x ccutil.py`
* Link `ccutil.py` to `$PATH`

## Usage

`ccutil.py OP ARGS`

## Operation list

### `revert` (or `r`)
Check current working tree agains current repo `HEAD` for reverted files. Should be used before amending.
Basically it comparest list of changed files of `HEAD` against it's base commit in `develop` and the same list, only with current working tree and `develop`. If there's a file that was changed, commited, and now reverted to it's `develop` state in the working tree app will print an alert and exit with 1.

### `conflict` (or `c`)
Check pending changed files in develop (commits that was made after current's branch base commit) agains changed files in current branch. Should be used before rebasing.
It compares list of changed files in `develop` commits which are aread of current branch base commit and list of files that was changed in branch, if there's files that were changed in both places app will print an alert and exit with 1.

_Arguments_:

* `-b BRANCH` - check for conflicts against `BRANCH` instead of develop.
* `-r CCID` - check for conflicts against review #`CCID` instead of develop.
* `-c BRANCH` - set current branch (instead the active one from git)

### `update` (or `up`)
ccollab commandline helper. At first run creates CC with name matching last commit message, updates it on subsequent runs.

_Following operations are available_:

* `auto` - upload files that was changed in this branch (matched against `develop`)
* `manual [FILE]` - upload files from paths in arguments
* `id` - get CC id for current branch
* `setid ID` - set CC id for current branch
* `reset` - reset CC id

_Arguments_:

* `-a` - append only mode. Instead of creating the review the app will fail
* `-i` - ignore missing files
* `--commit COMMIT` - use single commit to update the review
* `--reverts` - append files that was reverted to `manual` list of files
* `--browser APPLICATION` - browser to use after creating CCs (doesn't open one when argument is not provided)
* `--always-open-browser` - open browser even on CC update
* `--dry-run` - perform dry run (don't actually send anything, also enables `-v`)

It's encouraged to make an alias for `ccutil.py` that will incapsulate those settings.

## Global arguments

* `-v` - verbose. Use this when in doubt
* `-q` - only output useful information

## Participants config file

`~/.ccutilparticipants` is used to configure group and review participants. First line is ID of the group to use, and other lines is `LOGIN ROLE`, where role can be either `Reviewer` or `Observer`. If the file is present, **ccutil** will use the group and attach participants on review creation.

## Addons

There's few goodies in the `addons` folder - autocompletion for bash/zsh, firefox user style and few useful git hooks.

