%define major		5.43
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Summary:	A tcl extension for simplifying program-script interaction
Name:		expect
Version:	5.43.0
Release:	%mkrel 15
Group:		System/Libraries
License:	BSD
URL:		http://expect.nist.gov/
Source:		http://expect.nist.gov/src/%{name}-%{version}.tar.bz2
Patch10:	expect-fedora-5.32.2-random.patch
Patch13:	expect-5.32.2-fixcat.patch
Patch16:	expect-fedora-5.38.0-spawn-43310.patch
Patch18:	expect-fedora-5.43.0-h-comments.patch
Patch19:	expect-fedora-5.38.0-lib-spec.patch
Patch20:	expect-5.43.0.configure.patch
Patch21:	expect-5.43-soname.diff
# from fedora core
Patch22:	expect-fedora-5.43.0-tcl8.5.patch
# fix up install locations: let expect's 'libdir', the system libdir
# where the shared libs go, and the tcl dir all be different. also
# install a properly versioned shared library, and a couple other
# fixes.
Patch23:	expect-5.43.0-locations.patch
# fix for tcl 8.6
Patch24:	expect-5.43.0-tcl8.6.patch
# fix log file perms (Fedora)
Patch25:	expect-fedora-5.43.0-log_file.patch
Patch26:	expect-5.43.0-tclreq.patch
BuildRequires:	tcl tcl-devel
BuildRequires:	tk tk-devel
BuildRequires:	libxscrnsaver-devel
BuildRequires:	autoconf2.1
Requires:	tcl
Epoch:		1
Requires:	%{libname} = %{epoch}:%{version}
Buildroot:	%{_tmppath}/%{name}-%{version}

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

%setup -q -n %{name}-%{major}
%patch10 -p1 -b .random
%patch13 -p1 -b .fixcat
%patch16 -p1 -b .spawn
%patch18 -p1
%patch19 -p1 -b .libdir
%patch20
%patch21 -p1
%patch22 -p1 -b .tcl8.5
%patch23 -p1 -b .location
%patch24 -p1 -b .tcl86
%patch25 -p1 -b .log
%patch26 -p1 -b .tclreq

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

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog FAQ HISTORY NEWS README
%{_bindir}/*
%{_libdir}/%{name}%{major}
%{tcl_sitearch}/%{name}%{major}
%{_mandir}/man1/*
%{_mandir}/man3/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.1

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a

%files examples
%doc example/*
