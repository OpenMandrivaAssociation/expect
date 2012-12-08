%define major		5.45
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

%if %{_use_internal_dependency_generator}
%define __noautoreq '/depot/path/expect|/depot/path/expectk'
%endif

Summary:	A tcl extension for simplifying program-script interaction
Name:		expect
Version:	5.45
Release:	2
Epoch:		1
Group:		System/Libraries
License:	BSD
URL:		http://expect.nist.gov/
Source:		http://expect.nist.gov/src/%{name}%{version}.tar.gz
Patch0:		expect-5.45-pkgpath.patch
Patch1:		expect-fedora-5.45-match-gt-numchars-segfault.patch
Patch2:		expect-5.45-sfmt.patch
Patch3:		expect-5.45-soname.patch
Patch10:	expect-fedora-5.32.2-random.patch
# fix log file perms (Fedora)
Patch25:	expect-fedora-5.43.0-log_file.patch
BuildRequires:	tcl tcl-devel
BuildRequires:	tk tk-devel
BuildRequires:	pkgconfig(xscrnsaver)
BuildRequires:	autoconf
Requires:	tcl
Requires:	%{libname} = %{EVRD}
Provides:	%{_bindir}/expect
Provides:	%{_bindir}/expectk

%description
Expect is a tcl extension for automating interactive applications such
as telnet, ftp, passwd, fsck, rlogin, tip, etc.  Expect is also useful
for testing the named applications.  Expect makes it easy for a script
to control another program and interact with it.

Install the expect package if you'd like to develop scripts which interact
with interactive applications.  You'll also need to install the tcl
package.

%package -n	%{libname}
Summary:	Shared libraries for %{name}
Group:		System/Libraries

%description -n %{libname}
Expect is a tcl extension for automating interactive applications such
as telnet, ftp, passwd, fsck, rlogin, tip, etc.  Expect is also useful
for testing the named applications.  Expect makes it easy for a script
to control another program and interact with it.

Install the expect package if you'd like to develop scripts which interact
with interactive applications.  You'll also need to install the tcl
package.

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	lib%{name}-devel = %{EVRD}
Obsoletes:	%{mklibname expect 5.43 -d} < %{version}-%{release}

%description -n	%{develname}
This package contains development files for %{name}.

%package	examples
Summary:	Example scripts for %{name}
Group:		System/Libraries

%description	examples
This package contains example scripts for Expect.

Expect is a tcl extension for automating interactive applications such
as telnet, ftp, passwd, fsck, rlogin, tip, etc.  Expect is also useful
for testing the named applications.  Expect makes it easy for a script
to control another program and interact with it.

Install the expect package if you'd like to develop scripts which interact
with interactive applications.  You'll also need to install the tcl
package.

%prep
%setup -q -n %{name}%{major}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch10 -p1 -b .random
%patch25 -p1 -b .log

%build
autoconf

for f in config.guess config.sub ; do
        test -f /usr/share/libtool/$f || continue
        find . -type f -name $f -exec cp /usr/share/libtool/$f \{\} \;
done

chmod u+w testsuite/configure
. %{_libdir}/tclConfig.sh

%configure \
    --enable-gcc \
    --enable-shared

%make

%check
make test

%install
rm -rf %{buildroot}

%makeinstall_std TKLIB_INSTALLED="-L%{buildroot}%{_libdir} -ltk" \
	TCLLIB_INSTALLED="-L%{buildroot}%{_libdir} -ltcl" \
	INSTALL_ROOT=%{buildroot}

# fix up library naming
mv %{buildroot}%{_libdir}/lib%{name}%{major}.so %{buildroot}%{_libdir}/lib%{name}%{major}.so.1
ln -s lib%{name}%{major}.so.1 %{buildroot}%{_libdir}/lib%{name}%{major}.so

# remove cryptdir/decryptdir, as Linux has no crypt command (bug 6668).
rm -f %{buildroot}%{_bindir}/{cryptdir,decryptdir}
rm -f %{buildroot}%{_mandir}/man1/{cryptdir,decryptdir}.1*

