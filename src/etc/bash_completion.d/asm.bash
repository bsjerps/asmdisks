#============================================================================
# Title       : asm.bash
# Description : bash_completion file for asmdisks
# Author      : Bart Sjerps <bart@dirty-cache.com>
# License     : GPLv3+
# ---------------------------------------------------------------------------

_asm() {
  local cur prev opts cmd
  lsvols() { asm -nt list | cut -f1 ;}
  lsdevs() { lsblk -ndo kname ; }
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"
  cmd="${COMP_WORDS[1]}"
  opts="rescan list disks createdisk deletedisk renamedisk export import importrules importasm rebuild dump setup configure"
  if (( $COMP_CWORD == 1 )); then
    COMPREPLY=($(compgen -W "-h --version --tabs --nohead $opts" -- ${cur}))
  fi
  if (( $COMP_CWORD == 2 )); then
    case $cmd in
      createdisk) ;;
      deletedisk|renamedisk) COMPREPLY=($(compgen -W "$(lsvols)" -- ${cur})) ;;
      *) return 0 ;;
    esac
  fi
  if (( $COMP_CWORD == 3 )); then
    case $cmd in
      createdisk) COMPREPLY=($(compgen -W "$(lsdevs)" -- ${cur})) ;;
      *) return 0 ;;
    esac
  fi
}
complete -F _asm asm
