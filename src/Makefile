#============================================================================
# Title       : Makefile
# Description : Makefile for asmdisks
# Author      : Bart Sjerps <bart@outrun.nl>
# License     : GPLv3+
# ---------------------------------------------------------------------------
NAME      := $(RPM_PACKAGE_NAME)
VERSION    = $(shell rpm -q --qf '%{version}\n' --specfile ../$(NAME).spec)
SRCDIR     = $(shell rpm --eval %_sourcedir)

files     := $(shell find files/ -type f | cut -d/ -f2-)
dirs      := $(shell find files/ -type d | cut -d/ -f2-)

man1       = $(wildcard bin/*)
man8       = $(wildcard sbin/*)

man1dir    = $(DESTDIR)/usr/share/man/man1
man8dir    = $(DESTDIR)/usr/share/man/man8

.PHONY: all install man

all:

man:
	install -m 0755 -d $(man1dir)
	install -m 0755 -d $(man8dir)
	$(foreach exe,$(man1),$(exe) --mandump > $(man1dir)/$(notdir $(exe)).1 ;echo mandump $(exe);)
	$(foreach exe,$(man8),$(exe) --mandump > $(man8dir)/$(notdir $(exe)).8 ;echo mandump $(exe);)
	find $(man1dir) $(man8dir) -type f | xargs -L1 gzip

install: man
	install -d 0755 $(DESTDIR)/usr/bin
	install -d 0755 $(DESTDIR)/usr/share/doc/asmdisks
	
	install -m 0755 -pt $(DESTDIR)/usr/bin bin/*
	install -m 0755 -pt $(DESTDIR)/usr/share/doc/asmdisks doc/*
	
	for d in $(dirs); do install -m 0755 -d $(DESTDIR)/$$d ; done
	for f in $(files); do install -m 0644 -pt $(DESTDIR)/$$(dirname $$f)/ files/$$f ; done

