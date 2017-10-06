#compdef ccutil.py

_ccutil() {
  _arguments -s -S \
      '-h[prints help]:' \
      '-v[verbose]:' \
      '-b[branch]:branch:_get_branches' \
      '--browser[browser]:' \
      '--always-open-browser[always open browser]:' \
      '1:op:(c r up)' \
      '2:secop:(auto manual)' \
      '*:args:_gnu_generic'
}

_get_branches() {
  _branches=(${${(f)"$(git branch | grep -v \* | sed -e 's/ //g')"}})
  compadd -a _branches
}

_ccutil "$@"

