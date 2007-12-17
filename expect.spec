%define	name	expect
%define	version	5.43.0
%define major	5.43
%define libname	%mklibname %{name} %{major}

Summary:	A tcl extension for simplifying program-script interaction
Name:		%{name}
Version:	%{version}
Release:	%mkrel 11
Group:		System/Libraries
License:	BSD
URL:		http://expect.nist.gov/
Source:		http://expect.nist.gov/src/%{name}-%{version}.tar.bz2
Patch10:	expect-5.32.2-random.patch
Patch13:	expect-5.32.2-fixcat.patch
Patch16:	expect-5.32.2-spawn.patch
Patch18:	expect-5.32.2-setpgrp.patch
Patch19:	expect-5.32-libdir.patch
Patch20:	expect-5.43.0.configure.patch
Patch21:	expect-5.43-soname.diff
# from fedora core
Patch22:	expect-5.43.0-tcl8.5.patch
BuildRequires:	tcl tcl-devel
BuildRequires:	tk tk-devel
BuildRequires:	libxscrnsaver-devel
BuildRequires:	autoconf2.1
Requires:	tcl
Epoch:		1
Requires:	%{libname} = %{epoch}:%{version}

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

%package -n	%{libname}-devel 
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{libname} = %{epoch}:%{version}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	lib%{name}-devel = %{epoch}:%{version}-%{release}

%description -n	%{libname}-devel
This package contains development files for %{name}.

%prep

%setup -q -n %{name}-%{major}
%patch10 -p1 -b .random
%patch13 -p1 -b .fixcat
%patch16 -p1 -b .spawn
%patch18 -p2
%patch19 -p1 -b .libdir
%patch20
%patch21 -p1
%patch22 -p1 -b .tcl8.5

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

%install
rm -rf %{buildroot}

# If %{_libdir} is not %{_prefix}/lib, then define EXTRA_TCLLIB_FILES
# which contains actual non-architecture-dependent tcl code.
if [ "%{_libdir}" != "%{_prefix}/lib" ]; then
    EXTRA_TCLLIB_FILES="%{buildroot}%{_prefix}/lib/*"
fi

%makeinstall tcl_libdir=%{buildroot}%{_libdir} \
	libdir=%{buildroot}%{_libdir}/expect%{major} \
	TKLIB_INSTALLED="-L%{buildroot}%{_libdir} -ltk" \
	TCLLIB_INSTALLED="-L%{buildroot}%{_libdir} -ltcl"

# fix the shared libname
rm -f %{buildroot}%{_libdir}/lib%{name}%{major}.so*
install -m0755 lib%{name}%{major}.so %{buildroot}%{_libdir}/lib%{name}%{major}.so.1
ln -snf lib%{name}%{major}.so.1 %{buildroot}%{_libdir}/lib%{name}%{major}.so

# remove cryptdir/decryptdir, as Linux has no crypt command (bug 6668).
rm -f %{buildroot}%{_bindir}/{cryptdir,decryptdir}
rm -f %{buildroot}%{_mandir}/man1/{cryptdir,decryptdir}.1*

# cleanup
rm -f %{buildroot}%{_libdir}/%{name}%{major}/*.a

# (fc) make sure .so files are writable by root
chmod 755 %{buildroot}%{_libdir}/*.so

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog FAQ HISTORY NEWS README
%{_bindir}/*
%{_libdir}/%{name}%{major}
%{_mandir}/man1/*
%{_mandir}/man3/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a


