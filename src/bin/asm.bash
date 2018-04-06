#============================================================================
# Title              : asm.bash
# Description        : bash_completion file for asm script
# Author             : Bart Sjerps <bart@outrun.nl>
# License            : GPLv3+
# ---------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License at <http://www.gnu.org/licenses/> for
# more details.
# ---------------------------------------------------------------------------
# Revision history:
# 2016-10-20 : Added DSSD support
# 2015-03-10 : Updated for Powerpath support
# 2014-11-06 : Updated for new asm options
# 2014-10-24 : Created
# ---------------------------------------------------------------------------
_asm() {
  local cur prev opts cmd
  lsvols() { awk '$1!="#" && NF==3 {print $1}' /etc/asmtab 2>/dev/null ; }
  lsdevs() {
    find /dev/mapper -type l 2>/dev/null
    find /dev -maxdepth 1 -type b -name "sd[b-z]" -o -name "sd[a-z][a-z]" -o -name "emcpower*" -o -name "dssd[0-9][0-9][0-9][0-9]"
  }
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"
  cmd="${COMP_WORDS[1]}"
  (( $COMP_CWORD > 3)) && return 0
  if (( $COMP_CWORD == 2 )); then
    case $cmd in
      createdisk) ;;
      deletedisk|renamedisk) COMPREPLY=($(compgen -W "$(lsvols)" -- ${cur})) ; return 0 ;;
      *) return 0 ;;
    esac
  fi
  if (( $COMP_CWORD == 3 )); then
    case $cmd in
      createdisk) COMPREPLY=($(compgen -W "$(lsdevs)" -- ${cur})) ; return 0 ;;
      *) return 0 ;;
    esac
  fi
  opts="createdisk deletedisk renamedisk rescan scandisks listdisks disks list multi import"
  case ${prev} in
    createdisk) return 0 ;;
    *) ;;
  esac
  COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
  return 0
}
complete -F _asm asm
