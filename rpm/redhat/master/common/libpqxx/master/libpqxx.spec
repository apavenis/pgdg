%global		_vpath_builddir .
%global		libpqxxmajorver 7.3

Name:		libpqxx
Summary:	C++ client API for PostgreSQL
Epoch:		1
Version:	%{libpqxxmajorver}.1
Release:	1%{?dist}

License:	BSD
URL:		http://pqxx.org/
Source0:	https://github.com/jtv/libpqxx/archive/%{version}.tar.gz

BuildRequires:	gcc-c++
BuildRequires:	ninja-build
BuildRequires:	cmake
BuildRequires:	pkgconfig
BuildRequires:	libpq5-devel
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	xmlto

%description
C++ client API for PostgreSQL. The standard front-end (in the sense of
"language binding") for writing C++ programs that use PostgreSQL.
Supersedes older libpq++ interface.

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	pkgconfig
%description devel
%{summary}.

%package doc
Summary:	Developer documentation for %{name}
BuildArch:	noarch
%description doc
%{summary}.

%prep
%forgeautosetup

%build
mkdir build
pushd build
%cmake -G Ninja		\
  -DBUILD_DOC=ON	\
  ..
%ninja_build
popd

%install
pushd build
%ninja_install
popd

%files
%doc AUTHORS NEWS README.md VERSION
%license COPYING
%{_libdir}/%{name}-%{libpqxxmajorver}.so

%files devel
%dir %{_libdir}/cmake/%{name}
%doc README-UPGRADE
%{_includedir}/pqxx
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/%{name}-config.cmake
%{_libdir}/cmake/%{name}/%{name}-config-version.cmake
%{_libdir}/cmake/%{name}/%{name}-targets.cmake
%{_libdir}/cmake/%{name}/%{name}-targets-noconfig.cmake

%files doc
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/accessing-results.md
%{_docdir}/%{name}/datatypes.md
%{_docdir}/%{name}/escaping.md
%{_docdir}/%{name}/getting-started.md
%{_docdir}/%{name}/mainpage.md
%{_docdir}/%{name}/performance.md
%{_docdir}/%{name}/prepared-statement.md
%{_docdir}/%{name}/streams.md
%{_docdir}/%{name}/thread-safety.md
%{_docdir}/%{name}/html

%changelog
* Mon Feb 1 2021 Devrim Gündüz <devrim@gunduz.org> - 1:7.3.1-1
- Update to 7.3.1

* Fri Sep 25 2020 Devrim Gündüz <devrim@gunduz.org> - 1:7.2.0-1
- Update to 7.2.0

* Sat Jul 11 2020 Devrim Gündüz <devrim@gunduz.org> - 1:7.1.2-1
- Update to 7.1.2 using Fedora rawhide spec file.
