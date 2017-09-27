#compdef ccutil.py

_ccutil() {
  _arguments -s -S \
    '-b[branch]:branch:_get_branches' \
    '-v[verbose]' \
    '--always-open-browser' \
    '*:op:(r c up)'
}

_get_branches() {
  _branches=(${${(f)"$(git branch | grep -v \* | sed -e 's/ //g')"}})
  compadd -a _branches
}

_ccutil "$@"

