_ccutilpy_completion() 
{
    local prev opts
    COMPREPLY=('c' 'r' 'up')
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    if [[ ${prev} == "-b" ]] ; then
        COMPREPLY=($(git branch | grep -v \* | sed -e 's/ //g'))
        return 0
    fi
}
complete -F _ccutilpy_completion ccutil.py
