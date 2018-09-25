#============================================================================
# Title       : manpage.bash
# Description : Functions to generate manpages in shell scripts
# Version     : 1.0
# Author      : Bart Sjerps <bart@outrun.nl>
# Section     : 1
# License     : GPLv3+
#============================================================================
# How to use:
# Define: Title, Description, Version, Author and License as above
# Optional: Section, Manual, Source
# Then define usage function - see help2man(1) for formatting
# Then add this line
# source /usr/outrun/lib/manpage.bash || die "manpage extension not found"
#
# The date listed in the manpage is retrieved from the mtime of the file itself
# ---------------------------------------------------------------------------

version() {
  local version=$(awk -F: '/^# Version / {sub(/ /,"",$NF) ; print $NF}' $0)
  local author=$(awk -F: '/^# Author / {sub(/ /,"",$NF) ; print $NF}' $0)
  local license=$(awk -F: '/^# License / {sub(/ /,"",$NF) ; print $NF}' $0)
  case $license in
    GPLv3+) local ltext="License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>." ;;
    *)      local ltext="license $license (unknown)"
  esac
  cat <<- EOF
	$(basename $0) ${version:-0.0}
	Written by ${author:-<No Author>}, ${ltext}
	@br
	If you have suggestions for improvements in this tool, please send them along via the above address.
	
	Copyright (c) 2018 ${author% <*}
	EOF
  echo @br
  echo This is free software: you are free to change and redistribute it.  There is NO WARRANTY, to the extent permitted by law.
}

mandump() {
  test -x /usr/bin/help2man || exit 10
  local desc=$(awk -F: '/^# Description/ {sub(/ /,"",$NF) ; print $NF; exit}' $0)
  local sect=$(awk -F: '/^# Section/     {sub(/ /,"",$NF) ; print $NF; exit}' $0)
  local manual=$(awk -F: '/^# Manual/    {sub(/ /,"",$NF) ; print $NF; exit}' $0)
  local source=$(awk -F: '/^# Source/    {sub(/ /,"",$NF) ; print $NF; exit}' $0)
  SOURCE_DATE_EPOCH=$(stat -c %Y $0); export SOURCE_DATE_EPOCH
  help2man -N -n "$desc" -s "${sect:-1}" -S "${source:-Outrun}" -m "${manual:-Outrun manual}" $0 | sed "s/^@/\./"
}

case $1 in
  -\?)       man $(basename $0) ; exit;;
  --help)    usage   ; exit ;;
  --version) version ; exit ;;
  --mandump) mandump ; exit ;;
esac

