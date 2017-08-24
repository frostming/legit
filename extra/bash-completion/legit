_legit()
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="branches publish switch sync unpublish"
    local running=`git for-each-ref --format='%(refname:short)' --sort='refname:short' refs/heads`

    case "${prev}" in
        sy|sync)
            COMPREPLY=( $(compgen -W "${running}" -- ${cur}) )
            return 0
            ;;
        sw|switch)
            COMPREPLY=( $(compgen -W "${running}" -- ${cur}) )
            return 0
            ;;
        pub|publish)
            COMPREPLY=( $(compgen -W "${running}" -- ${cur}) )
            return 0
            ;;
        unp|unpublish|rs)
            local running=$(for x in `git ls-remote 2>/dev/null | grep refs/heads | awk '{ print $2 }' | sed -e 's/refs\/heads\///g'`; do echo ${x} ; done )
            COMPREPLY=( $(compgen -W "${running}" -- ${cur}) )
            return 0
            ;;
        *)
        ;;
    esac

    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
    return 0
}

complete -F _legit legit





_git_unpublish()
{
  local cur="${COMP_WORDS[COMP_CWORD]}"
  local running=$(for x in `git ls-remote 2>/dev/null | grep refs/heads | awk '{ print $2 }' | sed -e 's/refs\/heads\///g'`; do echo ${x} ; done )
  COMPREPLY=( $(compgen -W "${running}" -- ${cur}) )
  return 0
}

_complete_with_git_branch()
{
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local running=`git for-each-ref --format='%(refname:short)' --sort='refname:short' refs/heads`
    COMPREPLY=( $(compgen -W "${running}" -- ${cur}) )
    return 0
}

function _git_sync { _complete_with_git_branch; }
function _git_switch { _complete_with_git_branch; }
function _git_publish { _complete_with_git_branch; }

complete -F _git_sync git-sync
complete -F _git_switch git-switch
complete -F _git_publish git-publish
complete -F _git_unpublish git-unpublish
