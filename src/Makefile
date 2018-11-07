# Makefile for Outrun RPM packages - called by rpmbuild %make_install
# It installs doc files, man pages and the file/dir structure under ./files

NAME      := $(RPM_PACKAGE_NAME)
VERSION   := $(shell rpm -q --qf '%{version}\n' --specfile ../$(NAME).spec)
SRCDIR    := $(shell rpm --eval %_sourcedir)

files     := $(shell find files/ -type f | cut -d/ -f2-)
dirs      := $(shell find files/ -type d | cut -d/ -f2-)

man1dir   := $(DESTDIR)/usr/share/man/man1
man5dir   := $(DESTDIR)/usr/share/man/man5
man7dir   := $(DESTDIR)/usr/share/man/man7
man8dir   := $(DESTDIR)/usr/share/man/man8

.PHONY: all doc man files

default: all

doc:
	install -m 0755 -d $(DESTDIR)/usr/share/doc/$(NAME)
	test -f COPYING   && install -m 0644 -pt $(DESTDIR)/usr/share/doc/$(NAME) COPYING   || true
	test -f CHANGELOG && install -m 0644 -pt $(DESTDIR)/usr/share/doc/$(NAME) CHANGELOG || true
	test -f README    && install -m 0644 -pt $(DESTDIR)/usr/share/doc/$(NAME) README    || true

man:
	install -m 0755 -d $(man1dir) $(man5dir) $(man7dir) $(man8dir)
	
	test -d man1 && find man1 -type f | xargs install -m 0644 -pt $(man1dir) || true
	test -d man5 && find man5 -type f | xargs install -m 0644 -pt $(man5dir) || true
	test -d man7 && find man7 -type f | xargs install -m 0644 -pt $(man7dir) || true
	test -d man8 && find man8 -type f | xargs install -m 0644 -pt $(man8dir) || true

	find $(DESTDIR)/usr/share/man -type f ! -name "*.gz" | xargs -I% gzip %

all:

files:
	for d in $(dirs); do install -m 0755 -d $(DESTDIR)/$$d ; done
	for f in $(files); do install -m 0644 -pt $(DESTDIR)/$$(dirname $$f)/ files/$$f ; done

install: man doc files

