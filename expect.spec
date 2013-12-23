%define api	5.45
%define major	1
%define libname	%mklibname %{name} %{api} %{major}
%define devname	%mklibname %{name} -d

%if %{_use_internal_dependency_generator}
%define __noautoreq '/depot/path/expect|/depot/path/expectk'
%endif

Summary:	A tcl extension for simplifying program-script interaction
Name:		expect
Epoch:		1
Version:	5.45
Release:	8
Group:		System/Libraries
License:	BSD
Url:		http://expect.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/expect/Expect/%{version}/%{name}%{version}.tar.gz
Patch0:		expect-5.45-pkgpath.patch
Patch1:		expect-fedora-5.45-match-gt-numchars-segfault.patch
Patch2:		expect-5.45-sfmt.patch
Patch3:		expect-5.45-soname.patch
Patch10:	expect-fedora-5.32.2-random.patch
# fix log file perms (Fedora)
Patch25:	expect-fedora-5.43.0-log_file.patch
# Patch2: fixes minor man page formatting issue
Patch26:	expect-5.45-man-page.patch
# Patch4: fixes memory leak when using -re, http://sourceforge.net/p/expect/patches/13/
Patch28:	expect-5.45-re-memleak.patch
# Patch5: use vsnprintf instead of vsprintf to avoid buffer overflow
Patch29:	expect-5.45-exp-log-buf-overflow.patch
# Patch101: fixes bz674184 - mkpasswd fails randomly
Patch101:	expect-5.45-mkpasswd-dash.patch
# Patch102: fixes bz703702 - let user know that telnet is needed for
# running some examples
Patch102:	expect-5.45-check-telnet.patch
# Patch103: use full path to 'su', it's safer
Patch103:	expect-5.45-passmass-su-full-path.patch
# Patch104: rhbz 963889, fixes inaccuracy in mkpasswd man page
Patch104:	expect-5.45-mkpasswd-man.patch


BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
BuildRequires:	pkgconfig(xscrnsaver)
Requires:	tcl
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
Obsoletes:	%{_lib}expect5.45 < 1:5.45-4

%description -n %{libname}
This package contains the shared library for %{name}.

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
This package contains development files for %{name}.

%package	examples
Summary:	Example scripts for %{name}
Group:		System/Libraries

%description	examples
This package contains example scripts for Expect.

%prep
%setup -qn %{name}%{version}
%apply_patches

autoconf
autoreconf -fiv

for f in config.guess config.sub ; do
	test -f /usr/share/libtool/$f || continue
	find . -type f -name $f -exec cp /usr/share/libtool/$f \{\} \;
done

chmod u+w testsuite/configure
. %{_libdir}/tclConfig.sh

# MD fix doc perms
chmod 644 example/*

%build
%configure2_5x \
	--enable-gcc \
	--enable-shared

%make

%check
make test

%install
%makeinstall_std \
	TKLIB_INSTALLED="-L%{buildroot}%{_libdir} -ltk" \
	TCLLIB_INSTALLED="-L%{buildroot}%{_libdir} -ltcl" \
	INSTALL_ROOT=%{buildroot}

# fix up library naming
mv %{buildroot}%{_libdir}/lib%{name}%{api}.so %{buildroot}%{_libdir}/lib%{name}%{api}.so.1
ln -s lib%{name}%{api}.so.1 %{buildroot}%{_libdir}/lib%{name}%{api}.so

# remove cryptdir/decryptdir, as Linux has no crypt command (bug 6668).
rm -f %{buildroot}%{_bindir}/{cryptdir,decryptdir}
rm -f %{buildroot}%{_mandir}/man1/{cryptdir,decryptdir}.1*

# (fc) make sure .so files are writable by root
chmod 755 %{buildroot}%{_libdir}/*.so

%files
%doc ChangeLog FAQ HISTORY NEWS README
%{_bindir}/*
%{tcl_sitearch}/%{name}%{api}
%{_mandir}/man1/*
%{_mandir}/man3/*

%files -n %{libname}
%{_libdir}/libexpect%{api}.so.%{major}

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so

%files examples
%doc example/*