# (fc) make sure .so files are writable by root
chmod 755 %{buildroot}%{_libdir}/*.so

%files
%doc ChangeLog FAQ HISTORY NEWS README
%{_bindir}/*
%{tcl_sitearch}/%{name}%{major}
%{_mandir}/man1/*
%{_mandir}/man3/*

%files -n %{libname}
%{_libdir}/lib*.so.1

%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.so

%files examples
%doc example/*


%changelog
* Fri Jun 08 2012 Andrey Bondrov <abondrov@mandriva.org> 1:5.45-1
+ Revision: 803315
- Re-diff some older patches (soname and path)
- Fix tcl include path, add patch to fix string format
- Use new autoconf
- New version 5.45, drop/update patches
- Rebuild against new tcl

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1:5.43.0-20
+ Revision: 664163
- mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1:5.43.0-19mdv2011.0
+ Revision: 605112
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 1:5.43.0-18mdv2010.1
+ Revision: 518998
- rebuild

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1:5.43.0-17mdv2010.0
+ Revision: 424392
- rebuild

* Thu Mar 05 2009 Frederic Crozat <fcrozat@mandriva.com> 1:5.43.0-16mdv2009.1
+ Revision: 348818
- Patch27: fix format security error
- Explicitly provides /usr/bin/expect and /usr/bin/expectk

* Fri Dec 05 2008 Adam Williamson <awilliamson@mandriva.org> 1:5.43.0-15mdv2009.1
+ Revision: 310143
- fix up the lib naming
- new devel policy
- add tclreq.patch: relax the tcl version require (breaks with pre-releases)
- add tcl8.6.patch: fix for tcl 8.6
- add locations.patch to fix up install locations for new policy
- sync patches with fedora

  + Gustavo De Nardin <gustavodn@mandriva.com>
    - run tests in rpm check stage

* Tue Jul 01 2008 Gustavo De Nardin <gustavodn@mandriva.com> 1:5.43.0-14mdv2009.0
+ Revision: 230451
- include expect's examples in an expect-examples subpackage

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1:5.43.0-13mdv2009.0
+ Revision: 220736
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sat Jan 12 2008 Thierry Vignaud <tv@mandriva.org> 1:5.43.0-12mdv2008.1
+ Revision: 149708
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Sep 07 2007 Anssi Hannula <anssi@mandriva.org> 1:5.43.0-11mdv2008.0
+ Revision: 82146
- buildrequires autoconf2.1
- rebuild for fixed soname of tcl

* Tue Jun 12 2007 Christiaan Welvaart <spturtle@mandriva.org> 1:5.43.0-10mdv2008.0
+ Revision: 38243
- add BuildRequires: libxscrnsaver-devel
- Patch22: work around build problems with tcl 8.5


* Mon Nov 06 2006 Thierry Vignaud <tvignaud@mandriva.com> 5.43.0-9mdv2007.0
+ Revision: 76911
- Import expect

* Mon Nov 06 2006 Thierry Vignaud <tvignaud@mandriva.com> 5.43.0-9mdv2007.1
- fix requires
- fix doc perms

* Wed Sep 20 2006 Oden Eriksson <oeriksson@mandriva.com> 5.43.0-8mdv2007.0
- fix deps

* Fri Jan 06 2006 Oden Eriksson <oeriksson@mandriva.com> 5.43.0-7mdk
- fix deps (i need thicker glasses)

* Fri Jan 06 2006 Oden Eriksson <oeriksson@mandriva.com> 5.43.0-6mdk
- fix deps

* Fri Jan 06 2006 Buchan Milne <bgmilne@mandriva.org> 5.43.0-5mdk
- bump epoch so it upgrades old bundled-with-tcl package

* Sun Jan 01 2006 Oden Eriksson <oeriksson@mandriva.com> 5.43.0-4mdk
- fix deps

* Sun Jan 01 2006 Oden Eriksson <oeriksson@mandriva.com> 5.43.0-3mdk
- fix library-without-ldconfig-postin

* Sun Jan 01 2006 Oden Eriksson <oeriksson@mandriva.com> 5.43.0-2mdk
- fix soname (P21) after looking at debian
- misc lib64 and spec file fixes

* Thu Dec 29 2005 Guillaume Rousse <guillomovitch@mandriva.org> 5.43.0-1mdk
- first release as a standalone package
- drop unused patches

