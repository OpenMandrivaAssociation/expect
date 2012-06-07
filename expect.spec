%define major		5.45
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Summary:	A tcl extension for simplifying program-script interaction
Name:		expect
Version:	5.45
Release:	%mkrel 1
Group:		System/Libraries
License:	BSD
URL:		http://expect.nist.gov/
Source:		http://expect.nist.gov/src/%{name}%{version}.tar.gz
Patch0:		expect-fedora-5.43.0-pkgpath.patch
Patch1:		expect-fedora-5.45-match-gt-numchars-segfault.patch
Patch10:	expect-fedora-5.32.2-random.patch
# fix log file perms (Fedora)
Patch25:	expect-fedora-5.43.0-log_file.patch
BuildRequires:	tcl tcl-devel
BuildRequires:	tk tk-devel
BuildRequires:	pkgconfig(xscrnsaver)
BuildRequires:	autoconf2.1
Requires:	tcl
Epoch:		1
Requires:	%{libname} = %{epoch}:%{version}
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
Requires:	%{libname} = %{epoch}:%{version}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	lib%{name}-devel = %{epoch}:%{version}-%{release}
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
%patch10 -p1 -b .random
%patch25 -p1 -b .log

%build
autoconf-2.13

for f in config.guess config.sub ; do
        test -f /usr/share/libtool/$f || continue
        find . -type f -name $f -exec cp /usr/share/libtool/$f \{\} \;
done

chmod u+w testsuite/configure
. %{_libdir}/tclConfig.sh

%configure \
    --enable-gcc \
    --enable-shared \
    --with-tclinclude=$TCL_SRC_DIR

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

# cleanup
rm -f %{buildroot}%{_libdir}/%{name}%{major}/*.a

# (fc) make sure .so files are writable by root
chmod 755 %{buildroot}%{_libdir}/*.so

%clean
rm -rf %{buildroot}

%files
%doc ChangeLog FAQ HISTORY NEWS README
%{_bindir}/*
%{_libdir}/%{name}%{major}
%{tcl_sitearch}/%{name}%{major}
%{_mandir}/man1/*
%{_mandir}/man3/*

%files -n %{libname}
%{_libdir}/lib*.so.1

%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a

%files examples
%doc example/*
