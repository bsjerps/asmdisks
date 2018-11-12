Name:		asmdisks
Summary:	Replacement for Oracle ASMLib using UDEV
Version:	1.4.5.2
Release:	1%{?dtap}
BuildArch:	noarch
License:	GPLv3+
Group:		Outrun/Extras
Source0:	%{name}-%{version}.tbz2
Requires:	kernel >= 2.6.27
Requires:	parted lsscsi bc sysstat
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

%make_install

install -m 0755 -d %{buildroot}/usr/bin

install -m 0755 -pt %{buildroot}/usr/bin bin/*

%files
%defattr(0444,root,root)
%doc /usr/share/doc/%{name}/*
%defattr(0644,root,root)
/etc/bash_completion.d/asm.bash
/usr/share/man/man1/*
%defattr(0755,root,root)
/usr/bin/asm
/usr/bin/asmstat
/usr/bin/wipedisk
/usr/bin/diskheader
