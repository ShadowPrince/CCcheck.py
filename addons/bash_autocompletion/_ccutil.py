_ccutilpy_completion() 
{
    local prev opts
    COMPREPLY=('c' 'conflict' 'r' 'revert' 'up' 'update' '--always-open-browser' '--browser' '--reverts' '-h' '-b' '-v' '-q' '-a')
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    if [[ ${prev} == "-b" ]] ; then
        COMPREPLY=($(git branch | grep -v \* | sed -e 's/ //g'))
        return 0
    fi

    if [[ ${prev} == "up" ]] ; then
        COMPREPLY=('auto' 'manual')
        return 0
    fi
}
complete -F _ccutilpy_completion ccutil.py
