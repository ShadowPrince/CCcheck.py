#compdef ccutil.py

_ccutil() {
  _arguments -s -S \
      '-h[prints help]:' \
      '-v[verbose]:' \
      '-b[branch]:branch:_get_branches' \
      '-c[current branch]:currentbranch:_get_branches' \
      '--browser[browser]:' \
      '--reverts[add reverts to manual update]:' \
      '--group[ccuid group]:' \
      '--always-open-browser[always open browser]:' \
      '1:op:(c conflict r reverts up update)' \
      '2:secop:(auto manual id setid reset browse)' \
      '*:args:_files'
}

_get_branches() {
  _branches=(${${(f)"$(git branch | grep -v \* | sed -e 's/ //g')"}})
  compadd -a _branches
}

_ccutil "$@"

