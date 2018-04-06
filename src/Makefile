#============================================================================
# Title       : Makefile
# Description : Makefile for asmdisks
# Author      : Bart Sjerps <bart@outrun.nl>
# License     : GPLv3+
# ---------------------------------------------------------------------------

version    = 1.4.4
prefix     = /usr/local
bindir     = $(prefix)/bin
mandir     = $(prefix)/share/man
docdir     = $(prefix)/share/doc

sysconfdir = /etc

all:

src:
	tar -jcvf $(HOME)/SOURCES/asmdisks-$(version).tbz2 --transform "s|^|asmdisks/|" *

rpm:	src
	cd ../SPECS ; rpmbuild -ba asmdisks.spec

install:
	install -d 0755 $(bindir)
	install -d 0755 $(sysconfdir)/bash_completion.d
	install -d 0755 $(mandir)/man1
	install -d 0755 $(docdir)/asmdisks
	install -m 0755 bin/asm bin/asmstat bin/diskheader bin/wipedisk $(bindir)
	install -m 0644 bin/asm.bash $(sysconfdir)/bash_completion.d
	install -m 0644 man/* $(mandir)/man1/
	install -m 0444 doc/* $(docdir)/asmdisks/

clean:
	rm $(HOME)/SOURCES/asmdisks-$(version).tbz2

.PHONY: install

