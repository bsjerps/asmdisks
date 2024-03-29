Name:		asmdisks
Summary:	Replacement for Oracle ASMLib using UDEV
Version:	2.0.2
Release:	1%{?dtap}
BuildArch:	noarch
License:	GPLv3+
Source0:	%{name}-%{version}.tbz2
Requires:	kernel >= 2.6.27
Requires:	parted lsscsi bc sysstat
Requires:   python3-prettytable

# Maybe for diskheader?
# Requires:	vim-common

%description 
asmdisks provides a way to manage Oracle ASM volumes using Linux UDEV.
It is an alternative to Oracle ASMLib.
You can use a combination of entire disks, partitions or mapper
(including multipath) devices to configure as block devices for
Oracle ASM (or other purposes such as destructive IOPS performance testing)
Also supports DellEMC Powerpath (emcpower) and DellEMC ScaleIO (scini) volumes.

%prep
%setup -q -n %{name}

%install
rm -rf %{buildroot}

install -m 0755 -d %{buildroot}/etc
install -m 0755 -d %{buildroot}/usr/bin
install -m 0755 -d %{buildroot}/usr/lib/%{name}
install -m 0755 -d %{buildroot}/usr/share/doc/%{name}
install -m 0755 -d %{buildroot}/usr/share/man/man1

cp -pr etc/*    %{buildroot}/etc
cp -p  bin/*    %{buildroot}/usr/bin
cp -pr lib/*    %{buildroot}/usr/lib/%{name}
cp -p  doc/*    %{buildroot}/usr/share/doc/%{name}
cp -p  man1/*   %{buildroot}/usr/share/man/man1

touch %{buildroot}/etc/asmtab.db

%files
%defattr(0444,root,root)
%doc /usr/share/doc/%{name}/*
%defattr(0644,root,root)
%ghost /etc/asmtab.db
/etc/bash_completion.d/asm.bash
/usr/share/man/man1/*
%defattr(0644,root,root)
/usr/lib/%{name}
%defattr(0755,root,root)
/usr/bin/asm
/usr/bin/asmstat
/usr/bin/wipedisk
/usr/bin/diskheader
