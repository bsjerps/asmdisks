Name:		asmdisks
Summary:	Replacement for Oracle ASMLib using UDEV
Version:	1.4.5
Release:	1%{?prerel:.~%prerel}
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
Also supports EMC Powerpath and EMC DSSD volumes.
%prep
%setup -q -n %{name}

%install
rm -rf %{buildroot}
mkdir %{buildroot}

%make_install

%files
%defattr(0444,root,root)
%doc /usr/share/doc/%{name}/COPYING
%doc /usr/share/doc/%{name}/README
%defattr(0644,root,root)
/etc/bash_completion.d/asm.bash
/usr/share/man/man1/*.gz
%defattr(0755,root,root)
/usr/bin/asm
/usr/bin/asmstat
/usr/bin/wipedisk
/usr/bin/diskheader
